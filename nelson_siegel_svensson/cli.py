# -*- coding: utf-8 -*-

'''Console script for nelson_siegel_svensson.'''
import sys
import click
import json

from .ns import NelsonSiegelCurve
from .nss import NelsonSiegelSvenssonCurve


class Curve(click.ParamType):
    '''Parameter type representing a curve (either Nelson-Siegel
       or Nelson-Siegel-Svensson)'''
    name = 'ratio'

    def convert(self, value, param, ctx):
        try:
            decoded = json.loads(value)
            if 'beta3' in decoded:
                return NelsonSiegelSvenssonCurve(**decoded)
            else:
                return NelsonSiegelCurve(**decoded)
        except Exception:
            self.fail('{} is not a valid curve'.format(value), param, ctx)


@click.group(name='nelson_siegel_svensson')
def cli_main(args=None):
    '''Commandline interface for nelson_siegel_svensson.'''
    return 0


@click.command(name='calibrate')
def cli_calibrate(file):
    '''Evaluate a curve at given points'''
    raise NotImplementedError()


@click.command(name='evaluate')
def cli_evaluate(file):
    '''Evaluate a curve at given points'''
    raise NotImplementedError()


@click.command(name='plot')
def cli_plot(file):
    '''Plot a curve at given points'''
    raise NotImplementedError()


cli_main.add_command(cli_calibrate)
cli_main.add_command(cli_evaluate)
cli_main.add_command(cli_plot)


if __name__ == '__main__':
    sys.exit(cli_main())  # pragma: no cover
