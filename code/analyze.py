import numpy as np
import csv
import argparse
from datetime import datetime
from netCDF4 import date2num
from plotter_morris import morris_plotter
import util


# Reads the different files, including the raw simulation results as well as the pre-computed Morris indices,
# to set up the Morris plotting
#
# nb_plots is the number of figures to plot,
# m=0 no plot;
# m=1 only absolute value of normalized Morris indices |mu|,
# m=2 |mu| and (positive or negative) value of normalized Morris indices mu,
# m=3 add the standard deviation;
# m=4 add significance
#
def results_exploitation(quantity_name, config_number, nb_plots):

    # Filesystem
    # Reservoir data
    res_data = 'data/reservoirs/'
    results_path = 'data/WBM_results_extracted/' + quantity_name + '/res_config_'
    morris_folder = 'data/Morris_indices/' + quantity_name + '/'
    save_path = 'figures/USRB_all/' + quantity_name + '/'

    # Read outputs list to get the specs of the plotted quantity
    output_quantities = res_data + 'fields_morris.csv'
    qty_with_unit = 'WARNING: problem with field and unit referencing!'  # default
    with open(output_quantities) as csvfile:
        r = csv.DictReader(csvfile)
        for row in r:
            if str(row['Field']) == quantity_name:
                qty_with_unit = str(row['Name']) + ' (' + str(row['Unit']) + ')'
                to_plot = int(row['Plot_now'])

    if to_plot == 0 or nb_plots == 0:  # No need to plot: stop routine now
        print("Nothing to plot!")
        return None

    # Read first date of record, beginning and ending dates of analysis from .txt file.
    # fbaed = beginning_and_ending_dates
    fbaed = np.loadtxt('analysis_dates.txt', dtype=int, delimiter=',')
    first_day = int(date2num(datetime(fbaed[0, 0], fbaed[0, 1], fbaed[0, 2]), units='days since 1900-01-01',
                             calendar='standard'))
    beginning_date = int(date2num(datetime(fbaed[1, 0], fbaed[1, 1], fbaed[1, 2]), units='days since 1900-01-01',
                                  calendar='standard')) - first_day
    ending_date = int(date2num(datetime(fbaed[2, 0], fbaed[2, 1], fbaed[2, 2]), units='days since 1900-01-01',
                               calendar='standard')) - first_day
    # Index of days that fall on January 1st
    jan_first = util.january_first(beginning_date + first_day, ending_date + first_day, 0)

    # Read csv file to retrieve the name of columns (geographical places) in result files
    # Initialize outputs
    idvec = []
    is_histo = []
    # Initialize outputs
    res_id = []
    max_s = []
    # Read gages csv files to retrieve features' names
    gagesfile = res_data + 'gages.csv'
    # Line by line read
    with open(gagesfile) as csvfile:
        r = csv.DictReader(csvfile)
        for row in r:
            if int(row['Read']) == 1:
                # Read reservoir base data
                idvec.append(str(row['Name']))
                res_id.append(str(row['ID']))
                is_histo.append(int(row['Record_available?']))
                max_s.append(int(row['reservoir_storage']))
    nb_features = len(idvec)  # Number of features

    # Read variable names in problem file
    var_names = np.loadtxt('code/problem.txt', dtype=str, delimiter=',')[:, 0]

    # Read results and extract quartiles
    raw_results = np.loadtxt(results_path + str(0) + '.txt', dtype=float, delimiter=',')  # Read whole period
    x_results = raw_results[beginning_date:ending_date, :]  # Only keep the relevant part
    nb_dates = x_results.shape[0]
    z_results = np.zeros((nb_dates, nb_features, config_number))
    z_results[:, :, 0] = x_results
    for k in range(config_number-1):
        raw_qty_values = np.loadtxt(results_path + str(k) + '.txt', dtype=float, delimiter=',')  # Read whole record
        z_results[:, :, k+1] = raw_qty_values[beginning_date:ending_date, :]  # Keep relevant part
    results_quartiles = util.quartiles(z_results)
    del x_results, z_results
    if quantity_name == 'resStorage':  # Normalize data
        results_quartiles = results_quartiles / 1E6

    # Plot the results
    for j in range(nb_features):

        # Get the data
        raw_morris = np.loadtxt(morris_folder + idvec[j].replace(" ", "") + '.txt', dtype=float, delimiter=',')  # Read Morris record for whole period
        x_morris = raw_morris[beginning_date:ending_date, :]  # Only keep the relevant part

        # Manage historical series
        if is_histo[j] == 1:
            res = []
            with open(res_data + res_id[j] + '.csv') as csvfile:
                r = csv.DictReader(csvfile)
                for row in r:
                    if quantity_name == 'resStorage':
                        res.append(float(row['Storage_m3']) / 1E6)
                    if quantity_name == 'discharge_in':
                        res.append(float(row['Q_in_m3d']) / 86400)
                    if quantity_name == 'discharge_out':
                        res.append(float(row['Q_out_m3d']) / 86400)
            if len(res) == 0:
                is_histo[j] = 0
                histo = np.zeros(nb_dates)
            else:
                histo = res[beginning_date:ending_date]  # Only keep the relevant part
        else:
            histo = np.zeros(nb_dates)

        # Specify title
        title = idvec[j]

        # Normalize storage data and specify maximal storage
        if quantity_name == 'resStorage':
            x_morris = x_morris / 1E6
            max_storage = int(max_s[j])
        else:
            max_storage = np.nan

        if len(jan_first) > 2:  # Multiyear plot of whole period
            morris_plotter(x_morris, results_quartiles[:, j, :], [jan_first[0], jan_first[-1]], title, qty_with_unit,
                           save_path, var_names, nb_plots, is_histo[j], histo, max_storage)
        else:  # Plot for a year or part of a year
            morris_plotter(x_morris, results_quartiles[:, j, :], jan_first, title, qty_with_unit, save_path, var_names,
                           nb_plots, is_histo[j], histo, max_storage)

    return None


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--quantityname', type=str, required=True)
    parser.add_argument('-n', '--confignumber', type=int, required=True)
    parser.add_argument('-m', '--plotquantity', type=int)

    args = parser.parse_args()

    results_exploitation(args.quantityname, args.confignumber, args.plotquantity)
