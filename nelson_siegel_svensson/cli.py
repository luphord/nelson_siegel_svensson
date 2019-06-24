# -*- coding: utf-8 -*-

'''Console script for nelson_siegel_svensson.'''
import sys
import click
import json

import numpy as np

from .ns import NelsonSiegelCurve
from .nss import NelsonSiegelSvenssonCurve


class Curve(click.ParamType):
    '''Parameter type representing a curve (either Nelson-Siegel
       or Nelson-Siegel-Svensson)'''
    name = 'curve'

    def convert(self, value, param, ctx):
        try:
            decoded = json.loads(value)
            if 'beta3' in decoded:
                return NelsonSiegelSvenssonCurve(**decoded)
            else:
                return NelsonSiegelCurve(**decoded)
        except Exception as e:
            self.fail('{} is not a valid curve: {}'.format(value, e),
                      param, ctx)


class FloatArray(click.ParamType):
    '''Parameter type representing an array of floats'''
    name = 'floats'

    def convert(self, value, param, ctx):
        try:
            decoded = json.loads(value)
            return np.array([float(f) for f in decoded])
        except Exception as e:
            self.fail('{} is not a valid array of floats: {}'.format(value, e),
                      param, ctx)


@click.group(name='nelson_siegel_svensson')
def cli_main(args=None):
    '''Commandline interface for nelson_siegel_svensson.'''
    return 0


@click.command(name='calibrate')
def cli_calibrate():
    '''Evaluate a curve at given points'''
    raise NotImplementedError()


@click.command(name='evaluate')
@click.option('-c', '--curve',
              type=Curve(),
              required=True,
              help='Parameters for curve as JSON object.')
@click.option('-t', '--times',
              type=FloatArray(),
              required=True,
              help='Evaluation times as JSON array.')
def cli_evaluate(curve, times):
    '''Evaluate a curve at given points'''
    click.echo(json.dumps(curve(times).tolist()))


@click.command(name='plot')
def cli_plot():
    '''Plot a curve at given points'''
    raise NotImplementedError()


cli_main.add_command(cli_calibrate)
cli_main.add_command(cli_evaluate)
cli_main.add_command(cli_plot)


if __name__ == '__main__':
    sys.exit(cli_main())  # pragma: no cover
