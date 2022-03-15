# -*- coding: utf-8 -*-

import unittest
import os
import json
from dataclasses import asdict

import numpy as np
import click
from click.testing import CliRunner

from nelson_siegel_svensson import cli, NelsonSiegelCurve, NelsonSiegelSvenssonCurve


class TestNelson_siegel_svensson(unittest.TestCase):
    """Tests for `nelson_siegel_svensson` CLI."""

    def setUp(self):
        self.y1 = NelsonSiegelCurve(0.017, -0.023, 0.24, 2.2)
        self.y2 = NelsonSiegelSvenssonCurve(0.017, -0.023, 0.24, 0.1, 2.2, 3.1)
        self.t = [0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0]
        self.y = [
            0.01,
            0.011,
            0.013,
            0.016,
            0.019,
            0.021,
            0.026,
            0.03,
            0.035,
            0.037,
            0.038,
            0.04,
        ]
        self.runner = CliRunner()

    def test_command_line_interface(self):
        """Test the CLI."""
        result = self.runner.invoke(cli.cli_main)
        self.assertEqual(0, result.exit_code)
        help_result = self.runner.invoke(cli.cli_main, ["--help"])
        self.assertEqual(0, help_result.exit_code)
        self.assertIn("--help  Show this message and exit.", help_result.output)

    def test_cli_evaluate(self):
        """Test evaluate CLI."""
        param = [
            "evaluate",
            "-c",
            '{"beta0": 0.017, "beta1": -0.023, "beta2": 0.24, "tau": 2}',
            "-t",
            "[1,2,3]",
        ]
        result = self.runner.invoke(cli.cli_main, param)
        self.assertEqual(0, result.exit_code)
        self.assertIn("0.0758359", result.output)

    def test_cli_calibrate(self):
        """Test calibrate CLI."""
        param = ["calibrate", "-t", json.dumps(self.t), "-y", json.dumps(self.y)]
        result = self.runner.invoke(cli.cli_main, param)
        self.assertEqual(0, result.exit_code)
        self.assertIn("0.0451", result.output)
        first_output = result.output
        result = self.runner.invoke(cli.cli_main, param + ["--nelson-siegel-svensson"])
        self.assertEqual(0, result.exit_code)
        self.assertEqual(first_output, result.output)
        result = self.runner.invoke(cli.cli_main, param + ["--nelson-siegel"])
        self.assertEqual(0, result.exit_code)
        self.assertIn("0.0425", result.output)
        result = self.runner.invoke(
            cli.cli_main, param + ["--nelson-siegel", "--initial-tau1", "1.234"]
        )
        self.assertEqual(0, result.exit_code)
        self.assertIn("0.04179", result.output)

    def test_cli_plot(self):
        """Test plot CLI."""
        fname = "output.png"
        param = [
            "plot",
            "-o",
            fname,
            "-c",
            '{"beta0": 0.017, "beta1": -0.023, "beta2": 0.24, "tau": 2}',
        ]
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli.cli_main, param)
            self.assertEqual(0, result.exit_code)
            self.assertTrue(os.path.exists(fname), fname + " missing")
            result = self.runner.invoke(cli.cli_main, param + ["-f", "10", "-t", "20"])
            self.assertEqual(0, result.exit_code)
            self.assertTrue(os.path.exists(fname), fname + " missing")

    def test_curve_parameters(self):
        """Test curve parameter."""
        param = cli.Curve()
        self.assertRaises(
            click.BadParameter, param.convert, value="", param=None, ctx=None
        )
        self.assertRaises(
            click.BadParameter, param.convert, value="{}", param=None, ctx=None
        )
        missing_tau = '{"beta0": 0.017, "beta1": -0.023, "beta2": 0.24}'
        self.assertRaises(
            click.BadParameter, param.convert, value=missing_tau, param=None, ctx=None
        )
        self.assertEqual(
            self.y1, param.convert(json.dumps(asdict(self.y1)), None, None)
        )
        self.assertEqual(
            self.y2, param.convert(json.dumps(asdict(self.y2)), None, None)
        )

    def test_float_array_parameters(self):
        """Test float array parameter."""
        param = cli.FloatArray()
        self.assertRaises(
            click.BadParameter, param.convert, value="", param=None, ctx=None
        )
        self.assertRaises(
            click.BadParameter, param.convert, value='{"a": 1}', param=None, ctx=None
        )
        self.assertRaises(
            click.BadParameter, param.convert, value='["a"]', param=None, ctx=None
        )
        self.assertEqual(np.array([1.0]), param.convert("[1.0]", None, None))
        self.assertEqual(np.array([1.0]), param.convert("[1]", None, None))
        self.assertEqual([], param.convert("[]", None, None).tolist())
        self.assertTrue(
            (
                np.array([1.0, 2.0, 3.0]) == param.convert("[1,   2,3.0]", None, None)
            ).all()
        )
