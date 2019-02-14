import unittest

import numpy as np

from nelson_siegel_svensson import NelsonSiegelCurve
from nelson_siegel_svensson.calibrate import betas_ns_ols


class TestNelsonSiegelCurveCalibration(unittest.TestCase):
    '''Tests for Nelson-Siegel curve calibration'''

    def setUp(self):
        self.y = NelsonSiegelCurve(0.017, -0.023, 0.24, 2.2)

    def test_nelson_siegel_betas_recovery(self):
        '''Test recovery of betas using ordinary least squares
           (given fixed tau)
        '''
        t = np.linspace(0, 30)
        y_target = self.y(t)
        curve, lstsq_res = betas_ns_ols(self.y.tau, t, y_target)
        self.assertAlmostEqual(self.y.beta0, curve.beta0, places=12)
        self.assertAlmostEqual(self.y.beta1, curve.beta1, places=12)
        self.assertAlmostEqual(self.y.beta2, curve.beta2, places=12)
