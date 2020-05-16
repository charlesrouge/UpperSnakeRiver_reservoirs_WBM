import numpy as np
from datetime import datetime
from netCDF4 import date2num


# This function gets the requisite data from the simulation results in order to incorporate them to the online model
# Inputs:
#    - data_path: path to the simulated data
#    - starting_day: day the offline model starts
#    - first_year; first year of simulation
#    - window_length: duration we are looking at
#    - ens_size: size of simulated ensemble
def get_sim_data(data_path, starting_day, first_year, window_length, ens_size):

    # Date conversion for the day the offline water balance starts
    date = datetime.strptime(starting_day, "%m/%d/%Y")
    date_num = date2num(date, units='days since 1900-01-01', calendar='standard')
    day_index = int(date_num - date2num(datetime(first_year, 1, 1), units='days since 1900-01-01', calendar='standard'))

    # Get simulated data

    # Local variable
    res_sim_indexes = [0, 1, 2]
    nb_res = len(res_sim_indexes)

    # Inflows
    inflows_path = data_path + '/WBM_results_extracted/discharge_in/res_config_'
    raw_results = np.loadtxt(inflows_path + str(0) + '.txt', dtype=float, delimiter=',')  # Read whole period
    x_results = raw_results[day_index:day_index + window_length, res_sim_indexes]  # Only keep the relevant part
    nb_dates = x_results.shape[0]
    s_inflows = np.zeros((nb_dates, nb_res, ens_size))
    s_inflows[:, :, 0] = x_results
    for k in range(ens_size - 1):
        raw_results = np.loadtxt(inflows_path + str(k) + '.txt', dtype=float, delimiter=',')  # Read whole record
        s_inflows[:, :, k + 1] = raw_results[day_index:day_index + window_length, res_sim_indexes]  # Relevant part

    # Releases (Outflows) and storage
    outflows_path = data_path + '/WBM_results_extracted/discharge_out/res_config_'
    storage_path = data_path + '/WBM_results_extracted/resStorage/res_config_'
    s_outflows = np.zeros((nb_dates, nb_res, ens_size))
    s_storage = np.zeros((nb_dates + 1, nb_res, ens_size))  # Also accounts for day-before end-of-day storage
    for k in range(ens_size):
        raw_results = np.loadtxt(outflows_path + str(k) + '.txt', dtype=float, delimiter=',')  # Read whole record
        s_outflows[:, :, k] = raw_results[day_index:day_index + window_length, res_sim_indexes]  # Keep relevant part
        raw_results = np.loadtxt(storage_path + str(k) + '.txt', dtype=float, delimiter=',')  # Read whole record
        s_storage[:, :, k] = raw_results[day_index - 1:day_index + window_length, res_sim_indexes]  # Relevant part

    return [s_inflows, s_outflows, s_storage, date_num]


# This function does the one-step offline water balance for a reservoir, based on differences between simulation results
# and offline simulation up to there
# Inputs:
#    - sim_in: simulated inflows to the reservoir
#    - sur_in: a priori inflows from water balance model, before factoring in physical cosntraints
#    - sim_out: simulated outflows from the reservoir
#    - sur_out: a priori outflows from water balance model, before factoring in physical cosntraints
#    - sim_sto: simulated reservoir storage
#    - sur_sto: offline model storage from previous time step
#    - s_max: reservoir capacity
#    - inflow_deficit: if routing from upstream and different decisions lead to negative inflows, we have zeros inflows and report the deficit on the next day
def offline_reservoir_balance(sim_in, sur_in, sim_out, sur_out, sim_sto, sur_sto, s_max, inflow_deficit):

    # Inflows (m3/s)
    new_in = sur_in - inflow_deficit
    new_deficit = max(0, - new_in)
    new_in = max(0, new_in)

    # Storage (m3) and outflows (m3/s)
    new_sto = sim_sto[1] + (sur_sto - sim_sto[0]) + 86400 * (new_in - sim_in) - 86400 * (sur_out - sim_out)
    if new_sto > s_max:
        new_out = sur_out + (new_sto - s_max) / 86400
        new_sto = s_max
    else:
        if new_sto < 0:
            new_out = sur_out + new_sto / 86400
            if new_out < 0:  # not enough water
                new_in = new_in - new_out  # Increase inflows
                new_deficit = new_deficit - new_out  # Keep balance of that
                new_out = 0  # Set outflows to 0
            new_sto = 0
        else:
            new_out = sur_out

    return [new_in, new_out, new_sto, new_deficit]

