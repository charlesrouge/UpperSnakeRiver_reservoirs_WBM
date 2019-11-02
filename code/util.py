from datetime import datetime
from netCDF4 import date2num, num2date
import numpy as np


# Lists the days that are January firsts, in between and including the specified first and last days
# An adjustment variable knockdown is also specified
def january_first(first_day, last_day, knockdown):

    # Initialize loop
    jan_first = []
    this_day = num2date(first_day, units='days since 1900-01-01', calendar='standard')
    current_year = this_day.year
    current_day = first_day

    # Main loop
    while current_day < last_day:
        jan_first.append(current_day - knockdown)
        current_year += 1
        this_day = date2num(datetime(current_year, 1, 1), units='days since 1900-01-01', calendar='standard')
        current_day = int(this_day)

    if last_day > 0:
        jan_first.append(last_day - knockdown)

    return jan_first


# Lists the days that firsts of their month, from a first day
# A last day is specified
# BOTH first and last days are in number format
# Also, am adjustment variable knockdown exists
def monthly_first(first_day, last_day, knockdown):

    # Initialize loop
    month_first = []
    this_day = num2date(first_day, units='days since 1900-01-01', calendar='standard')
    current_year = this_day.year
    current_month = this_day.month
    this_day = date2num(datetime(current_year, current_month, 1), units='days since 1900-01-01', calendar='standard')
    current_day = int(this_day)

    # Main loop
    while current_day <= last_day:
        month_first.append(int(current_day - knockdown))
        if current_month == 12:
            current_year += 1
            current_month = 1
        else:
            current_month += 1
        this_day = date2num(datetime(current_year, current_month, 1), units='days since 1900-01-01',
                            calendar='standard')
        current_day = int(this_day)

    return month_first


# List the months as letters, from a list of days, and possibly a knockdown that translates the values
def month_list(days_list, knockdown):

    all_months = []

    for i in range(len(days_list)):
        this_day = num2date(days_list[i] + knockdown, units='days since 1900-01-01', calendar='standard')
        this_month = this_day.month
        all_months.append(get_month(this_month))

    return all_months


# Get the letter associated to a month
def get_month(argument):
    switcher = {
        1: "J",
        2: "F",
        3: "M",
        4: "A",
        5: "M",
        6: "J",
        7: "J",
        8: "A",
        9: "S",
        10: "O",
        11: "N",
        12: "D"
    }
    return switcher.get(argument, "Invalid month")


# Outputs the quartiles from an ensemble of time series
# 3 dimensions in input, classified by
#   0) time steps
#   1) points at each time step
#   2) ensemble members
def quartiles(tab):

    s = tab.shape
    q = np.zeros((s[0], s[1], 5))

    for j in range(s[1]):
        a = tab[:, j, :]
        x = np.sort(a)
        for i in range(5):
            z = float((s[2]-1)*i)/4
            if int(z) == z:
                q[:, j, i] = x[:, int(z)]
            else:
                coeff = z - int(z)
                q[:, j, i] = (1 - coeff) * x[:, int(z)] + coeff * x[:, int(z)+1]

    return q
