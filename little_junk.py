from scipy.interpolate import interp1d


class YearFrac:

    @staticmethod
    def calculation(d1, d2, convention):

        if convention.upper() == "ACT/ACT":
            return (d2 - d1).days / 365

        elif convention.upper() == "ACT/360":
            return (d2 - d1).days / 360

        elif convention.upper() == "30/360":
            return (360 * (d2.year - d1.year) + 30 * (d2.month - d1.month) + (min(30, d2.day) - min(30, d1.day))) / 360


class Curve:
    """Clase curvita"""
    def __init__(self, name, dates, fd):
        self.name = name
        self.dates = dates
        self.fd = fd
        self.f = interp1d([date.toordinal() for date in self.dates], self.fd)

    def __call__(self, value):
        return self.f(value.toordinal())


class FixFlow:

    def __init__(self, date1, date2, r, convention, nominal):
        self.date1 = date1
        self.date2 = date2
        self.r = r
        self.convention = convention
        self.nominal = nominal
        self.yf = YearFrac.calculation(date1, date2, convention)
        self.npv = None
        self.fd = None

    def value(self, fd):
        self.npv = self.nominal * self.yf * self.r * fd
        self.fd = fd
        return self.nominal * self.yf * self.r * fd


class FloatFlow:

    def __init__(self, date1, date2, curve, convention, nominal):
        self.fwd = None
        self.npv = None
        self.date1 = date1
        self.date2 = date2
        self.curve = curve
        self.convention = convention
        self.nominal = nominal
        self.yf = YearFrac.calculation(date1, date2, convention)
        self.fd = None
        self.fd = None

    def get_forward(self, curve):
        try:
            df_1 = curve(self.date1)
            df_2 = curve(self.date2)
            self.fwd = (df_1 / df_2 - 1) / self.yf
        except:
            self.fwd = -0.00545

    def value(self, fd):
        self.npv = self.nominal * self.yf * self.fwd * fd
        self.fd = fd
        return self.nominal * self.yf * self.fwd * fd