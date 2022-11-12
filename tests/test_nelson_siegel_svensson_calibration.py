# -*- coding: utf-8 -*-

import unittest

import numpy as np
from scipy.optimize import minimize

from nelson_siegel_svensson import NelsonSiegelSvenssonCurve
from nelson_siegel_svensson.calibrate import (
    betas_nss_ols,
    errorfn_nss_ols,
    calibrate_nss_ols,
)


class TestNelsonSiegelSvenssonCurveCalibration(unittest.TestCase):
    """Tests for Nelson-Siegel-Svensson curve calibration."""

    def setUp(self):
        self.y = NelsonSiegelSvenssonCurve(0.017, -0.023, 0.24, 0.1, 2.2, 3.1)

    def test_nelson_siegel_svensson_betas_recovery(self):
        """Test recovery of betas using ordinary least squares
        (given fixed tau1 and tau2).
        """
        t = np.linspace(0, 30)
        y_target = self.y(t)
        tau = [self.y.tau1, self.y.tau2]
        curve, lstsq_res = betas_nss_ols(tau, t, y_target)
        self.assertAlmostEqual(self.y.beta0, curve.beta0, places=12)
        self.assertAlmostEqual(self.y.beta1, curve.beta1, places=12)
        self.assertAlmostEqual(self.y.beta2, curve.beta2, places=12)
        self.assertAlmostEqual(self.y.beta3, curve.beta3, places=12)

    def test_nelson_siegel_svensson_ols_errorfn_for_correct_tau(self):
        """Test ols based error function for correct tau."""
        t = np.linspace(0, 30)
        y_target = self.y(t)
        tau = np.array([self.y.tau1, self.y.tau2])
        error = errorfn_nss_ols(tau, t, y_target)
        self.assertAlmostEqual(0.0, error, places=12)
        error2 = errorfn_nss_ols(tau * 1.1, t, y_target)
        self.assertNotAlmostEqual(0.0, error2)

    def test_nelson_siegel_svensson_ols_calibration(self):
        """Test ols based calibration of Nelson-Siegel-Svensson model."""
        t = np.linspace(0, 30)
        y_target = self.y(t)
        tau0 = np.array([self.y.tau1, self.y.tau2])
        y_hat, opt_res = calibrate_nss_ols(t, y_target, tau0=tau0)
        places = 12
        self.assertAlmostEqual(self.y.beta0, y_hat.beta0, places=places)
        self.assertAlmostEqual(self.y.beta1, y_hat.beta1, places=places)
        self.assertAlmostEqual(self.y.beta2, y_hat.beta2, places=places)
        self.assertAlmostEqual(self.y.beta3, y_hat.beta3, places=places)
        self.assertAlmostEqual(self.y.tau1, y_hat.tau1, places=places)
        self.assertAlmostEqual(self.y.tau2, y_hat.tau2, places=places)
        # Not using the true values for tau1/2 as starting values
        # turns optimization results bad fairly quick
        # just 1% deviation and we only get two places accuracy
        tau0 = np.array([self.y.tau1 * 0.99, self.y.tau2 * 1.01])
        places_beta = 2
        places_tau = 1
        y_hat, opt_res = calibrate_nss_ols(t, y_target, tau0=tau0)
        self.assertAlmostEqual(self.y.beta0, y_hat.beta0, places=places_beta)
        self.assertAlmostEqual(self.y.beta1, y_hat.beta1, places=places_beta)
        self.assertAlmostEqual(self.y.beta2, y_hat.beta2, places=places_beta)
        self.assertAlmostEqual(self.y.beta3, y_hat.beta3, places=places_beta)
        self.assertAlmostEqual(self.y.tau1, y_hat.tau1, places=places_tau)
        self.assertAlmostEqual(self.y.tau2, y_hat.tau2, places=places_tau)

    def test_nelson_siegel_svensson_inverted_tau_starting_values(self):
        """Test the effect of inverting the starting values for tau1/2
        on calibration."""
        t = np.linspace(0, 30)
        y_target = self.y(t)
        tau0 = (0.5, 2)
        tau_hat_1 = minimize(errorfn_nss_ols, x0=tau0, args=(t, y_target)).x
        tau_hat_2 = minimize(errorfn_nss_ols, x0=tau0[::-1], args=(t, y_target)).x
        self.assertLess(tau_hat_1[0], tau_hat_1[1])
        self.assertGreater(tau_hat_2[0], tau_hat_2[1])
