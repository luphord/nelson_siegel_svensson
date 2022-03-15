# -*- coding: utf-8 -*-

import unittest

import numpy as np

from nelson_siegel_svensson import NelsonSiegelCurve


class TestNelsonSiegelCurveImplementation(unittest.TestCase):
    """Tests for Nelson-Siegel curve implementation."""

    def setUp(self):
        self.y = NelsonSiegelCurve(0.017, -0.023, 0.24, 2.2)

    def test_curve_init(self):
        NelsonSiegelCurve(0, 0, 0, 0)

    def test_nelson_siegel_curve_array_vs_individual(self):
        """Test curve evaluation on array vs individual elements"""
        t = np.linspace(0, 10, 11)
        y_array = self.y(t)
        y_individual = np.array([self.y(t_i) for t_i in t])
        self.assertTrue(
            np.allclose(y_array, y_individual),
            "array valued yields differ from individual ones",
        )

    def test_nelson_siegel_at_0(self):
        """Test curve evaluation at time 0"""
        y = self.y
        y_actual = y(0.0)  # float time
        self.assertEqual(y.beta0 + y.beta1, y_actual)
        y_actual = y(0)  # int time
        self.assertEqual(y.beta0 + y.beta1, y_actual)
        y_actual = y(np.array([0.0]))  # array time
        self.assertEqual(y.beta0 + y.beta1, y_actual[0])

    def test_forward_against_zero_curve(self):
        """Test forward against zero curve implementation by integrating"""
        t = np.linspace(0.001, 25, 500)
        dt = t[1] - t[0]
        y_by_fw_integration = np.cumsum(self.y.forward(t)) * dt / t
        y_actual = self.y(t)
        self.assertTrue(
            np.allclose(y_actual[100:], y_by_fw_integration[100:], atol=1e-3)
        )
        # todo: numerical issue closer to 0?

    def test_factor_matrix(self):
        """Test shape of factor matrix"""
        n = 50
        t = np.linspace(0, 25, n)
        fmat = self.y.factor_matrix(t)
        self.assertEqual((n, 3), fmat.shape)
        self.assertEqual((3,), self.y.factor_matrix(0.123).shape)
