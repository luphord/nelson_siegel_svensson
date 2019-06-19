============================
Nelson-Siegel-Svensson Model
============================


.. image:: https://img.shields.io/pypi/v/nelson_siegel_svensson.svg
        :target: https://pypi.python.org/pypi/nelson_siegel_svensson

.. image:: https://img.shields.io/travis/luphord/nelson_siegel_svensson.svg
        :target: https://travis-ci.org/luphord/nelson_siegel_svensson

.. image:: https://readthedocs.org/projects/nelson-siegel-svensson/badge/?version=latest
        :target: https://nelson-siegel-svensson.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Implementation of the Nelson-Siegel-Svensson interest rate curve model in Python.

.. code-block:: python

        from nelson_siegel_svensson import NelsonSiegelSvenssonCurve
        import numpy as np
        from matplotlib.pyplot import plot

        y = NelsonSiegelSvenssonCurve(0.028, -0.03, -0.04, -0.015, 1.1, 4.0)
        t = np.linspace(0, 20, 100)
        plot(t, y(t))

.. image:: docs/_static/an_example_nelson-siegel-svensson-curve.png

* Free software: MIT license
* Documentation: https://nelson-siegel-svensson.readthedocs.io.


Features
--------

* Python implementation of the Nelson-Siegel curve (three factors)
* Python implementation of the Nelson-Siegel-Svensson curve (four factors)
* Methods for zero and forward rates (as vectorized functions of time points)
* Methods for the factors (as vectorized function of time points)
* Calibration based on ordinary least squares (OLS) for betas and nonlinear optimization for taus

Credits
-------

Main developer is luphord_.

.. _luphord: https://github.com/luphord

This package was prepared with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
