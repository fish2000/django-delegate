#!/usr/bin/env python
# encoding: utf-8
"""
delegate/__init__.py

Created by Alexander Bohn on 2011-02-08.
Copyright (c) 2011 Objects in Space and Time. All rights reserved.

"""

import types
from django.db import models

consumable_types = (
    types.FunctionType,
    types.MethodType,
)

delegateable_types = consumable_types + (
    types.ClassType,
    types.TypeType,
)

def delegate(f_or_cls):
    """
    # Delegate QuerySet methods to a DelegateManager subclass,
    # by decorating them thusly:
    
    class CustomQuerySet(models.query.QuerySet):
        
        @delegate
        def qs_method(self, some_value):
            return self.filter(some_param__icontains=some_value)
        
        # ... 
    
    # You can also decorate classes.
    # This will delegate all of the classes' methods:
    
    @delegate
    class CustomQuerySet(models.query.QuerySet):
        
        def qs_method(self, some_value):
            return self.filter(some_param__icontains=some_value)
    
    # Both of these examples are equivalent.
    
    """
    if type(f_or_cls) in delegateable_types:
        
        # It's a class decorator.
        f_or_cls.__delegate__ = 1
        
        if hasattr(f_or_cls, '__dict__'):
            cls_funcs = filter(
                lambda attr: type(attr) in consumable_types,
                    f_or_cls.__dict__.values())
            for cls_func in cls_funcs:
                cls_func.__delegate__ = 1
    
    else:
        # It's a function decorator.
        f_or_cls.__delegate__ = 1
    
    return f_or_cls


class DelegateSupervisor(type(models.Manager)):
    """
    # The DelegateSupervisor metaclass handles delegation
    # of the specified methods from a QuerySet to a Manager
    # at compile-time. You don't need to invoke it to
    # perform your delegations.
    
    """
    def __new__(cls, name, bases, attrs):
        
        if '__queryset__' in attrs:
            
            from django.db.models.query import QuerySet
            qs_delegates = dict()
            qs = attrs.get('__queryset__', None)
            
            if issubclass(qs, QuerySet):
                qs_funcs = dict(filter(
                    lambda attr: type(attr[1]) in (delegateable_types),
                        qs.__dict__.items()))
                
                deleg = 0
                
                for f_name, f in qs_funcs.items():
                    if issubclass(qs, DelegateQuerySet):
                        deleg += 1
                        qs_delegates[f_name] = f
                    elif hasattr(f, '__delegate__'):
                        deleg += 1
                        qs_delegates[f_name] = f
                
                #print "Delegating %s funcs to %s from %s" % (
                #   deleg, name, qs.__name__)
                
                attrs.update(qs_delegates)
        
        return super(DelegateSupervisor, cls).__new__(
            cls, name, bases, attrs)


class DelegateManager(models.Manager):
    """
    # Subclass DelegateManager,
    # and specify the queryset from which to delegate:
    
    class CustomManager(DelegateManager):
        __queryset__ = CustomQuerySet
    
    # No other methods are necessary.
    
    """
    __metaclass__ = DelegateSupervisor
    
    use_for_related_fields = True
    
    def __init__(self, fields=None, *args, **kwargs):
        super(DelegateManager, self).__init__(*args, **kwargs)
        self.__managerfields__ = fields
    
    def get_query_set(self):
        qs = getattr(self, '__queryset__', None)
        if callable(qs):
            return qs(self.model, self.__managerfields__, using=self._db)
        return None
    
    # Defining these next three functions ensure that delegated
    # queryset functions that operate on sliced querysets --
    # e.g. 'return self[:10]' and suchlike -- will act as they
    # should if they're called on the manager instance.
    # ... as a bonus, you can also use them directly yourself --
    # e.g. 'MyModel.objects[0:10:2]', et cetera.
    
    def __getitem__(self, idx):
        return self.get_query_set().__getitem__(idx)
    
    def __setitem__(self, idx, val):
        return self.get_query_set().__setitem__(idx, val)
    
    def __delitem__(self, idx):
        return self.get_query_set().__delitem__(idx)


class DelegateQuerySet(models.query.QuerySet):
    """
    # ALL methods in a DelegateQuerySet subclass will
    # be delegated -- no decoration needed.
    # These two QuerySet subclasses work identically:
    
    class ManualDelegator(models.query.QuerySet):
        @delegate
        def qs_method(self):
            # ...
    
    class AutomaticDelegator(DelegateQuerySet):
        def qs_method(self):
            # ...
    
    """
    pass


"""
*********** WARNING -- HIGHLY EXPERIMENTAL -- FOR THE TRULY LAZY ***********

@micromanage -- get it? 'micromanage'? -- will cut out even more boilerplate
from your manager definitions. The following class decorator @micromanage
will set everything up for you, as per the above delegation apparatus, in
one fell swoop. You do this:


@micromanage(model=MyModel)
class MyQuerySet(models.query.QuerySet):
    def yodogg(self):
        return self.filter(yo__icontains="dogg")


... and everything will behave as though you had done ALL THIS:


class MyQuerySet(models.query.QuerySet):
    def yodogg(self):
        return self.filter(yo__icontains="dogg")

class MyManager(models.Manager):
    use_for_related_fields = True
    
    def __init__(self, fields=None, *args, **kwargs):
        super(MyManager, self).__init__(*args, **kwargs)
        self._fields = fields
    
    def get_query_set(self):
        return MyQuerySet(self.model, self._fields)
    
    def yodogg(self):
        return self.filter(yo__icontains="dogg")

class MyModel(models.Model):
    objects = MyManager()
    # ...


This minimizes boilerplate -- you're defining the manager AND queryset,
AND plugging the manager into the model in one fell swoop. @micromanage
creates a manager automatically, based on your queryset. If you already
have a manager defined on your target model (with "objects = SomeManager()"),
@micromanage will subclass the manager you've chosen, to keep your
refactoring to a minimum. It can also subclass an arbitrary manager class
you specify in the decorator kwargs -- see the micromanage.__init__() method
and the undergo_management_training() function below.

HOWEVER: the implementation is meta enough that it may very well break your
existing shit.

So DO NOT USE IT ANYWHERE NEAR PRODUCTION. Do not use it with existing
codebases **IN GENERAL** and expect everything to come up roses, unless you
have the most anal-retentive test suite around and/or you enjoy debugging
tracebacks with "Error when calling the metaclass bases" in them (google it
if you're curious). YOU HAVE BEEN WARNED. PROCEED PAST THIS POINT AT YOUR
OWN RISK.

At the moment, one limitation is: you have to define @micromanaged QuerySet
subclasses AFTER you define the model, because you need to pass the model
class itself into the decorator kwargs; in the future I may make it work by
naming the class with a string instead, but maybe not, as the thing is
already pushing it w/r/t complexity, I think.

"""
def undergo_management_training(queryset=None, progenitor=None):
    """
    I believe this function is an example of a 'factory', as per the
    lexographical usage of many Java and C# programming afficionatos.
    
    """
    if not progenitor:
        from django.db.models import Manager
        progenitor = Manager
    
    if queryset and hasattr(progenitor, '__class__'):
        
        # define the micromanager
        class MicroManager(progenitor.__class__):
            __queryset__ = queryset
            use_for_related_fields = True
            def __init__(smelf, fields=None, *args, **kwargs):
                super(MicroManager, smelf).__init__(*args, **kwargs)
                smelf.__managerfields__ = fields
            def get_query_set(smelf):
                queset = getattr(smelf, '__queryset__', None)
                if callable(queset):
                    return queset(smelf.model, smelf.__managerfields__)
                return smelf.all()
        
        # return it
        return MicroManager

class micromanage(object):
    
    cls_name_suffixes = ('QuerySet', 'Queryset', 'queryset')
    
    def __init__(self, *args, **kwargs):
        from django.db.models import Manager
        self.clsname = kwargs.pop('name', None)
        self.target_model = kwargs.pop('model', None)
        self.subclass = kwargs.pop('subclass', Manager)
        super(micromanage, self).__init__(*args, **kwargs)
        
        if not self.clsname:
            if hasattr(self.target_model, "__name__"):
                self.clsname = "%sMgr" % self.target_model.__name__
    
    def __call__(self, qs):
        from django.db.models import Model, Manager
        from django.db.models.query import QuerySet
        if issubclass(self.target_model, Model):
            theoldboss = getattr(self.target_model, 'objects', None)
            if theoldboss:
                # subclass the existant manager if one wasn't specified
                if self.subclass == Manager and issubclass(
                    theoldboss.__class__, Manager):
                    self.subclass = theoldboss # same as the new one
        
        # crank out the new manager
        newmgr = undergo_management_training(qs, self.subclass)
        
        # if there isn't an explicit name for the generated manager class,
        # try to make one out of this queryset's name:
        if not self.clsname:
            for suffix in self.cls_name_suffixes:
                if qs.__name__.endswith(suffix):
                    self.clsname = "%sMgr" % qs.__name__.rstrip(suffix)
                    break
        
        if not self.clsname: # if *still* not self.clsname
            self.clsname = "%sMgr" % qs.__name__
        
        newmgr.__name__ = self.clsname
        
        # delegate all methods. (currently we delegate everything,
        # ignoring the method status as it is set per the @delegate
        # decorator, which may change)
        if issubclass(qs, QuerySet):
            #qs_delegates = dict()
            qs_funcs = dict(filter(
                lambda attr: type(attr[1]) in consumable_types,
                    qs.__dict__.items()))
            for f_name, f in qs_funcs.items():
                setattr(newmgr, f_name, f)
        
        # if a target_model was specified, add an instance of the new
        # queryset class
        # TODO: do something useful with the class in the absence of
        # a target_model setting
        if issubclass(self.target_model, Model):
            qs.model = self.target_model
            self.target_model.add_to_class('objects', newmgr())
            self.target_model._default_manager = self.target_model.objects
        
        # we're done here.
        return qs


if __name__ == '__main__':
    pass
