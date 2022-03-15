# -*- coding: utf-8 -*-

import unittest

import numpy as np

from nelson_siegel_svensson import NelsonSiegelSvenssonCurve


class TestNelsonSiegelSvenssonCurveImplementation(unittest.TestCase):
    """Tests for Nelson-Siegel-Svensson curve implementation."""

    def setUp(self):
        self.y = NelsonSiegelSvenssonCurve(0.017, -0.023, 0.24, 0.1, 2.2, 3.1)

    def test_curve_init(self):
        NelsonSiegelSvenssonCurve(0, 0, 0, 0, 0, 0)

    def test_nelson_siegel_svensson_curve_array_vs_individual(self):
        """Test curve evaluation on array vs individual elements."""
        y = self.y
        t = np.linspace(0, 10, 11)
        y_array = y(t)
        y_individual = np.array([y(t_i) for t_i in t])
        self.assertTrue(
            np.allclose(y_array, y_individual),
            "array valued yields differ from individual ones",
        )

    def test_nelson_siegel_svensson_at_0(self):
        """Test curve evaluation at time 0."""
        y = self.y
        y_actual = y(0.0)  # float time
        self.assertEqual(y.beta0 + y.beta1, y_actual)
        y_actual = y(0)  # int time
        self.assertEqual(y.beta0 + y.beta1, y_actual)
        y_actual = y(np.array([0.0]))  # array time
        self.assertEqual(y.beta0 + y.beta1, y_actual[0])

    def test_mithril_parameters(self):
        y = NelsonSiegelSvenssonCurve(0.038, -0.032, -0.019, -0.02, 2.1, 1.04)
        y_expected = np.array([0.38, 0.63, 1.65, 2.58, 3.32]) / 100
        y_actual = np.array([y(1), y(2), y(5), y(10), y(25)]).round(4)
        self.assertTrue(
            np.allclose(y_expected, y_actual, atol=5e-4),
            "calculated yields differ from expected ones",
        )

    def test_ecb_2016_01_04_parameters(self):
        """Test curve evaluation for ECB AAA curve parameters on 2016-01-04."""
        y = NelsonSiegelSvenssonCurve(
            2.142562216,
            -2.649562216,
            19.9532384206,
            -24.0677865973,
            1.6568604918,
            1.8145254889,
        )
        y_expected = np.array(
            [
                -0.410613,
                -0.366505,
                -0.290997,
                -0.174151,
                -0.028807,
                0.129236,
                0.287602,
                0.438365,
                0.577291,
                0.702713,
                0.814554,
                0.913619,
                1.001124,
                1.078417,
                1.146814,
                1.207524,
                1.261617,
                1.310018,
                1.353515,
                1.392777,
                1.428369,
                1.460766,
                1.490370,
                1.517522,
                1.542510,
                1.565581,
                1.586946,
                1.606787,
                1.625260,
                1.642502,
            ]
        )
        y_actual = y(np.arange(1, 31)).round(6)
        self.assertTrue(
            np.allclose(y_expected, y_actual),
            "calculated yields differ from expected ones",
        )

    def test_gilli_grosse_schumann_parameters(self):
        """Test parameters from Gilli, Grosse, Schumann paper (Table 1)."""
        y = NelsonSiegelSvenssonCurve(2.05, -1.82, -2.03, 8.25, 0.87, 14.38)
        t = np.array([1 / 4, 1 / 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30])
        y_expected = np.array(
            [
                0.3,
                0.4,
                0.68,
                1.27,
                1.78,
                2.2,
                2.53,
                2.8,
                3.03,
                3.23,
                3.4,
                3.54,
                4.04,
                4.28,
                4.38,
                4.38,
            ]
        )
        y_actual = y(t).round(2)
        self.assertTrue(
            np.allclose(y_expected, y_actual),
            "calculated yields differ from expected ones",
        )

    def test_forward_against_zero_curve(self):
        """Test forward against zero curve implementation by integrating."""
        t = np.linspace(0.001, 25, 500)
        dt = t[1] - t[0]
        y_by_fw_integration = np.cumsum(self.y.forward(t)) * dt / t
        y_actual = self.y(t)
        self.assertTrue(
            np.allclose(y_actual[100:], y_by_fw_integration[100:], atol=1e-3)
        )
        # todo: numerical issue closer to 0?

    def test_factor_matrix(self):
        """Test shape of factor matrix."""
        n = 50
        t = np.linspace(0, 25, n)
        fmat = self.y.factor_matrix(t)
        self.assertEqual((n, 4), fmat.shape)
        self.assertEqual((4,), self.y.factor_matrix(0.123).shape)
