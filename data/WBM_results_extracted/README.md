# Results data from the numerical experiment

This directory contains the data extracted from all 400 runs described by the experiment. 
At all five reservoirs listed in the paper's Table 2, it gives with a daily timestep the following quantities, one per sub-directory:

1) discharge_in: reservoir inflow (m3/s)
2) discharge_out: reservoir outflow (release + spill) (m3/s)
3) resStorage: end-of-period reservoir storage (with a daily timestep) (m3)

In each sub-directory, there is one text file per run, with a line for each day between Jan 1st 2009 and Dec 31st 2016 (2922 lines total), and five columns. Each one corresponds to a reservoir from upstream to downstream on the Snake River. The order, identical to that given in ../reservoirs/gages.csv is for each column
1) Jackson Lake
2) Palisades
3) American Falls
4) Minidoka (Walcott Lake)
5) Milner

