#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nelson_siegel_svensson` package."""


import unittest
from click.testing import CliRunner

import numpy as np

from nelson_siegel_svensson import NelsonSiegelCurve, NelsonSiegelSvenssonCurve
from nelson_siegel_svensson import cli


class TestNelson_siegel_svensson(unittest.TestCase):
    """Tests for `nelson_siegel_svensson` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_curve_init(self):
        NelsonSiegelCurve(0, 0, 0, 0)
        NelsonSiegelSvenssonCurve(0, 0, 0, 0, 0, 0)

    def test_nelson_siegel_curve(self):
        y = NelsonSiegelCurve(0.017, -0.023, 0.24, 2.2)
        print(y(0), y(1), y(2), y(3))
        t = np.linspace(0, 10, 11)
        print(y(t))

    def test_nelson_siegel_svensson_curve(self):
        y = NelsonSiegelSvenssonCurve(0.017, -0.023, 0.24, 0.1, 2.2, 3.1)
        print(y(0), y(1), y(2), y(3))
        t = np.linspace(0, 10, 11)
        print(y(t))

    def test_mithril_parameters(self):
        y = NelsonSiegelSvenssonCurve(0.04, -0.03, -0.02, -0.02, 2.1, 1.04)
        y_expected = np.array([0.38, 0.63, 1.65, 2.58, 3.32]) / 100
        y_actual = [y(1), y(2), y(5), y(10), y(25)]
        print(y_expected)
        print(y_actual)
        # ToDo: they do not match. why?

    def test_ecb_2016_01_04_parameters(self):
        y = NelsonSiegelSvenssonCurve(2.142562216, -2.649562216,
                                      19.9532384206, -24.0677865973,
                                      1.6568604918, 1.8145254889)
        y_expected = np.array([-0.410613, -0.366505, -0.290997, -0.174151,
                               -0.028807, 0.129236, 0.287602, 0.438365,
                               0.577291, 0.702713, 0.814554, 0.913619,
                               1.001124, 1.078417, 1.146814, 1.207524,
                               1.261617, 1.310018, 1.353515, 1.392777,
                               1.428369, 1.460766, 1.490370, 1.517522,
                               1.542510, 1.565581, 1.586946, 1.606787,
                               1.625260, 1.642502])
        y_actual = y(np.arange(1, 31))
        print(y_expected)
        print(y_actual)
        # ToDo: they do not match. why?

    def test_gilli_grosse_schumann_parameters(self):
        '''Test parameters from Gilli, Grosse, Schumann paper (Table 1)'''
        y = NelsonSiegelSvenssonCurve(2.05, -1.82, -2.03, 8.25, 0.87, 14.38)
        t = np.array([1/4, 1/2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30])
        y_expected = np.array([0.3, 0.4, 0.68, 1.27, 1.78, 2.2, 2.53, 2.8,
                               3.03, 3.23, 3.4, 3.54, 4.04, 4.28, 4.38, 4.38])
        y_actual = y(t).round(2)
        self.assertTrue(np.allclose(y_expected, y_actual),
                        'calculated yields differ from expected ones')

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'nelson_siegel_svensson.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
