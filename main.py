import pandas as pd
import datetime
from curve import Curve
from irs import IRS_leg


def main():
    ois_dates = pd.read_excel(r"C:\Users\ferra\PycharmProjects\HW_CVA_simulation\archives\Curves_EUR.xlsx",
                              sheet_name="EUR", usecols="I", dtype={'Dates': datetime.date}).dropna()
    ois_dates = ois_dates['EUR Std'].tolist()
    ois_values = pd.read_excel(r"C:\Users\ferra\PycharmProjects\HW_CVA_simulation\archives\Curves_EUR.xlsx",
                               sheet_name="EUR", usecols="J").dropna()['VL5'].tolist()
    ois_curve = Curve("OIS", ois_dates, ois_values)

    date_value = datetime.date(year=2020, month=12, day=31)
    d1 = datetime.date(year=2020, month=12, day=31)
    d2 = datetime.date(year=2021, month=3, day=31)
    d3 = datetime.date(year=2021, month=6, day=30)
    maturity = datetime.date(year=2025, month=3, day=31)
    val_date = d2

    leg = IRS_leg(d1, d2, 0.01, "30/360", 1_000_000, maturity, ois_curve, val_date)

    flow_list = leg.construct_flows()
    yf = [x.yf for x in flow_list]
    fd = leg.df_s()
    v = [f.value(x) for x, f in zip(fd, flow_list)]
    var = flow_list[1].yf

    print(leg.value())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
