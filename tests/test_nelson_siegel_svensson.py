# -*- coding: utf-8 -*-

import unittest
import click
from click.testing import CliRunner

from nelson_siegel_svensson import cli


class TestNelson_siegel_svensson(unittest.TestCase):
    '''Tests for `nelson_siegel_svensson` package.'''

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
