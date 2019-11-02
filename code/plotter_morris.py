import util
import numpy as np
import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
from netCDF4 import num2date


def morris_plotter(morris, quartiles, date_list, title, qty_name, save_path, var_names, nb_plots, is_histo, histo_data,
                   max_storage):

    # Local variables
    num_var = len(var_names)
    t = np.zeros(len(date_list), dtype=int)
    for i in range(len(date_list)-1):
        t[i+1] = date_list[i+1] - date_list[0]  # Dates with origin the first day

    # Common color map for significance
    cmap = plt.cm.cool   #plt.cm.bwr
    cmaplist = [cmap(0), cmap(255)]
    mycmap = cmap.from_list('Custom cmap', cmaplist, 2)

    # Figure position
    pos = [0.08, 0.08, 0.77, 0.87]

    # Loop on the time periods within t
    for y in range(len(t) - 1):

        # List years and month
        first_day = num2date(date_list[y], units='days since 1900-01-01', calendar='standard')
        first_year = first_day.year
        jan_first_from_beg = util.january_first(date_list[y], date_list[y+1], date_list[y] - 1)
        year_list = np.arange(first_year, first_year + len(jan_first_from_beg) - 1, 1)
        month_first_from_beg = util.monthly_first(date_list[y], date_list[y+1], date_list[y] - 1)
        month_list = util.month_list(month_first_from_beg, date_list[y] - 1)

        # Normalize Morris results
        x_morris = normalize_morris(morris[t[y]:t[y + 1], :], num_var)

        # Maximum of the plotted quantity through time
        if 'Storage' in qty_name:
            qmax = max_storage
        else:
            qmax = np.amax(quartiles[t[y]:t[y + 1], 4])
            if is_histo == 1:
                qmax = max(qmax, np.amax(histo_data[t[y]:t[y + 1]]))

        if qmax == 0:  # Plotting is useless (here qmin = 0)
            return None

        # Title
        if len(t) == 2 and len(year_list) > 1:
            titlestring = title + ', ' + str(first_year) + '-' + str(year_list[-1])
        else:
            titlestring = title + ', year ' + str(first_year)

        # Loop on the four plots for Morris
        for m in range(nb_plots):

            # Morris results
            ze = np.transpose(x_morris[:, np.arange(m, num_var * 4, step=4)])

            # Initialize figure
            aspect_modifier = float(365) / float(min((t[y + 1] - t[y]), 365))
            if 1 < aspect_modifier < 10:
                fig = plt.figure(figsize=(min(16, 18 / np.sqrt(aspect_modifier)), 6 * np.sqrt(aspect_modifier)))
            else:
                fig = plt.figure(figsize=(16, 6))
            ax1 = fig.add_axes(pos)  # Normal axis

            # Supplementary axis for colorbar
            ax2 = fig.add_axes([pos[0] + pos[2] + 0.09, pos[1] + 0.05, 0.015, pos[3] - 0.1])
            ax2.xaxis.set_label_position('top')

            # Colorbar specs
            colorbar_legend = ['$\mu^*$', '$\mu$', '$\sigma$', 'Sig.?']

            # Part dependent on m

            # Colorbar boundaries
            if m < 3:
                z = np.zeros((ze.shape[0], ze.shape[1] + 1))
                z[:, 1:z.shape[1]] = ze
                z[0:2, 0] = [-1 * (m == 1), 1]

            # Colorbar specs
            plt.figtext(pos[0] + pos[2] + 0.07, pos[3] + 0.07, 'Morris ' + colorbar_legend[m], size=20)
            cmapticks = np.linspace(0, 1, num=5, dtype=float)

            if m == 0:  # Plotting the absolute value of the Morris sensitivity index, [0, 1] scale
                cb = matplotlib.colorbar.ColorbarBase(ax2, cmap=plt.cm.Reds )
                cb.set_ticks(cmapticks, update_ticks=True)
                ax1.imshow(z, origin='lower', cmap=plt.cm.Reds, extent=[0, t[y + 1] - t[y], 0, 1.1 * qmax],
                           interpolation='none')
            elif m == 1:  # Plotting the relative value of the Morris sensitivity index, [-1, 1] scale
                cb = matplotlib.colorbar.ColorbarBase(ax2, cmap=plt.cm.bwr)
                cb.set_ticks(cmapticks, update_ticks=True)
                cb.set_ticklabels(['-1', '-0.5', '0', '0.5', '1'])
                ax1.imshow(z, origin='lower', cmap=plt.cm.bwr, extent=[0, t[y + 1] - t[y], 0, 1.1 * qmax],
                           interpolation='none')
            elif m == 2:  # Plotting the standard deviation of the Morris sensitivity index, [0, 1] scale
                cb = matplotlib.colorbar.ColorbarBase(ax2, cmap=plt.cm.Reds)
                cb.set_ticks(cmapticks, update_ticks=True)
                ax1.imshow(z, origin='lower', cmap=plt.cm.Reds, extent=[0, t[y + 1] - t[y], 0, 1.1 * qmax],
                           interpolation='none')
            else:  # Set colorbar boundaries and plot the mesh to represent Morris results significance
                cb = matplotlib.colorbar.ColorbarBase(ax2, cmap=mycmap)
                cb.set_ticks(cmapticks, update_ticks=True)
                cb.set_ticklabels(['', 'No', '', 'Yes, 95%', ''])
                z = np.zeros((ze.shape[0], ze.shape[1] + 1))
                z[:, 1:z.shape[1]] = ze
                ax1.imshow(z >= 1, origin='lower', cmap=mycmap, extent=[0, t[y + 1] - t[y], 0, 1.1 * qmax],
                           interpolation='none')

            # Updating colorbar ticks
            cb.ax.tick_params(labelsize=16)
            cb.update_ticks()

            # Legend initialization
            handles = []

            # Plot the quantity of interest
            for i in range(5):
                if i == 0:
                    simul, = ax1.plot(np.arange(1, t[y + 1] - t[y] + 1), quartiles[t[y]:t[y + 1], i], c='k',
                                      label='Simulated min,\n max and quartiles')
                    handles.append(simul)
                else:
                    ax1.plot(np.arange(1, t[y + 1] - t[y] + 1), quartiles[t[y]:t[y + 1], i], c='k')

            # If there is a historical record, plot it
            if is_histo == 1:
                histo, = ax1.plot(np.arange(1, t[y + 1] - t[y] + 1), histo_data[t[y]:t[y + 1]], c='y', linewidth=2,
                                  label='Historical record')
                handles.append(histo)

            # If this is storage, add max storage
            if 'Storage' in qty_name:
                storage_line = np.ones(t[y + 1] - t[y]) * max_storage
                max_st, = ax1.plot(np.arange(1, t[y + 1] - t[y] + 1), storage_line, c='k', linewidth=2, linestyle=':',
                                   label='Max storage')
                handles.append(max_st)

            # Put legend in
            # if len(handles) > 0:
            #    ax1.legend(handles=handles, loc=1, prop={'size': 16})

            # Title
            ax1.set_title(titlestring, size=24)

            # Tick label x axis, set labels
            ax1.set_ylabel(qty_name, size=20)
            if len(year_list) > 3:
                ax1.xaxis.set_ticks(jan_first_from_beg)
                ax1.xaxis.set_ticklabels(year_list)
                ax1.set_xlabel('Time (years)', size=20)
            else:
                ax1.xaxis.set_ticks(month_first_from_beg)
                ax1.xaxis.set_ticklabels(month_list)
                ax1.set_xlabel('Time (months)', size=20)

            # Tick label sizes
            ax1.tick_params(labelsize=16)
            ax2.tick_params(labelsize=16)

            # Set aspect
            if aspect_modifier > 1 and aspect_modifier < 10:
                aspe = unicode(0.35 / qmax * (t[y + 1] - t[y]) * aspect_modifier)
            else:
                aspe = unicode(0.35 / qmax * (t[y + 1] - t[y]))
            ax1.set_aspect(aspe)
            ax1.set_xlim(1, t[y + 1] - t[y])
            ax1.set_ylim(0, max(1, qmax * 1.1))

            for i in range(num_var):
                label_position = pos[1] + 0.04 + (pos[3] - 0.1) * (1 + 2 * i) / (2 * num_var)
                plt.figtext(pos[0] + pos[2] + .01, label_position, var_names[i], size=20)

            # Save figure and free memory
            if len(t) == 2 and len(year_list) > 1:
                plt.savefig(save_path + title.replace(" ", "") + '_' + str(first_year-2000) + '-' +
                            str(year_list[-1]-2000) + '_' + str(m) + '.png')
            else:
                plt.savefig(save_path + title.replace(" ", "") + '_' + str(first_year) + '_' + str(m) + '.png')
            plt.close(fig)
            del z

    return None


def normalize_morris(morris, nvar):

    x_morris = np.zeros(morris.shape)

    mu_max = np.amax(morris[:, np.arange(0, nvar * 4, step=4)])

    # Determine if 95% CI smaller than mu*
    inter = (morris[:, np.arange(3, nvar * 4, step=4)] < morris[:, np.arange(0, nvar * 4, step=4)])
    x_morris[:, np.arange(3, nvar * 4, step=4)] = inter

    # Normalize mu*
    inter = np.zeros((morris.shape[0], morris.shape[1] / 4))
    np.divide(morris[:, np.arange(0, nvar * 4, step=4)], max(mu_max, 1E-10), out=inter)
    x_morris[:, np.arange(0, nvar * 4, step=4)] = inter

    # Normalize mu
    np.divide(morris[:, np.arange(1, nvar * 4, step=4)], max(mu_max, 1E-10), out=inter)
    x_morris[:, np.arange(1, nvar * 4, step=4)] = inter

    # Normalize sigma
    np.divide(morris[:, np.arange(2, nvar * 4, step=4)],
              max(1E-10, np.amax(morris[:, np.arange(2, nvar * 4, step=4)])), out=inter)
    x_morris[:, np.arange(2, nvar * 4, step=4)] = inter

    return x_morris
