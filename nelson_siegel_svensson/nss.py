from dataclasses import dataclass


@dataclass
class NelsonSiegelSvenssonCurve:
    beta1: float
    beta2: float
    beta3: float
    beta4: float
    tau1: float
    tau2: float
