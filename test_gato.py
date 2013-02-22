import unittest2 as unittest
from gato import *

class TestGato(unittest.TestCase):

    def test_a_buncha_stuff(self):
        expected = [5,4,4]
        actual = [4,3,2,1] | mult | add | swap | dup | where(lambda x: x>3)
        self.assertEqual(expected, actual)

    def test_a_buncha_stuff2(self):
        expected = [4,5]
        actual = ([4,3,2,1] | mult) + [2,3] | add | swap | dup | where(lambda x: x>3)
        self.assertEqual(expected, actual)

    def test_composition(self):
        starting_stack00 = [3,4,5,6]
        starting_stack01 = [3,4,5,6]
        decomposed_0 = starting_stack00 | mult | add
        composition_0 = mult | add
        composed_0 = starting_stack01 | composition_0
        self.assertEqual(decomposed_0, composed_0)
