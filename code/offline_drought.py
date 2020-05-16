import numpy as np
from datetime import datetime
from netCDF4 import date2num
import matplotlib.pyplot as plt
import util
import offline_util

# This produces Figure for S1


# This function is the online model for the flood event studied in the paper
# Inputs:
#    - data_path: path to the simulated data
#    - ens_size: size of simulated ensemble
def offline_model(data_path, ens_size):

    # Local variables, keeping in mind this is a paper-specific figure
    # (most should be arguments for other uses of function)
    first_year = 2009  # First year of simulation results
    starting_day = '01/01/2012'  # First day of drought analysis
    window_length = 731  # Number of days to plot
    routing_lag = 7  # Between two reservoirs
    res_names = ['Jackson', 'Palisades', 'American_Falls']
    nb_res = len(res_names)  # Number of reservoirs in cascade
    s_max = [1.078E9, 1.503E9, 2.145E9]  # Maximal storage of reservoirs

    # Get simulation data
    [sim_inflows, sim_outflows, sim_storage, date_num] = \
        offline_util.get_sim_data(data_path, starting_day, first_year, window_length, ens_size)

    # Drought release policy
    policy1_start = '06/21/2012'  # Day the flood release policy starts
    policy2_start = '06/21/2013'  # Day the flood release policy starts
    policy_releases = 50  # Imposed extra daily releases
    policy_duration = 92
    # Date conversion for the days the policy starts
    date1_start = datetime.strptime(policy1_start, "%m/%d/%Y")
    index1_start = int(date2num(date1_start, units='days since 1900-01-01', calendar='standard') - date_num)
    date2_start = datetime.strptime(policy2_start, "%m/%d/%Y")
    index2_start = int(date2num(date2_start, units='days since 1900-01-01', calendar='standard') - date_num)

    # Initialise offline model results
    sur_inflows = np.zeros(sim_inflows.shape)
    sur_outflows = np.zeros(sim_outflows.shape)
    sur_storage = np.zeros(sim_storage.shape)
    inflow_deficit = np.zeros((nb_res, ens_size))

    # Fill them in
    sur_inflows[:, :, :] = sim_inflows
    sur_storage[0, :, :] = sim_storage[0, :, :]  # Initial storage values
    # Set release policy
    sur_outflows[:, :, :] = sim_outflows

    # Main loop
    for t in range(window_length):
        for n in range(ens_size):

            # Jackson Lake outflow bonus:
            if t >= index2_start and t < index2_start + policy_duration and sur_storage[t, 0, n] > 0.2 * s_max[0]:
                sur_outflows[t, 0, n] = sur_outflows[t, 0, n] + policy_releases

            # Jackson Lake one-step balance
            [sur_inflows[t, 0, n], sur_outflows[t, 0, n], sur_storage[t + 1, 0, n], inflow_deficit[0, n]] = \
                offline_util.offline_reservoir_balance(sim_inflows[t, 0, n], sur_inflows[t, 0, n],
                                                       sim_outflows[t, 0, n], sur_outflows[t, 0, n],
                                                       sim_storage[t:t + 2, 0, n], sur_storage[t, 0, n],
                                                       s_max[0], inflow_deficit[0, n])

            # Jackson Lake to Palisades routing
            if t >= routing_lag:
                sur_inflows[t, 1, n] = sur_inflows[t, 1, n] + (sur_outflows[t - routing_lag, 0, n] -
                                                                   sim_outflows[t - routing_lag, 0, n])

            # Palisades outflow bonus
            if sur_storage[t, 1, n] > 0.2 * s_max[1]:
                if (t >= index2_start and t < index2_start + policy_duration) or (t >= index1_start and t < index1_start + policy_duration):
                    sur_outflows[t, 1, n] = sur_outflows[t, 1, n] + policy_releases

            # Palisades one-step balance
            [sur_inflows[t, 1, n], sur_outflows[t, 1, n], sur_storage[t + 1, 1, n], inflow_deficit[1, n]] = \
                offline_util.offline_reservoir_balance(sim_inflows[t, 1, n], sur_inflows[t, 1, n], sim_outflows[t, 1, n],
                                            sur_outflows[t, 1, n], sim_storage[t:t + 2, 1, n], sur_storage[t, 1, n],
                                            s_max[1], inflow_deficit[1, n])

            # Palisades to American Falls routing
            if t >= routing_lag:
                sur_inflows[t, 2, n] = sur_inflows[t, 2, n] + (sur_outflows[t - routing_lag, 1, n] -
                                                                sim_outflows[t - routing_lag, 1, n])

            # American Falls one-step balance
            [sur_inflows[t, 2, n], sur_outflows[t, 2, n], sur_storage[t + 1, 2, n], inflow_deficit[2, n]] = \
                offline_util.offline_reservoir_balance(sim_inflows[t, 2, n], sur_inflows[t, 2, n], sim_outflows[t, 2, n],
                                            sur_outflows[t, 2, n], sim_storage[t:t + 2, 2, n], sur_storage[t, 2, n],
                                            s_max[2], inflow_deficit[2, n])

    # Only returning the quartiles
    sur_in = util.quartiles(sur_inflows)
    sur_out = util.quartiles(sur_outflows)
    sur_st = util.quartiles(sur_storage)
    sim_in = util.quartiles(sim_inflows)
    sim_out = util.quartiles(sim_outflows)
    sim_st = util.quartiles(sim_storage)

    # Plotting
    for i in range(nb_res):
        comparison_drought(res_names[i], 'Inflows', '$m^3/s$', sim_in[:, i, :], sur_in[:, i, :], 0, [152, 335])
        comparison_drought(res_names[i], 'Release', '$m^3/s$', sim_out[:, i, :], sur_out[:, i, :], 0, [152, 335])
        comparison_drought(res_names[i], 'Storage', 'Millions $m^3$', sim_st[1:window_length + 1, i, :] / 1E6,
                            sur_st[1:window_length + 1, i, :] / 1E6, s_max[i] / 1E6, [152, 335])

    # Plotting
    for i in range(nb_res):
        comparison_drought(res_names[i], 'Inflows', '$m^3/s$', sim_in[:, i, :], sur_in[:, i, :], 0, [518, 701])
        comparison_drought(res_names[i], 'Release', '$m^3/s$', sim_out[:, i, :], sur_out[:, i, :], 0, [518, 701])
        comparison_drought(res_names[i], 'Storage', 'Millions $m^3$', sim_st[1:window_length + 1, i, :] / 1E6,
                            sur_st[1:window_length + 1, i, :] / 1E6, s_max[i] / 1E6, [518, 701])

    return None


# Handles the plotting
def comparison_drought(res_name, var_name, unit, sim_var, sur_var, bonus_param, date_range):

    # Plot general specs
    fig = plt.figure()
    ax = fig.add_axes([0.15, 0.15, 0.8, 0.8])

    # Quantities to plot and legend
    handles = []  # Initialize legend
    for i in range(5):  # Simulated and offline model time series
        simul, = ax.plot(sim_var[date_range[0]:date_range[1], i], 'k', label='Simulated')
        surrog, = ax.plot(sur_var[date_range[0]:date_range[1], i], ':b', label='Offline model')
    handles.append(simul)
    handles.append(surrog)
    if 'Storage' in var_name:
        max_st, = ax.plot(np.ones(date_range[1]-date_range[0]) * bonus_param, c='r', linewidth=2, linestyle='--',
                          label='Max storage')
        handles.append(max_st)
        ax.legend(handles=handles, loc=3, prop={'size': 14})
    else:
        ax.legend(handles=handles, loc=2, prop={'size': 14})
    ax.xaxis.set_ticks([0, 30, 61, 92, 122, 153])
    ax.xaxis.set_ticklabels(['J', 'J', 'A', 'S', 'O', 'N'])
    ax.tick_params(labelsize=14)
    ax.set_xlabel("Time", size=14)
    ax.set_xlim(0, date_range[1]-date_range[0])
    ax.set_ylim(0, 1.1 * max(np.amax(sim_var), np.amax(sur_var)))
    ax.set_ylabel(var_name + ' (' + unit + ')', size=14)
    # ax.set_title('Min., max. and quartiles, simulated vs. offline model')
    range_index = 1 + date_range[0]/365
    fig.savefig(res_name + '_' + var_name + '_' + str(range_index) + '.png')
    fig.clf()

    return None


# Executing code above
offline_model('data', 400)
