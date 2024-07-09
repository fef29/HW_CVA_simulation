from little_junk import *
from dateutil.relativedelta import relativedelta as rd
import pandas as pd
import datetime as dt


class FixLeg(FixFlow):
    """date1 y date2 son las 2 primeras fechas del flujo"""
    def __init__(self, date1, date2, r, convention, nominal, maturity):
        super().__init__(date1, date2, r, convention, nominal)
        self.maturity = maturity
        self.fix_dates = self.generate_dates()[:-1]
        self.pay_dates = self.generate_dates()[1:]
        self.flows = self.construct_flows()

    def generate_dates(self):
        number_flows = int(round(YearFrac.calculation(self.date1, self.maturity, self.convention) / self.yf, 0))
        return [self.date1 + rd(months=int(round(12 * x * self.yf, 0))) for x in range(number_flows + 1)]

    def generate_discount_factors(self, df_curve, valuation_date):
        a = []
        for f in self.flows:
            if f.date1 > valuation_date:
                a.append(df_curve(f.date2))
            else:
                a.append(0)
        return a

    def construct_flows(self):
        return [FixFlow(d1, d2, self.r, self.convention, self.nominal) for d1, d2 in zip(self.fix_dates, self.pay_dates)]

    def leg_value(self, df_curve, valuation_date):
        FDs = self.generate_discount_factors(df_curve, valuation_date)
        v = 0
        for f, fd in zip(self.flows, FDs):
            if f.date1 > valuation_date:
                v += f.value(fd)
        return v


class FloatLeg(FloatFlow):
    def __init__(self, date1, date2, curve, convention, nominal, maturity):
        super().__init__(date1, date2, curve, convention, nominal)
        self.maturity = maturity
        self.fix_dates = self.generate_dates()[:-1]
        self.pay_dates = self.generate_dates()[1:]
        self.flows = self.construct_flows()

    def generate_dates(self):
        number_flows = int(round(YearFrac.calculation(self.date1, self.maturity, self.convention) / self.yf, 0))
        return [self.date1 + rd(months=int(round(12 * x * self.yf, 0))) for x in range(number_flows + 1)]

    def generate_discount_factors(self, df_curve, valuation_date):
        a = []
        for f in self.flows:
            if f.date1 > valuation_date:
                a.append(df_curve(f.date2))
            else:
                a.append(0)
        return a

    def construct_flows(self):
        flows = [FloatFlow(d1, d2, self.curve, self.convention, self.nominal) for d1, d2 in zip(self.fix_dates, self.pay_dates)]
        flows = self.assign_forward_rate(flows)
        return flows

    def assign_forward_rate(self, flows):
        path = r"C:\Users\ferra\PycharmProjects\HW_CVA_simulation\archives\Curves_EUR.xlsx"
        if self.curve == 'EUR1M':
            dates = pd.read_excel(path, sheet_name="EUR", usecols="A", dtype={'Dates': dt.date}).dropna()['EUR1m'].tolist()
            values = pd.read_excel(path, sheet_name="EUR", usecols="B").dropna()['VL1'].tolist()

        elif self.curve == 'EUR3M':
            dates = pd.read_excel(path, sheet_name="EUR", usecols="C", dtype={'Dates': dt.date}).dropna()['EUR3m'].tolist()
            values = pd.read_excel(path, sheet_name="EUR", usecols="D").dropna()['VL2'].tolist()

        elif self.curve == 'EUR6M':
            dates = pd.read_excel(path, sheet_name="EUR", usecols="E", dtype={'Dates': dt.date}).dropna()['EUR6m'].tolist()
            values = pd.read_excel(path, sheet_name="EUR", usecols="F").dropna()['VL3'].tolist()

        elif self.curve == 'EUR1Y':
            dates = pd.read_excel(path, sheet_name="EUR", usecols="G", dtype={'Dates': dt.date}).dropna()['EUR1y'].tolist()
            values = pd.read_excel(path, sheet_name="EUR", usecols="H").dropna()['VL4'].tolist()

        else:
            dates = 0
            values = 0
            print('error loading the curve to compute forwards')

        fwd_curve = Curve(self.curve, dates, values)
        valuation_date = dates[0]

        # Asignamos forward a los flujos
        for f in flows:
            if f.date1 > valuation_date:
                f.get_forward(fwd_curve)

        return flows

    def leg_value(self, df_curve, valuation_date):
        FDs = self.generate_discount_factors(df_curve, valuation_date)

        v = 0
        for f, fd in zip(self.flows, FDs):
            if f.date1 > valuation_date:
                v += f.value(fd)
        return v


class interest_rate_swap:
    def __init__(self, fix_date1, fix_date2, float_date1, float_date2, fix_rate, curve, fix_convention,
                 float_convention, nominal, maturity, type):
        self.fix_leg = FixLeg(fix_date1, fix_date2, fix_rate, fix_convention, nominal, maturity)
        self.float_leg = FloatLeg(float_date1, float_date2, curve, float_convention, nominal, maturity)
        self.type = type

    def value(self, ois_curve, valuation_date):
        float = self.float_leg.leg_value(ois_curve, valuation_date)
        fix = self.fix_leg.leg_value(ois_curve, valuation_date)

        if self.type == 'payer':
            npv = float - fix
        elif self.type == 'receiver':
            npv = fix - float
        else:
            npv = 0
            print('error')

        return npv
