import numpy as np
from numpy.linalg import lstsq
from scipy.optimize import minimize

from .ns import NelsonSiegelCurve


def _assert_same_shape(t, y):
    assert t.shape == y.shape, 'Mismatching shapes of time and values'


def betas_ns_ols(t, y, tau):
    '''Calculate the best-fitting beta-values given tau
       for time-value pairs t and y and return a corresponding
       Nelson-Siegel curve instance.
    '''
    _assert_same_shape(t, y)
    curve = NelsonSiegelCurve(0, 0, 0, tau)
    factors = curve.factor_matrix(t)
    res = lstsq(factors, y, rcond=None)
    beta = res[0]
    return NelsonSiegelCurve(beta[0], beta[1], beta[2], tau), res


def errorfn_ns_ols(tau, t, y):
    '''Sum of squares error function for a Nelson-Siegel model and
       time-value pairs t and y. All betas are obtained by ordinary
       least squares given tau.
    '''
    _assert_same_shape(t, y)
    curve, lstsq_res = betas_ns_ols(t, y, tau)
    return np.sum((curve(t) - y)**2)


def calibrate_ns_ols(t, y, tau0=2.0):
    '''Calibrate a Nelson-Siegel curve to time-value pairs
       t and y, by optimizing tau and chosing all betas
       using ordinary least squares.
    '''
    _assert_same_shape(t, y)
    opt_res = minimize(errorfn_ns_ols, x0=tau0, args=(t, y))
    curve, lstsq_res = betas_ns_ols(t, y, opt_res.x[0])
    return curve, opt_res
