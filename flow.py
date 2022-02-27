from year_frac import YearFrac


class Flow:
    """Clase flujo que nos permitirá contruir la clase IRS"""

    def __init__(self, f1, f2, r, convention, nominal):
        self.f1 = f1
        self.f2 = f2
        self.r = r
        self.convention = convention
        self.nominal = nominal
        self.yf = YearFrac.calculation(f1, f2, convention)

    @property
    def f1(self):
        return self._f1

    @f1.setter
    def f1(self, value):
        self._f1 = value

    @property
    def f2(self):
        return self._f2

    @f2.setter
    def f2(self, value):
        self._f2 = value

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        self._r = value

    @property
    def convention(self):
        return self._convention

    @convention.setter
    def convention(self, value):
        self._convention = value

    @property
    def nominal(self):
        return self._nominal

    @nominal.setter
    def nominal(self, value):
        self._nominal = value

    def value(self, fd):
        """Devuelve el valor del flujo"""
        return self.nominal * self.yf * self.r * fd
