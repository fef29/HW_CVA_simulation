import os
import pandas as pd
import datetime as dt
from little_junk import *
from irs import *


def main():
    path = r"C:\Users\ferra\PycharmProjects\HW_CVA_simulation\archives\Curves_EUR.xlsx"
    ois_dates = pd.read_excel(path, sheet_name="EUR", usecols="I", dtype={'Dates': dt.date}).dropna()['EUR Std'].tolist()
    ois_values = pd.read_excel(path, sheet_name="EUR", usecols="J").dropna()['VL5'].tolist()
    ois_curve = Curve("OIS", ois_dates, ois_values)

    d1_fix = dt.date(year=2019, month=8, day=30)
    d2_fix = dt.date(year=2019, month=11, day=30)

    d1_float = dt.date(year=2019, month=8, day=30)
    d2_float = dt.date(year=2020, month=2, day=29)

    maturity = dt.date(year=2025, month=8, day=30)
    valuation_date = dt.date(year=2021, month=3, day=31)

    irs = interest_rate_swap(d1_fix,
                             d2_fix,
                             d1_float,
                             d2_float,
                             0.01,
                             "EUR3M",
                             "30/360",
                             "ACT/360",
                             1_000_000,
                             maturity,
                             "payer")

    print(irs.fix_leg.leg_value(ois_curve, valuation_date))
    print(irs.float_leg.leg_value(ois_curve, valuation_date))
    print(irs.value(ois_curve, valuation_date))
    print('hola')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
