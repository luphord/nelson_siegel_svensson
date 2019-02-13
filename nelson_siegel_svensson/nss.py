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

    def factors(self, T):
        tau1 = self.tau1
        tau2 = self.tau2
        if isinstance(T, Number) and T <= 0:
            return 1, 0, 0
        elif isinstance(T, np.ndarray):
            zero_idx = T <= 0
            T[zero_idx] = EPS  # avoid warnings in calculations
        exp_tt1 = exp(-T/tau1)
        exp_tt2 = exp(-T/tau2)
        factor1 = (1 - exp_tt1) / (T / tau1)
        factor2 = factor1 - exp_tt1
        factor3 = (1 - exp_tt2) / (T / tau2) - exp_tt2
        if isinstance(T, np.ndarray):
            T[zero_idx] = 0
            factor1[zero_idx] = 1
            factor2[zero_idx] = 0
            factor3[zero_idx] = 0
        return factor1, factor2, factor3

    def zero(self, T):
        beta0 = self.beta0
        beta1 = self.beta1
        beta2 = self.beta2
        beta3 = self.beta3
        factor1, factor2, factor3 = self.factors(T)
        res = beta0 + beta1*factor1 + beta2*factor2 + beta3*factor3
        return res

    def __call__(self, T):
        return self.zero(T)

    def forward(self, T):
        exp_tt0 = exp(-T/self.tau1)
        exp_tt1 = exp(-T/self.tau2)
        return self.beta0 + self.beta1*exp_tt0 \
            + self.beta2*exp_tt0*T/self.tau1 + self.beta3*exp_tt1*T/self.tau2
