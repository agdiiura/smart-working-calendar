"""
-----------------------
smartWorkingCalendar.py
-----------------------

An awesome module to compute the maximum number of days spent in Mordor.
"""
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from workalendar.europe import Italy

if __name__ == '__main__':
    cal = Italy()
    years = (2022, 2023)

    closed_days = list(
        map(pd.Timestamp, ['2022-10-31', '2022-12-09'])
    )

    n_smart = 13

    for year in years:

        holidays = list(map(lambda x: pd.Timestamp(x[0]), cal.holidays(year)))
        holidays += closed_days

        months = list(range(1, 13))
        for month in months:
            start = pd.Timestamp(f'{year}-{month}-01')
            end = start + MonthEnd(1)
            days = pd.date_range(start=start, end=end, freq='B')
            allowed_days = pd.to_datetime(list(
                filter(lambda x: x not in holidays, days)
            ))
            s = allowed_days.size
            print(
                f"""\n{year}-{start.strftime('%b')}
                {allowed_days}
                Number of working days: {s}.
                Days in office: {s - n_smart}."""
            )
