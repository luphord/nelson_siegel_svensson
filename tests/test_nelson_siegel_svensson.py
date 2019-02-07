#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `nelson_siegel_svensson` package."""


import unittest
from click.testing import CliRunner

from nelson_siegel_svensson import cli


class TestNelson_siegel_svensson(unittest.TestCase):
    """Tests for `nelson_siegel_svensson` package."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'nelson_siegel_svensson.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
