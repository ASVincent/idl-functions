#!/usr/bin/env python

from __future__ import absolute_import
import sys
import os
import unittest
import numpy

# Need to temporarily append to the PYTHONPATH in order to import the 
# newly built array_indices function
sys.path.append(os.getcwd())
from idl_functions import array_indices


class IDL_array_indices_Tester(unittest.TestCase):

    """
    A unit testing procedure for the IDL array_indices function.
    """

    def setUp(self):
        self.array_1D_1 = numpy.random.randint(0,256,(10000))
        self.array_1D_2 = numpy.random.randint(0,256,(30000))
        self.array_2D = self.array_1D_1.reshape(100,100)
        self.array_3D = self.array_1D_2.reshape((3,100,100))

    def test_2D_indices_row(self):
        """
        The returned 2D index should be the same as control.
        """
        control = numpy.where(self.array_2D == 66)
        wh = numpy.where(self.array_1D_1 == 66)
        ind2D = array_indices(array=self.array_2D, index=wh[0])
        n = len(control[0])
        self.assertEqual((control[0] == ind2D[0]).sum(), n)

    def test_2D_indices_col(self):
        """
        The returned 2D index should be the same as control.
        """
        control = numpy.where(self.array_2D == 66)
        wh = numpy.where(self.array_1D_1 == 66)
        ind2D = array_indices(array=self.array_2D, index=wh[0])
        n = len(control[1])
        self.assertEqual((control[1] == ind2D[1]).sum(), n)

    def test_dimensions(self):
        """
        Test that the dimensions keyword works and yields the same
        result as the control.
        """
        control = numpy.where(self.array_3D == 66)
        control_sum = numpy.sum(self.array_3D[control])
        wh = numpy.where(self.array_1D_2 == 66)
        ind3D = array_indices(array=self.array_3D.shape, index=wh[0],
                              dimensions=True)
        test_sum = numpy.sum(self.array_3D[ind3D])
        self.assertEqual(control_sum, test_sum)

    def test_index_type(self):
        """
        Test that index type of not ndarray or scalar raises an error.
        """
        index = [5]
        self.assertRaises(TypeError, array_indices, self.array_2D, index)

    def test_index_out_of_bounds_lower(self):
        """
        Test that an index outside the array bounds raises an error.
        """
        index = -5
        self.assertRaises(IndexError, array_indices, self.array_2D, index)

    def test_index_out_of_bounds_upper(self):
        """
        Test that an index outside the array bounds raises an error.
        """
        index = 10001
        self.assertRaises(IndexError, array_indices, self.array_2D, index)

if __name__ == '__main__':
    unittest.main()
