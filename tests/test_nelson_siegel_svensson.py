# -*- coding: utf-8 -*-

import unittest
import json
from dataclasses import asdict

import numpy as np
import click
from click.testing import CliRunner

from nelson_siegel_svensson import cli, NelsonSiegelCurve, \
    NelsonSiegelSvenssonCurve


class TestNelson_siegel_svensson(unittest.TestCase):
    '''Tests for `nelson_siegel_svensson` CLI.'''

    def setUp(self):
        self.y1 = NelsonSiegelCurve(0.017, -0.023, 0.24, 2.2)
        self.y2 = NelsonSiegelSvenssonCurve(0.017, -0.023, 0.24, 0.1, 2.2, 3.1)
        self.runner = CliRunner()

    def test_command_line_interface(self):
        '''Test the CLI.'''
        result = self.runner.invoke(cli.cli_main)
        assert result.exit_code == 0
        help_result = self.runner.invoke(cli.cli_main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    def test_cli_evaluate(self):
        '''Test evaluate CLI.'''
        param = ['evaluate', '-c',
                 '{"beta0": 0.017, "beta1": -0.023, "beta2": 0.24, "tau": 2}',
                 '-t', '[1,2,3]']
        help_result = self.runner.invoke(cli.cli_main, param)
        assert help_result.exit_code == 0
        assert '0.0758359' in help_result.output

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

    def test_float_array_parameters(self):
        '''Test float array parameter.'''
        param = cli.FloatArray()
        self.assertRaises(click.BadParameter, param.convert,
                          value='', param=None, ctx=None)
        self.assertRaises(click.BadParameter, param.convert,
                          value='{"a": 1}', param=None, ctx=None)
        self.assertRaises(click.BadParameter, param.convert,
                          value='["a"]', param=None, ctx=None)
        self.assertEqual(np.array([1.0]),
                         param.convert('[1.0]', None, None))
        self.assertEqual(np.array([1.0]),
                         param.convert('[1]', None, None))
        self.assertEqual([],
                         param.convert('[]', None, None).tolist())
        self.assertTrue((np.array([1.0, 2.0, 3.0]) ==
                         param.convert('[1,   2,3.0]', None, None)).all())
