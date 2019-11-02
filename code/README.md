# UpperSnakeRiver_reservoirs_WBM: code README

This directory contains the code used to generate the figure. It contains the following files:

1) Paper_figures_main.sh
This is the main Bash executable, calling it from this directory produces Figures 5 to 10 from the paper.

IMPORTANT: the code contains all the options enabling one to look at results across all five reservoirs described in the paper's Table 2: for this, just comment the lines at the end that clean the "figures/USRB_all" directory. The code is also purposefully geared to enable anyone to generate their own figures by changing the period they are interested in.

2) analyze.py
This is the main Python routine that (1) calls. It gathers the all the necessary data to generate the figures. It then calls (3)

3) plotter_morris.py
This is what produces the figures.

4) util.py
This Python programme contains auxiliary functions that (2) and (3) need.

5) problem.txt
This text file contains the reservoir rule variables described in Section 2 of the paper. This information is used for plotting these variables on the Figures with the correct name.
