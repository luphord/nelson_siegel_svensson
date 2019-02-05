from numbers import Number
from dataclasses import dataclass

import numpy as np
from numpy import exp

EPS = np.finfo(float).eps


@dataclass
class NelsonSiegelCurve:
    beta1: float
    beta2: float
    beta3: float
    tau: float

    def factors(self, T):
        tau = self.tau
        if isinstance(T, Number) and T <= 0:
            return 1, 0
        elif isinstance(T, np.ndarray):
            zero_idx = T <= 0
            T[zero_idx] = EPS  # avoid warnings in calculations
        exp_tt0 = exp(-T/tau)
        factor_2 = (1 - exp_tt0) / (T / tau)
        factor_3 = factor_2 - exp_tt0
        if isinstance(T, np.ndarray):
            T[zero_idx] = 0
            factor_2[zero_idx] = 1
            factor_3[zero_idx] = 0
        return factor_2, factor_3

    def zero(self, T):
        factor_2, factor_3 = self.factors(T)
        return self.beta1 + self.beta2*factor_2 + self.beta3*factor_3

    def __call__(self, T):
        return self.zero(T)
