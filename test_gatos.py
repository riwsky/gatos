import unittest
from gatos import *

class TestGato(unittest.TestCase):

    def test_a_buncha_stuff(self):
        expected = [5,4,4]
        actual = [4,3,2,1] | mult | add | swap | dup | where(lambda x: x>3)
        self.assertEqual(expected, actual)

    def test_a_buncha_stuff2(self):
        expected = [4,5]
        actual = ([4,3,2,1] | mult) + [2,3] | add | swap | dup | where(lambda x: x>3)
        self.assertEqual(expected, actual)

    def test_adding(self):
        expected = [4,5]
        actual = [4,3,2,1] | mult + [2,3] | add | swap | dup | where(lambda x: x>3)
        self.assertEqual(expected, actual)

    def test_transform(self):
        starting_stack = [3,4,5,6]
        expected = [5,6,7,8]
        actual = starting_stack | transform(lambda x: x +2)
        self.assertEqual(expected, actual)

    def test_aggregate(self):
        starting_stack = [3,4,5,6]
        expected = [18]
        actual = starting_stack | aggregate(lambda x,y: x+y)
        self.assertEqual(expected, actual)

    def test_rep(self):
        #test its use on non-gatos
        starting_stack = [3,4,5,6]
        expected =  [3,4,5,5,5,5,5,5]
        actual = starting_stack | rep
        self.assertEqual(expected, actual)

    def test_partial(self):
        starting_stack = [3,4,5,6]
        expected =  [3,4,5,18]
        actual = starting_stack | mult.partial(3)
        self.assertEqual(expected, actual)

        #needs to test kwarg stuff
        starting_stack = [3,4,5,6]
        
        @Gato
        def fake_fn(a,b,c):
            print b,c
            return a

        expected = [3,4,6]
        actual = starting_stack | fake_fn.partial(c=77)
        self.assertEqual(expected, actual)

    def test_composition(self):
        starting_stack00 = [3,4,5,6]
        starting_stack01 = [3,4,5,6]
        decomposed_0 = starting_stack00 | mult | add
        composition_0 = mult | add
        composed_0 = starting_stack01 | composition_0
        self.assertEqual(decomposed_0, composed_0)

        starting_stack1 = [3,4,5]
        expected = [3,4,25]
        actual = starting_stack1 | square
        self.assertEqual(expected, actual)
