import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy import interpolate


class hullWhite1F():
    def __init__(self, lambd, eta, curve):
        self.lambd = lambd
        self.eta = eta
        self.curve = curve

    def HW_ZCB(self, T1, T2, rT1):
        B_r = self.HW_B(T1, T2)
        A_r = self.HW_A(T1, T2)
        return np.exp(A_r + B_r * rT1)

    def f0T(self, t):
        # time-step needed for differentiation
        dt = 0.01
        expr = - (np.log(self.curve(t + dt)) - np.log(self.curve(t - dt))) / (2 * dt)
        return expr

    def HW_theta(self, t):
        dt = 0.01
        return 1.0 / self.lambd * (self.f0T(t + dt) - self.f0T(t - dt)) / (2.0 * dt) + self.f0T(t) + self.eta ** 2 / (
                    2.0 * self.lambd ** 2) * (1.0 - np.exp(-2.0 * self.lambd * t))

    def HW_A(self, T1, T2):
        tau = T2 - T1
        zGrid = np.linspace(0.0, tau, 250)
        B_r = lambda x: 1.0 / self.lambd * (np.exp(-self.lambd * x) - 1.0)

        temp1 = self.lambd * integrate.trapezoid(self.HW_theta(T2 - zGrid) * B_r(zGrid), zGrid)

        temp2 = self.eta ** 2 / (4.0 * np.power(self.lambd, 3.0)) * (np.exp(-2.0 * self.lambd * tau) * (
                    4 * np.exp(self.lambd * tau) - 1.0) - 3.0) + self.eta ** 2 * tau / (2.0 * self.lambd ** 2)

        return temp1 + temp2

    def HW_B(self, T1, T2):
        return 1.0 / self.lambd * (np.exp(-self.lambd * (T2 - T1)) - 1.0)
