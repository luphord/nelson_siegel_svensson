# -*- coding: utf-8 -*-

"""Implementation of a Nelson-Siegel interest rate curve model.
See `NelsonSiegelCurve` class for details.
"""

from numbers import Real
from dataclasses import dataclass
from typing import Union, Tuple

import numpy as np
from numpy import exp

EPS = np.finfo(float).eps


@dataclass
class NelsonSiegelCurve:
    """Implementation of a Nelson-Siegel interest rate curve model.
    This curve can be interpreted as a factor model with three
    factors (including a constant).
    """

    beta0: float
    beta1: float
    beta2: float
    tau: float

    def factors(
        self, T: Union[float, np.ndarray]
    ) -> Union[Tuple[float, float], Tuple[np.ndarray, np.ndarray]]:
        """Factor loadings for time(s) T, excluding constant."""
        tau = self.tau
        if isinstance(T, Real) and T <= 0:
            return 1, 0
        elif isinstance(T, np.ndarray):
            zero_idx = T <= 0
            T[zero_idx] = EPS  # avoid warnings in calculations
        exp_tt0 = exp(-T / tau)
        factor1 = (1 - exp_tt0) / (T / tau)
        factor2 = factor1 - exp_tt0
        if isinstance(T, np.ndarray):
            T[zero_idx] = 0
            factor1[zero_idx] = 1
            factor2[zero_idx] = 0
        return factor1, factor2

    def factor_matrix(self, T: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Factor loadings for time(s) T as matrix columns,
        including constant column (=1.0).
        """
        factor1, factor2 = self.factors(T)
        constant: Union[float, np.ndarray] = (
            np.ones(T.size) if isinstance(T, np.ndarray) else 1
        )
        return np.stack([constant, factor1, factor2]).transpose()

    def zero(self, T: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Zero rate(s) of this curve at time(s) T."""
        factor1, factor2 = self.factors(T)
        return self.beta0 + self.beta1 * factor1 + self.beta2 * factor2

    def __call__(self, T: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Zero rate(s) of this curve at time(s) T."""
        return self.zero(T)

    def forward(self, T: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Instantaneous forward rate(s) of this curve at time(s) T."""
        exp_tt0 = exp(-T / self.tau)
        return self.beta0 + self.beta1 * exp_tt0 + self.beta2 * exp_tt0 * T / self.tau
