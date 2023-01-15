import numpy as np
from scipy.stats import norm as norm

class BachelierSwaption:
    def __init__(self, sigma, t, T, K, swap_rate):
        self.sigma = sigma
        self.t = t
        self.T = T
        self.K = K
        self.swap_rate = swap_rate

        self.tau = self.T - self.t
        self.vol_pond = self.sigma * np.sqrt(self.tau)

    # def compute_price(self):

    def __call__(self):
        return self.vol_pond * (norm.pdf((self.swap_rate - self.K) / self.vol_pond) + (
                    self.swap_rate - self.K) / self.vol_pond * norm.cdf((self.K - self.swap_rate) / self.vol_pond))


class Vasicek:
    def __init__(self, kappa, theta, vol, s, t, T):
        self.kappa = kappa
        self.theta = theta
        self.vol = vol
        self.s = s
        self.t = t
        self.T = T
