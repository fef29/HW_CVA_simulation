
from scipy.interpolate import interp1d


class Curve:
    """Clase curvita"""
    def __init__(self, name, dates, fd):
        self.name = name
        self.dates = dates
        self.fd = fd
        self.f = interp1d([date.toordinal() for date in self.dates], self.fd)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def dates(self):
        return self._dates

    @dates.setter
    def dates(self, value):
        self._dates = value

    @property
    def fd(self):
        return self._fd

    @fd.setter
    def fd(self, value):
        self._fd = value

    def __call__(self, value):
        return self.f(value.toordinal())
