import csv
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np

# This code produces the panels for Figure 6 of this paper

# Inputs are:
#    file_path: the complete path of the file containing the data
#    day: a 2-uplet for month and day of the month, under the form [mm,dd]
#    window_length: number of days over which we are summing inflows and outflows, starting from "day"
#    nbyears: number of years in the historical record that we are considering
# Outputs in MILLIONS M3 are:
#    av_water: total available water (initial storage plus inflows during period)
#    out_tot: total release during period
def period_release(file_path, day, window_length, nbyears):

    # Reading the csv file
    dates = []
    storage = []
    inflows = []
    outflows = []
    with open(file_path) as csvfile:
        r = csv.DictReader(csvfile)
        for row in r:
            dates.append(str(row['DateTime']))
            storage.append(float(row['Storage_m3']))
            inflows.append(float(row['Q_in_m3d']))
            outflows.append(float(row['Q_out_m3d']))

    # Getting key dates (exclude last thirty days)
    date_indexes = []
    for d in range(len(dates)-window_length):
        this_day = datetime.strptime(dates[d], "%m/%d/%Y")
        if this_day.day == day[1] and this_day.month == day[0]:
            date_indexes.append(d)

    # Computing quantities of interest
    in_tot = np.zeros(nbyears)
    out_tot = np.zeros(nbyears)
    av_water = np.zeros(nbyears)
    for i in range(nbyears):
        # Thirty-day inflows and releases
        in_tot[i] = 0
        out_tot[i] = 0
        for j in range(window_length):
            in_tot[i] = in_tot[i] + inflows[date_indexes[i]+j]
            out_tot[i] = out_tot[i] + outflows[date_indexes[i]+j]
        # Available water in next thirty days
        av_water[i] = storage[date_indexes[i]] + in_tot[i]

    # Express results in Millions m3
    av_water = av_water / 1E6
    out_tot = out_tot / 1E6

    return [av_water, out_tot]


def plot_all():

    # First the 2012-2013 drought
    # August 2013 monthly totals
    [aw, rel] = period_release('data/reservoirs/WY9999.csv', [8, 1], 31, 8)
    # Plot only if releases are maximal in 2013
    if rel[4] == np.amax(rel):
        print('Figure for drought in 2013: August available water and release totals')
        # Plot
        fig = plt.figure()
        ax = fig.add_axes([0.125, 0.125, 0.75, 0.75])
        ax.scatter(aw, rel)
        ax.set_xlabel("Total water availability (Millions $m^3$)", size=12)
        ax.set_ylabel("Total release (Millions $m^3$)", size=12)
        ax.set_title("a) August: for years 2009-2016", size=15)
        ax.set_xlim(600, 1200)
        ax.set_ylim(0, 350)
        ax.tick_params(labelsize=12)
        fig.savefig('Aug_2013.png')
        fig.clf()

    # Second the 2011 flood
    # April monthly totals
    [aw, rel] = period_release('data/reservoirs/WY9999.csv', [4, 1], 30, 8)
    # Plot only if releases are maximal in 2011
    if rel[2] == np.amax(rel):
        print('Figure for flooding in 2011: April available water and release totals')
        # Plot
        fig = plt.figure()
        ax = fig.add_axes([0.125, 0.125, 0.75, 0.75])
        ax.scatter(aw, rel)
        ax.set_xlabel("Total water availability (Millions $m^3$)", size=12)
        ax.set_ylabel("Total release (Millions $m^3$)", size=12)
        ax.set_title("b) April: for years 2009-2016", size=15)
        ax.set_xlim(300, 1000)
        ax.set_ylim(0, 250)
        ax.tick_params(labelsize=12)
        fig.savefig('Apr_2011.png')
        fig.clf()

    return None


# Plot the panels of Figure 6
plot_all()
