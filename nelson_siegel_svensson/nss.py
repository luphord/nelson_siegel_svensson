from numbers import Number
from dataclasses import dataclass

import numpy as np
from numpy import exp

EPS = np.finfo(float).eps


@dataclass
class NelsonSiegelSvenssonCurve:
    beta0: float
    beta1: float
    beta2: float
    beta3: float
    tau1: float
    tau2: float

    def zero(self, T):
        beta0 = self.beta0
        beta1 = self.beta1
        beta2 = self.beta2
        beta3 = self.beta3
        tau1 = self.tau1
        tau2 = self.tau2
        if isinstance(T, Number) and T <= 0:
            return beta0 + beta1
        elif isinstance(T, np.ndarray):
            zero_idx = T <= 0
            T[zero_idx] = EPS  # avoid warnings in calculations
        exp_tt1 = exp(-T/tau1)
        exp_tt2 = exp(-T/tau2)
        factor_1 = (1 - exp_tt1) / (T / tau1)
        factor_2 = factor_1 - exp_tt1
        factor_3 = (1 - exp_tt2) / (T / tau2) - exp_tt2
        res = beta0 + beta1*factor_1 + beta2*factor_2 + beta3*factor_3
        if isinstance(T, np.ndarray):
            T[zero_idx] = 0
            res[zero_idx] = beta0 + beta1
        return res

    def __call__(self, T):
        return self.zero(T)
