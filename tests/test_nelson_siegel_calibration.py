# -*- coding: utf-8 -*-

import unittest

import numpy as np
from scipy.optimize import minimize

from nelson_siegel_svensson import NelsonSiegelCurve
from nelson_siegel_svensson.calibrate import (
    betas_ns_ols,
    errorfn_ns_ols,
    calibrate_ns_ols,
)


class TestNelsonSiegelCurveCalibration(unittest.TestCase):
    """Tests for Nelson-Siegel curve calibration."""

    def setUp(self):
        self.y = NelsonSiegelCurve(0.017, -0.023, 0.24, 2.2)

    def test_nelson_siegel_betas_recovery(self):
        """Test recovery of betas using ordinary least squares
        (given fixed tau).
        """
        t = np.linspace(0, 30)
        y_target = self.y(t)
        curve, lstsq_res = betas_ns_ols(self.y.tau, t, y_target)
        self.assertAlmostEqual(self.y.beta0, curve.beta0, places=12)
        self.assertAlmostEqual(self.y.beta1, curve.beta1, places=12)
        self.assertAlmostEqual(self.y.beta2, curve.beta2, places=12)

    def test_nelson_siegel_ols_errorfn_for_correct_tau(self):
        """Test ols based error function for correct tau."""
        t = np.linspace(0, 30)
        y_target = self.y(t)
        error = errorfn_ns_ols(self.y.tau, t, y_target)
        self.assertAlmostEqual(0.0, error, places=12)
        error2 = errorfn_ns_ols(self.y.tau * 1.1, t, y_target)
        self.assertNotAlmostEqual(0.0, error2)

    def test_nelson_siegel_ols_calibration(self):
        """Test ols based calibration of Nelson-Siegel model."""
        t = np.linspace(0, 30)
        y_target = self.y(t)
        y_hat, opt_res = calibrate_ns_ols(t, y_target, tau0=self.y.tau)
        places = 12
        self.assertAlmostEqual(self.y.beta0, y_hat.beta0, places=places)
        self.assertAlmostEqual(self.y.beta1, y_hat.beta1, places=places)
        self.assertAlmostEqual(self.y.beta2, y_hat.beta2, places=places)
        self.assertAlmostEqual(self.y.tau, y_hat.tau, places=places)
        # The following does not work in general, but in this case the
        # error function (of tau) is well-behaving
        places_beta = 3
        places_tau = 2
        y_hat, opt_res = calibrate_ns_ols(t, y_target)  # default start value
        self.assertAlmostEqual(self.y.beta0, y_hat.beta0, places=places_beta)
        self.assertAlmostEqual(self.y.beta1, y_hat.beta1, places=places_beta)
        self.assertAlmostEqual(self.y.beta2, y_hat.beta2, places=places_beta)
        self.assertAlmostEqual(self.y.tau, y_hat.tau, places=places_tau)
        y_hat, opt_res = calibrate_ns_ols(t, y_target, tau0=0.5)
        self.assertAlmostEqual(self.y.beta0, y_hat.beta0, places=places_beta)
        self.assertAlmostEqual(self.y.beta1, y_hat.beta1, places=places_beta)
        self.assertAlmostEqual(self.y.beta2, y_hat.beta2, places=places_beta)
        self.assertAlmostEqual(self.y.tau, y_hat.tau, places=places_tau)
        y_hat, opt_res = calibrate_ns_ols(t, y_target, tau0=5)
        self.assertAlmostEqual(self.y.beta0, y_hat.beta0, places=places_beta)
        self.assertAlmostEqual(self.y.beta1, y_hat.beta1, places=places_beta)
        self.assertAlmostEqual(self.y.beta2, y_hat.beta2, places=places_beta)
        self.assertAlmostEqual(self.y.tau, y_hat.tau, places=places_tau)
        y_hat, opt_res = calibrate_ns_ols(t, y_target, tau0=10)
        self.assertAlmostEqual(self.y.beta0, y_hat.beta0, places=places_beta)
        self.assertAlmostEqual(self.y.beta1, y_hat.beta1, places=places_beta)
        self.assertAlmostEqual(self.y.beta2, y_hat.beta2, places=places_beta)
        self.assertAlmostEqual(self.y.tau, y_hat.tau, places=places_tau)
        y_hat, opt_res = calibrate_ns_ols(t, y_target, tau0=20)
        self.assertAlmostEqual(self.y.beta0, y_hat.beta0, places=places_beta)
        self.assertAlmostEqual(self.y.beta1, y_hat.beta1, places=places_beta)
        self.assertAlmostEqual(self.y.beta2, y_hat.beta2, places=places_beta)
        self.assertAlmostEqual(self.y.tau, y_hat.tau, places=places_tau)

    def test_nelson_siegel_ols_constrained_calibration(self):
        """Test ols based calibration with constrained optimization of tau
        of Nelson-Siegel model."""
        t = np.linspace(0, 30)
        y_target = self.y(t)
        tau0_grid = (0.08, 0.1, 0.2, 0.5, 1, 2, 3, 4, 5)
        places_tau = 2
        # unconstrained
        for tau0 in tau0_grid:
            opt_res = minimize(errorfn_ns_ols, x0=tau0, args=(t, y_target))
            self.assertAlmostEqual(self.y.tau, opt_res.x[0], places=places_tau)
        # constrained
        for tau0 in tau0_grid:
            opt_res = minimize(
                errorfn_ns_ols, x0=tau0, args=(t, y_target), bounds=((0.08, None),)
            )
            self.assertAlmostEqual(self.y.tau, opt_res.x[0], places=places_tau)
