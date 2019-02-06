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

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'nelson_siegel_svensson.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
