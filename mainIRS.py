import os
import pandas as pd
import datetime as dt
from junk import *
from IRS import *
from dateutil.relativedelta import relativedelta as rd


def main():
    ## DATA ##
    path = r"C:\Users\ffuster\PycharmProjects\HW_CVA_simulation\input\Datos.xlsx"
    curve_data = pd.read_excel(path, sheet_name="curvas")
    portfolio_data = pd.read_excel(path, sheet_name="portfolio")

    ois = curve_data.loc[curve_data['Curva'] == portfolio_data['Curva Descuento'].values[0]]
    ois_curve = Curve("OIS", list(map(to_datetime, ois['Fecha'].tolist())), ois['Tipo'].tolist())

    float_c = curve_data.loc[curve_data['Curva'] == portfolio_data['Pata Flotante'].values[0]]
    float_curve = Curve(portfolio_data['Pata Flotante'].values[0], list(map(to_datetime, float_c['Fecha'].tolist())),
                        float_c['Tipo'].tolist())

    # print(float_curve.r0())
    # float_curve.shift_dates1(6)
    # float_curve.shift_dates2(dt.datetime(year=2018, month=5, day=31))

    d1_fix = to_datetime(portfolio_data['Start Date'].values[0]).date()
    d1_float = d1_fix

    d2_fix = to_datetime(portfolio_data['d2 fix'].values[0]).date()
    d2_float = to_datetime(portfolio_data['d2 float'].values[0]).date()

    maturity = to_datetime(portfolio_data['Maturity'].values[0]).date()
    valuation_date = to_datetime(portfolio_data['Valuation Date'].values[0]).date()
    fix_rate = portfolio_data['Pata Fija'].values[0]
    nominal = portfolio_data['Nominal'].values[0]
    fixing = portfolio_data['Fixing'].values[0]
    spread = portfolio_data['Spread'].values[0]

    irs = IRS(d1_fix,
              d2_fix,
              d1_float,
              d2_float,
              fix_rate,
              float_curve,
              "30/360",
              "ACT/360",
              nominal,
              maturity,
              "payer",
              spread,
              fixing)

    irs.value(ois_curve, valuation_date)
    irs.print_value()

    val_dates = [valuation_date + rd(months=6 * i) for i in range(1, 12)]
    irsValue = [irs.value(ois_curve, valuation_date)]

    for v_date in val_dates:
        ois_curve.shift_dates1(months=6)
        float_curve.shift_dates1(months=6)
        irs.change_float_curve(float_curve)
        irsValue.append(irs.value(ois_curve, v_date))

    print('aaa')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
