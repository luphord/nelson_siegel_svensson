import unittest

import numpy as np

from nelson_siegel_svensson import NelsonSiegelSvenssonCurve
from nelson_siegel_svensson.calibrate import betas_nss_ols, errorfn_nss_ols


class TestNelsonSiegelSvenssonCurveCalibration(unittest.TestCase):
    '''Tests for Nelson-Siegel-Svensson curve calibration'''

    def setUp(self):
        self.y = NelsonSiegelSvenssonCurve(0.017, -0.023, 0.24, 0.1, 2.2, 3.1)

    def test_nelson_siegel_svensson_betas_recovery(self):
        '''Test recovery of betas using ordinary least squares
           (given fixed tau1 and tau2)
        '''
        t = np.linspace(0, 30)
        y_target = self.y(t)
        tau = [self.y.tau1, self.y.tau2]
        curve, lstsq_res = betas_nss_ols(tau, t, y_target)
        self.assertAlmostEqual(self.y.beta0, curve.beta0, places=12)
        self.assertAlmostEqual(self.y.beta1, curve.beta1, places=12)
        self.assertAlmostEqual(self.y.beta2, curve.beta2, places=12)
        self.assertAlmostEqual(self.y.beta3, curve.beta3, places=12)

    def test_nelson_siegel_svensson_ols_errorfn_for_correct_tau(self):
        '''Test ols based error function for correct tau'''
        t = np.linspace(0, 30)
        y_target = self.y(t)
        tau = np.array([self.y.tau1, self.y.tau2])
        error = errorfn_nss_ols(tau, t, y_target)
        self.assertAlmostEqual(0.0, error, places=12)
        error2 = errorfn_nss_ols(tau * 1.1, t, y_target)
        self.assertNotAlmostEqual(0.0, error2)
