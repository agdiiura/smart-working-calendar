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
from workalendar.europe import Italy
from pandas.tseries.offsets import MonthEnd

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

    for year in reversed(years):
        tot_days = 0
        bsn_days = 0
        holidays = list(map(lambda x: pd.Timestamp(x[0]), cal.holidays(year)))
        holidays += closed_days + [pd.Timestamp(f'{year}-06-29')]

        months = reversed(list(range(1, 13)))
        for month in months:
            start = pd.Timestamp(f'{year}-{month}-01')
            if start >= today - MonthEnd(1):
                end = start + MonthEnd(1)
                days = pd.date_range(start=start, end=end, freq='B')
                allowed_days = pd.to_datetime(list(
                    filter(lambda x: x not in holidays, days)
                ))
                s = allowed_days.size

                fancy_output = [
                    (str(d.date()), d.day_name()) for d in allowed_days
                ]
                out = \
                    f'\n{Style.DIM}' \
                    f'{year}-{start.strftime("%b")}' \
                    f'{Style.RESET_ALL}\n'  \
                    f'{fancy_output}\n' \
                    f'Number of working days: {s}.\n'  \
                    f'{Back.LIGHTRED_EX + Style.DIM}' \
                    f'Days in office: {s - n_smart}.' \
                    f'{Style.RESET_ALL}'

                print(out)

                tot_days += s - n_smart
                bsn_days += s

        print(f'\nNumber of bsn days in {year}: {bsn_days}')
        print(f'Number of remaining days in {year}: {tot_days}')
