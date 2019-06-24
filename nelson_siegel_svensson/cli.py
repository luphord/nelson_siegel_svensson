# -*- coding: utf-8 -*-

'''Console script for nelson_siegel_svensson.'''
import sys
import click


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
