# -*- coding: utf-8 -*-

'''Implementation of the Nelson-Siegel-Svensson interest rate curve model.
For details, see classes `NelsonSiegelCurve` and `NelsonSiegelSvenssonCurve`.
'''

__author__ = '''luphord'''
__email__ = 'luphord@protonmail.com'
__version__ = '0.4.1'

from .ns import NelsonSiegelCurve
from .nss import NelsonSiegelSvenssonCurve

__all__ = ['NelsonSiegelCurve', 'NelsonSiegelSvenssonCurve']
