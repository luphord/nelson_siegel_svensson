# -*- coding: utf-8 -*-

"""Console script for nelson_siegel_svensson."""
import sys
import click
import json

import numpy as np
from matplotlib import pyplot as plt

from .ns import NelsonSiegelCurve
from .nss import NelsonSiegelSvenssonCurve
from .calibrate import calibrate_ns_ols, calibrate_nss_ols


class Curve(click.ParamType):
    """Parameter type representing a curve (either Nelson-Siegel
    or Nelson-Siegel-Svensson)"""

    name = "curve"

    def convert(self, value, param, ctx):
        try:
            decoded = json.loads(value)
            if "beta3" in decoded:
                return NelsonSiegelSvenssonCurve(**decoded)
            else:
                return NelsonSiegelCurve(**decoded)
        except Exception as e:
            self.fail("{} is not a valid curve: {}".format(value, e), param, ctx)


class FloatArray(click.ParamType):
    """Parameter type representing an array of floats"""

    name = "floats"

    def convert(self, value, param, ctx):
        try:
            decoded = json.loads(value)
            return np.array([float(f) for f in decoded])
        except Exception as e:
            self.fail(
                "{} is not a valid array of floats: {}".format(value, e), param, ctx
            )


@click.group(name="nelson_siegel_svensson")
def cli_main(args=None):
    """Commandline interface for nelson_siegel_svensson."""
    return 0


@click.command(name="calibrate")
@click.option(
    "-t", "--times", type=FloatArray(), required=True, help="time points as JSON array."
)
@click.option(
    "-y",
    "--values",
    type=FloatArray(),
    required=True,
    help="values corresponding to time points as JSON array.",
)
@click.option(
    "--nelson-siegel-svensson/--nelson-siegel",
    default=True,
    help="whether to calibrate a Nelson-Siegel-Svensson (4 factor)"
    + " or a Nelson-Siegel (3 factor) curve. Defaults to"
    + " the former.",
)
@click.option(
    "--initial-tau1",
    type=click.FLOAT,
    default=2.0,
    show_default=True,
    help="Initial value of tau1 (or tau for Nelson-Siegel) " + "for optimization.",
)
@click.option(
    "--initial-tau2",
    type=click.FLOAT,
    default=5.0,
    show_default=True,
    help="Initial value of tau2 (ignored by Nelson-Siegel) " + "for optimization.",
)
def cli_calibrate(times, values, nelson_siegel_svensson, initial_tau1, initial_tau2):
    """Calibrate a curve to the given data points."""
    if nelson_siegel_svensson:
        curve, status = calibrate_nss_ols(times, values, (initial_tau1, initial_tau2))
    else:
        curve, status = calibrate_ns_ols(times, values, initial_tau1)
    assert status.success
    click.echo(json.dumps(vars(curve)))


@click.command(name="evaluate")
@click.option(
    "-c",
    "--curve",
    type=Curve(),
    required=True,
    help="Parameters for curve as JSON object.",
)
@click.option(
    "-t",
    "--times",
    type=FloatArray(),
    required=True,
    help="Evaluation times as JSON array.",
)
def cli_evaluate(curve, times):
    """Evaluate a curve at given points."""
    click.echo(json.dumps(curve(times).tolist()))


@click.command(name="plot")
@click.option(
    "-c",
    "--curves",
    type=Curve(),
    required=True,
    multiple=True,
    help="Parameters for curve as JSON object; " + "accepts multiple curves.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(file_okay=True, dir_okay=False, writable=True, resolve_path=True),
    required=True,
    help="Output file for the plot.",
)
@click.option(
    "-f",
    "--from-time",
    type=click.FLOAT,
    default=0.0,
    show_default=True,
    help="Left time point of the plot.",
)
@click.option(
    "-t",
    "--to-time",
    type=click.FLOAT,
    default=30.0,
    show_default=True,
    help="Right time point of the plot.",
)
def cli_plot(curves, output, from_time, to_time):
    """Plot a curve at given points."""
    fig, ax = plt.subplots(nrows=1, ncols=1)
    t = np.linspace(from_time, to_time, num=100)
    for curve in curves:
        y = curve(t)
        ax.plot(t, y)
    fig.savefig(output)
    plt.close(fig)


cli_main.add_command(cli_calibrate)
cli_main.add_command(cli_evaluate)
cli_main.add_command(cli_plot)


if __name__ == "__main__":
    sys.exit(cli_main())  # pragma: no cover
