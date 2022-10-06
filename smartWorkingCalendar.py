"""
-----------------------
smartWorkingCalendar.py
-----------------------

An awesome module to compute the maximum number of days spent in Mordor.
"""
import json
from pathlib import Path

import pandas as pd
from colorama import Back, Style
from pandas.tseries.offsets import MonthEnd
from workalendar.europe import Italy

if __name__ == '__main__':
    cal = Italy()
    today = pd.Timestamp.now()

    with open(Path(__file__).parent / 'config.json', 'r') as f:
        config = json.load(f)
    years = config['years']

    closed_days = list(
        map(pd.Timestamp, config['closed_days'])
    )

    n_smart = config['n_smart']

    for year in years:

        holidays = list(map(lambda x: pd.Timestamp(x[0]), cal.holidays(year)))
        holidays += closed_days

        months = list(range(1, 13))
        for month in months:
            start = pd.Timestamp(f'{year}-{month}-01')
            if start >= today - MonthEnd(1):
                end = start + MonthEnd(1)
                days = pd.date_range(start=start, end=end, freq='B')
                allowed_days = pd.to_datetime(list(
                    filter(lambda x: x not in holidays, days)
                ))
                s = allowed_days.size

                out = \
                    f'\n{Style.DIM}' \
                    f'{year}-{start.strftime("%b")}' \
                    f'{Style.RESET_ALL}\n'  \
                    f'{allowed_days}\n' \
                    f'Number of working days: {s}.\n'  \
                    f'{Back.LIGHTRED_EX + Style.DIM}' \
                    f'Days in office: {s - n_smart}.' \
                    f'{Style.RESET_ALL}'

                print(out)
