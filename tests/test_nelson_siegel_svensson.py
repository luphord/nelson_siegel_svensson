# -*- coding: utf-8 -*-

import unittest
import json
from dataclasses import asdict
import click
from click.testing import CliRunner

from nelson_siegel_svensson import cli, NelsonSiegelCurve, \
    NelsonSiegelSvenssonCurve


class TestNelson_siegel_svensson(unittest.TestCase):
    '''Tests for `nelson_siegel_svensson` CLI.'''

    def setUp(self):
        self.y1 = NelsonSiegelCurve(0.017, -0.023, 0.24, 2.2)
        self.y2 = NelsonSiegelSvenssonCurve(0.017, -0.023, 0.24, 0.1, 2.2, 3.1)

    def test_command_line_interface(self):
        '''Test the CLI.'''
        runner = CliRunner()
        result = runner.invoke(cli.cli_main)
        assert result.exit_code == 0
        help_result = runner.invoke(cli.cli_main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    def test_curve_parameters(self):
        '''Test curve parameter.'''
        param = cli.Curve()
        self.assertRaises(click.BadParameter, param.convert,
                          value='', param=None, ctx=None)
        self.assertRaises(click.BadParameter, param.convert,
                          value='{}', param=None, ctx=None)
        missing_tau = '{"beta0": 0.017, "beta1": -0.023, "beta2": 0.24}'
        self.assertRaises(click.BadParameter, param.convert,
                          value=missing_tau, param=None, ctx=None)
        self.assertEqual(self.y1,
                         param.convert(json.dumps(asdict(self.y1)),
                                       None, None))
        self.assertEqual(self.y2,
                         param.convert(json.dumps(asdict(self.y2)),
                                       None, None))
