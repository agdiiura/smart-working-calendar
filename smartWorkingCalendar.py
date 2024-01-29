"""
-----------------------
smartWorkingCalendar.py
-----------------------

This module uses the user-defined work calendar to calculate the number of
working days for each month in the specified years.
It considers closed days, holidays, and the configured number
of smart working days to provide detailed information for better planning.


Usage:
1. Make sure to configure the 'config.json' file with the required parameters.
2. Run the script.

Note:
    The module assumes the presence of a valid 'config.json' file
    in the same directory.
"""
import json
import importlib

from pathlib import Path

import click
import pandas as pd

from colorama import Back, Style
from workalendar.core import CoreCalendar
from pandas.tseries.offsets import MonthEnd


def get_calendar(name) -> CoreCalendar:
    """Get the calendar object"""
    region, country = name.split('.')

    module = importlib.import_module(f'workalendar.{region}')
    return getattr(module, country)()


def load_configuration(file_path: str | Path) -> dict:
    """
    Load configuration from a JSON file.

    :param file_path: Path to the JSON configuration file.
    :type file_path: str

    :return: Configuration parameters.
    :rtype: dict
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def compute_working_days(cal: CoreCalendar, year: int, closed_days: list[str], n_smart: int) -> tuple[int, int]:
    """
    Compute the number of working days and remaining days for a given year.

    :param cal: Calendar object.
    :type cal: CoreCalendar

    :param year: The year for which to calculate working days.
    :type year: int

    :param closed_days: List of additional closed days.
    :type closed_days: List[str]

    :param n_smart: Number of smart working days.
    :type n_smart: int

    :return: Total working days and remaining days.
    :rtype: Tuple[int, int]
    """

    today = pd.Timestamp.now()
    holidays = [pd.Timestamp(x[0]) for x in cal.holidays(year)]
    holidays += [pd.Timestamp(day) for day in closed_days] + [pd.Timestamp(f'{year}-06-29')]

    tot_days = 0
    bsn_days = 0

    for month in reversed(range(1, 13)):
        start = pd.Timestamp(f'{year}-{month}-01')
        if start >= today - MonthEnd(1):
            end = start + MonthEnd(1)
            days = pd.date_range(start=start, end=end, freq='B')
            allowed_days = pd.to_datetime([d for d in days if d not in holidays])
            s = allowed_days.size

            fancy_output = [(str(d.date()), d.day_name()) for d in allowed_days]
            out = (
                f'\n{Style.DIM}'
                f'{year}-{start.strftime("%b")}'
                f'{Style.RESET_ALL}\n'
                f'{fancy_output}\n'
                f'Number of working days: {s}.\n'
                f'{Back.LIGHTRED_EX + Style.DIM}'
                f'Days in office: {s - n_smart}.'
                f'{Style.RESET_ALL}'
            )

            print(out)

            tot_days += s - n_smart
            bsn_days += s

    print(f'\nNumber of bsn days in {year}: {bsn_days}')
    print(f'Number of remaining days in {year}: {tot_days}')

    return bsn_days, tot_days


@click.command()
@click.option('--config-path', default=None, help='Configuration file')
def main(config_path: str | Path | None = None):
    """Execute the main script"""

    if config_path is None:
        config_path = Path(__file__).parent / 'config.json'

    if isinstance(config_path, str):
        config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f'config_path {config_path} not exist')

    config = load_configuration(config_path)

    calendar = config['calendar']
    years = config['years']
    closed_days = config['closed_days']
    n_smart = config['n_smart']

    cal = get_calendar(calendar)

    for year in reversed(years):
        _ = compute_working_days(
            cal, year, closed_days, n_smart
        )


if __name__ == '__main__':
    main()
