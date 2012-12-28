#!/usr/bin/env python
# encoding: utf-8
"""
Execute this file to run the tests. The output should look like this:

Creating test database for alias 'default' ('/tmp/delegate-test.db')...
Destroying old test database 'default'...
Creating tables ...
Creating table auth_permission
Creating table auth_group_permissions
Creating table auth_group
Creating table auth_user_user_permissions
Creating table auth_user_groups
Creating table auth_user
Creating table django_content_type
Creating table django_session
Creating table django_site
Creating table django_admin_log
Creating table delegate_testmodel
Creating table delegate_testmicromanagermodel
Installing custom SQL ...
Installing indexes ...
No fixtures found.
test_EXPERIMENTAL_micromanager (delegate.tests.DelegateTests) ... ok
test_EXPERIMENTAL_micromanager_querysets (delegate.tests.DelegateTests) ... ok
test_automatic_delegate (delegate.tests.DelegateTests) ... ok
test_automatic_delegate_querysets (delegate.tests.DelegateTests) ... ok
test_manual_delegate (delegate.tests.DelegateTests) ... ok
test_manual_delegate_querysets (delegate.tests.DelegateTests) ... ok
test_slice_syntax (delegate.tests.DelegateTests) ... ok
Destroying test database for alias 'default' ('/tmp/delegate-test.db')...
Deleting test data: /tmp
    
----------------------------------------------------------------------
Ran 7 tests in 0.044s
    
OK

"""

import settings as delegate_settings
from django.conf import settings
if not settings.configured:
    settings.configure(**delegate_settings.__dict__)

from django.test import TestCase
from django.db import models
from delegate import DelegateManager, DelegateQuerySet, delegate, micromanage

if __name__ == "__main__":
    from django.core.management import call_command
    call_command('test', 'delegate',
        settings='delegate.settings',
        interactive=False, traceback=True, verbosity=2)
    import shutil, sys
    tempdata = delegate_settings.tempdata
    print "Deleting test data: %s" % tempdata
    shutil.rmtree(tempdata)
    sys.exit(0)

class AutoDelegateTestQuerySet(DelegateQuerySet):
    def yodogg(self):
        return self.filter(name__icontains="yo dogg")
    def iheardyoulike(self, whatiheardyoulike):
        return self.filter(name__icontains=whatiheardyoulike)

class ManualDelegateTestQuerySet(models.query.QuerySet):
    @delegate
    def queryinyourquery(self):
        return self.filter(name__icontains="yo dogg")
    def iheardyoulike(self, whatiheardyoulike):
        return self.filter(name__icontains=whatiheardyoulike)

class AutoDelegateTestManager(DelegateManager):
    __queryset__ = AutoDelegateTestQuerySet

class ManualDelegateTestManager(DelegateManager):
    __queryset__ = ManualDelegateTestQuerySet

class TestModel(models.Model):
    objects = AutoDelegateTestManager()
    other_objects = ManualDelegateTestManager()
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,
        blank=False, null=False, unique=False,
        default="Test Model Instance.")

class TestMicroManagerModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,
        blank=False, null=False, unique=False,
        default="Test Model Instance.")

@micromanage(model=TestMicroManagerModel)
class TestMicroManagerQuerySet(models.query.QuerySet):
    def yodogg(self):
        return self.filter(name__icontains="yo dogg")

class DelegateTests(TestCase):
    def setUp(self):
        self.instances = [
            TestModel(name="yo dogg."),
            TestModel(name="Yo Dogg!"),
            TestModel(),
            TestModel(),
            TestMicroManagerModel(name="yo dogg."),
            TestMicroManagerModel(name="Yo Dogg!"),
            TestMicroManagerModel(),
            TestMicroManagerModel(),
        ]
        for instance in self.instances:
            instance.save()
    
    def tearDown(self):
        TestModel.objects.all().delete()
        TestMicroManagerModel.objects.all().delete()
    
    def test_manual_delegate(self):
        self.assertTrue(hasattr(TestModel.other_objects, 'queryinyourquery'))
        self.assertFalse(hasattr(TestModel.other_objects, 'iheardyoulike'))
        self.assertEqual(
            TestModel.other_objects.queryinyourquery().count(),
            TestModel.other_objects.all().queryinyourquery().count())
    
    def test_manual_delegate_querysets(self):
        comparator = [repr(q) for q \
             in TestModel.other_objects.all().queryinyourquery()]
        self.assertQuerysetEqual(
            TestModel.other_objects.queryinyourquery(),
            comparator)
        self.assertQuerysetEqual(
            TestModel.other_objects.all().queryinyourquery(),
            comparator)
    
    def test_automatic_delegate(self):
        self.assertTrue(hasattr(TestModel.objects, 'yodogg'))
        self.assertTrue(hasattr(TestModel.objects, 'iheardyoulike'))
        self.assertEqual(
            TestModel.objects.yodogg().count(),
            TestModel.objects.all().yodogg().count())
        self.assertEqual(
            TestModel.objects.iheardyoulike('yo dogg').count(),
            TestModel.objects.all().iheardyoulike('yo dogg').count())
    
    def test_automatic_delegate_querysets(self):
        comparator = [repr(q) for q \
             in TestModel.objects.all().yodogg()]
        self.assertQuerysetEqual(
            TestModel.objects.yodogg(),
            comparator)
        self.assertQuerysetEqual(
            TestModel.objects.all().yodogg(),
            comparator)
    
    def test_slice_syntax(self):
        self.assertEqual(
            TestModel.objects[0].name,
            TestModel.objects.all()[0].name)
        self.assertEqual(
            TestModel.objects[0:2].count(),
            TestModel.objects.all()[0:2].count())
    
    def test_EXPERIMENTAL_micromanager(self):
        self.assertTrue(hasattr(TestMicroManagerModel.objects, 'yodogg'))
        self.assertEqual(
            TestMicroManagerModel.objects.yodogg().count(),
            TestMicroManagerModel.objects.all().yodogg().count())
    
    def test_EXPERIMENTAL_micromanager_querysets(self):
        comparator = [repr(q) for q \
             in TestMicroManagerModel.objects.all().yodogg()]
        self.assertQuerysetEqual(
            TestMicroManagerModel.objects.yodogg(),
            comparator)
        self.assertQuerysetEqual(
            TestMicroManagerModel.objects.all().yodogg(),
            comparator)

