from flow import Flow
from year_frac import YearFrac
from dateutil.relativedelta import relativedelta as rd


class IRS_leg(Flow):
    def __init__(self, f1, f2, r, convention, nominal, date_final, df_curve, value_date):
        super().__init__(f1, f2, r, convention, nominal)
        self.date_final = date_final
        self.df_curve = df_curve
        self.value_date = value_date
        self.yf = YearFrac.calculation(self.f1, self.f2, self.convention)

    @property
    def date_final(self):
        return self._date_final

    @date_final.setter
    def date_final(self, value):
        self._date_final = value

    @property
    def df_curve(self):
        return self._df_curve

    @df_curve.setter
    def df_curve(self, value):
        self._df_curve = value

    @property
    def value_date(self):
        return self._value_date

    @value_date.setter
    def value_date(self, value):
        self._value_date = value

    def generate_dates(self):
        """Se generan fechas según la fecha de valoración"""

        if self.value_date <= self.f2:
            final = int(YearFrac.calculation(self.f1, self.date_final, self.convention) / self.yf)
            return [self.f1 + rd(months=12 * x * self.yf) for x in range(final + 2)]

        else:

            x = 1
            while self.value_date > self.f2:
                self.f2 = self.f2 + rd(months=12 * self.yf)
                x = x + 1

            self.f1 = self.f1 + rd(months=12 * x * self.yf)
            final = int(YearFrac.calculation(self.f2, self.date_final, self.convention) / self.yf)

            return [self.f1 + rd(months=12 * x * self.yf) for x in range(final + 1)]

    def fix_dates(self):
        return self.generate_dates()[:-1]

    def pay_dates(self):
        return self.generate_dates()[1:]

    def df_s(self):
        pay_dates = self.pay_dates()
        return [self.df_curve(x) for x in pay_dates]

    def construct_flows(self):
        fix_dates = self.fix_dates()
        pay_dates = self.pay_dates()
        return [Flow(f1, f2, self.r, self.convention, self.nominal) for f1, f2 in zip(fix_dates, pay_dates)]

    def value(self):
        FDs = self.df_s()
        flows = self.construct_flows()
        return sum([f.value(FD) for f, FD in zip(flows, FDs)])


class IRS(IRS_leg):
    def __init__(self, f1, f2, r, convention, N, date_final, DFcurve):
        super().__init__(f1, f2, r, convention, N, date_final, DFcurve, )
