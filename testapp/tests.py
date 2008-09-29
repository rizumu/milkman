from milkman import *
from testapp.models import *

import unittest
import types

from django.db import models

MODELS = [Root, Child]
class ModelTest(unittest.TestCase):
    def tearDown(self):
        for m in MODELS:
            m._default_manager.all().delete()
    
    def test_create(self):
        r = milkman.deliver(Root)
        self.assertEqual(Root, r.__class__)
        self.assertTrue(bool(r.id))
        self.assert_(r.name is not None)

    def test_create_child(self):
        child = milkman.deliver(Child)
        self.assert_(child.root)
    
    def test_optional_relation(self):
        sibling = milkman.deliver(Sibling)
        self.assertEqual(None, sibling.root)
    
    def test_recurs_on_grandchildren(self):
        gc = milkman.deliver(GrandChild)
        self.assertNotEqual(None, gc.parent.root)

    def test_m2m(self):
        aunt = milkman.deliver(Aunt)
        self.assertEquals(1, len(aunt.uncles.all()))
        self.assertEquals(1, len(Uncle.objects.all()))
        self.assertEquals(Uncle.objects.all()[0], aunt.uncles.all()[0])
    

class RandomFieldTest(unittest.TestCase):
    def test_required_field(self):
        root = milkman.deliver(Root)
        assert root.name
        assert isinstance(root.boolean, types.BooleanType)

class FieldTest(unittest.TestCase):
    def test_needs_generated_value(self):
        f = Root._meta.get_field('name')
        assert milkman.needs_generated_value(f)
        self.assert_(not f.has_default())
        self.assertEqual('', f.get_default())

class FieldValueGeneratorTest(unittest.TestCase):
    def test_email_generator(self):
        f = models.EmailField()
        g = email_generator('test', 'fake.com')
        self.assertEquals('test1@fake.com', g(f))
        self.assertEquals('test2@fake.com', g(f))

    def test_random_str(self):
        self.assertEqual(8, len(random_string()))
        self.assertEqual('a' * 8, random_string(chars=['a']))
        class Foo: 
            max_length = 10
        self.assertEqual('a' * 10, random_string(Foo, ['a']))
        
    def test_random_choice_iterator(self):
        self.assertEqual([''],[x for x in random_choice_iterator()])
        self.assertEqual([1],[x for x in random_choice_iterator([1])])
        self.assertEqual(['', ''], [s for s in random_choice_iterator(size=2)])
        self.assertEqual([1, 1], [s for s in random_choice_iterator([1], 2)])
        