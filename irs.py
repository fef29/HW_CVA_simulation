from junk import *
from dateutil.relativedelta import relativedelta as rd
import pandas as pd
import datetime as dt


class Pata(FLujo):
    def __init__(self, date1, date2, r, convention, nominal, maturity):
        super().__init__(date1, date2, r, convention, nominal)
        self.maturity = maturity
        self.fix_dates = self.generate_dates()[:-1]
        self.pay_dates = self.generate_dates()[1:]
        self.flows = self.construct_flows()

    def generate_dates(self):
        # total_yf = YearFrac.calculation(self.date1, self.maturity, self.convention)
        # yf_first_period = YearFrac.calculation(self.date1, self.date2, self.convention)
        total_yf = YearFrac_QL.calculation(self.date1, self.maturity, self.convention)
        yf_first_period = YearFrac_QL.calculation(self.date1, self.date2, self.convention)

        number_flows = int(round(total_yf / yf_first_period, 0))

        # dates = [self.date1 + rd(months=int(round(12 * i * self.yf, 0))) for i in range(number_flows + 1)]
        dates = [self.date1]
        yf = int(round(12 * self.yf, 0))

        for i in range(1, number_flows + 1):
            next_date = dates[i-1] + rd(months=yf)
            dates.append(next_date)

        return dates

    def generate_discount_factors(self, df_curve, valuation_date):
        a = []
        for f in self.flows:
            if valuation_date < f.date2:
                a.append(df_curve(f.date2))
            else:
                a.append(0)
        return a

    def construct_flows(self):
        return [FLujo(d1, d2, self.r, self.convention, self.nominal) for d1, d2 in zip(self.fix_dates, self.pay_dates)]

    def leg_value(self, df_curve, valuation_date):
        FDs = self.generate_discount_factors(df_curve, valuation_date)

        v = 0
        for f, fd in zip(self.flows, FDs):

            if valuation_date < f.date2:
                v += f.value(fd)

            elif f.date2 < valuation_date:
                v += 0
        return v


class PataVariable(Pata):
    def __init__(self, date1, date2, r, convention, nominal, maturity, curve, spread, fixing):
        super().__init__(date1, date2, r, convention, nominal, maturity)
        self.curve = curve
        self.spread = spread
        self.fixing = fixing

    def assign_forward_rate(self, valuation_date):
        for f in self.flows:

            if valuation_date < f.date1:
                f.r = self.get_forward(f.date1, f.date2, f.yf) + self.spread

            elif f.date1 < valuation_date < f.date2:
                f.r = self.fixing

            else:
                f.r = 0

    def get_forward(self, date1, date2, yf):
        df_1 = self.curve(date1)
        df_2 = self.curve(date2)
        fwd = (df_1 / df_2 - 1) / yf
        return fwd

    def leg_value(self, df_curve, valuation_date):
        FDs = self.generate_discount_factors(df_curve, valuation_date)
        self.assign_forward_rate(valuation_date)

        v = 0
        for f, fd in zip(self.flows, FDs):

            if valuation_date < f.date2:
                v += f.value(fd)

            elif f.date2 < valuation_date:
                v += 0
        return v

    def change_float_curve(self, new_curve):
        self.curve = new_curve


class IRS:
    def __init__(self, fix_date1, fix_date2, float_date1, float_date2, fix_rate, curve, fix_convention,
                 float_convention, nominal, maturity, type, spread, fixing):

        self.fix_leg = Pata(fix_date1, fix_date2, fix_rate, fix_convention, nominal, maturity)
        self.float_leg = PataVariable(float_date1, float_date2, 0, float_convention, nominal, maturity, curve, spread, fixing)
        self.type = type
        self.fix_leg_value = None
        self.float_leg_value = None
        self.npv = None

    def change_float_curve(self, new_curve):
        self.float_leg.change_float_curve(new_curve)

    def value(self, ois_curve, valuation_date):
        self.fix_leg_value = self.fix_leg.leg_value(ois_curve, valuation_date)
        self.float_leg_value = self.float_leg.leg_value(ois_curve, valuation_date)

        if self.type == 'payer':
            npv = self.float_leg_value - self.fix_leg_value
        elif self.type == 'receiver':
            npv = self.fix_leg_value - self.float_leg_value
        else:
            npv = 0
            print('error')
        self.npv = npv
        return npv

    def print_value(self):
        print("Pata fija: {}".format(self.fix_leg_value))
        print("Pata variable: {}".format(self.float_leg_value))
        print("MtM: {}".format(self.npv))
        print("##############################################")

