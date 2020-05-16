# Morris data

At all five reservoirs listed in the paper's Table 2, it gives with a daily timestep the results of the Morris analysis performed with SALib. There is one sub-directory for every quantity of interest:

1) discharge_in: reservoir inflow (m3/s)
2) discharge_out: reservoir outflow (release + spill) (m3/s)
3) resStorage: end-of-period reservoir storage (with a daily timestep) (m3)

In each subdirectory, there is a txt file per reservoir. Each file:

=> has one line per day between Jan 1st 2009 and Dec 31st 2016 (2922 lines total)

=> has 28 columns. There are four quantities associated with each of the seven parameters of the release rule. Results are given in the order of variables as given in code/problem.txt: the first four columns are for the first variables, columns 5-8 for the second variable, etc.
Within each block of four columns, we have in order 1) the absolute value of the Morris index on the day, 2) the actual value, 3) the index's variance, 4) the 95% CI associated with the index.
