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




Implementation of the Nelson-Siegel-Svensson interest rate curve model.

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

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
