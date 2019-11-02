#!/bin/bash

###############################
# Environment and variables

# Which figures to plot
FIG5=1
FIG6=1
FIG7=1
FIG8TO10=1 

# Morris ensemble size in paper
ENS_SIZE=400

# Call Python if needed
#source /etc/profile.d/modules.sh
#module load python-2.7.5

cd ..  # to main directory

###############################
# If it does not exist, creat directories and subdirectories for the figures

if [ ! -d figures ]; then
	mkdir figures
	mkdir figures/in_paper  # where to store the paper's figure
	mkdir figures/USRB_all  # where the Python code produces figures for the whole basin
	cd figures/USRB_all
	mkdir discharge_in discharge_out resStorage  # create subdirectories where figures from th different fields will be stored
	cd ../..  # back to main directory
fi



###############################
# Figure 5

if [ $FIG5 = 1 ]; then

	# Specify analysis dates
	# Date results start
	echo "2009,1,1" > analysis_dates.txt
	# Date plotting starts
	echo "2009,1,1" >> analysis_dates.txt
	# Date plotting ends
	echo "2016,12,31" >> analysis_dates.txt

	# Call the main Python routine to get figures
	python code/analyze.py \
		-q resStorage \
		-n $ENS_SIZE \
		-m 2 

	python code/analyze.py \
		-q discharge_out \
		-n $ENS_SIZE \
		-m 2 

	# Get panels
	mv figures/USRB_all/resStorage/Jackson_9-16_1.png figures/in_paper/Fig5_a.png
	mv figures/USRB_all/discharge_out/Jackson_9-16_1.png figures/in_paper/Fig5_b.png

fi

###############################
# Figure 6

if [ $FIG6 = 1 ]; then

	# Specify analysis dates
	# Date results start
	echo "2009,1,1" > analysis_dates.txt
	# Date plotting starts
	echo "2013,1,1" >> analysis_dates.txt
	# Date plotting ends
	echo "2013,12,31" >> analysis_dates.txt

	# Call the main Python routine to get figures
	python code/analyze.py \
		-q discharge_in \
		-n $ENS_SIZE \
		-m 2
	python code/analyze.py \
		-q discharge_out \
		-n $ENS_SIZE \
		-m 2 
	python code/analyze.py \
		-q resStorage \
		-n $ENS_SIZE \
		-m 2 

	# Get panels
	mv figures/USRB_all/discharge_in/Minidoka_2013_1.png figures/in_paper/Fig6_a.png
	mv figures/USRB_all/discharge_out/Minidoka_2013_1.png figures/in_paper/Fig6_b.png
	mv figures/USRB_all/resStorage/Minidoka_2013_1.png figures/in_paper/Fig6_c.png

fi

###############################
# Figure 7

if [ $FIG7 = 1 ]; then

	# Specify analysis dates
	# Date results start
	echo "2009,1,1" > analysis_dates.txt
	# Date plotting starts
	echo "2012,1,1" >> analysis_dates.txt
	# Date plotting ends
	echo "2013,12,31" >> analysis_dates.txt

	# Call the main Python routine to get figures
	python code/analyze.py \
		-q resStorage \
		-n $ENS_SIZE \
		-m 2 

	# Get panels
	mv figures/USRB_all/resStorage/Jackson_12-13_1.png figures/in_paper/Fig7_a.png
	mv figures/USRB_all/resStorage/Palisades_12-13_1.png figures/in_paper/Fig7_b.png
	mv figures/USRB_all/resStorage/AmericanFalls_12-13_1.png figures/in_paper/Fig7_c.png

fi

###############################
# Figures 8 to 10

if [ $FIG8TO10 = 1 ]; then

	# Specify analysis dates
	# Date results start
	echo "2009,1,1" > analysis_dates.txt
	# Date plotting starts
	echo "2011,3,1" >> analysis_dates.txt
	# Date plotting ends
	echo "2011,7,31" >> analysis_dates.txt

	# Call the main Python routine to get figures
	python code/analyze.py \
		-q resStorage \
		-n $ENS_SIZE \
		-m 2 

	python code/analyze.py \
		-q discharge_out \
		-n $ENS_SIZE \
		-m 2 

	# Get panels
	mv figures/USRB_all/resStorage/Jackson_2011_1.png figures/in_paper/Fig8_a.png
	mv figures/USRB_all/discharge_out/Jackson_2011_1.png figures/in_paper/Fig8_b.png
	mv figures/USRB_all/resStorage/Palisades_2011_1.png figures/in_paper/Fig9_a.png
	mv figures/USRB_all/discharge_out/Palisades_2011_1.png figures/in_paper/Fig9_b.png
	mv figures/USRB_all/resStorage/AmericanFalls_2011_1.png figures/in_paper/Fig10_a.png
	mv figures/USRB_all/discharge_out/AmericanFalls_2011_1.png figures/in_paper/Fig10_b.png

fi

###############################
# Some cleaning
rm analysis_dates.txt
rm figures/USRB_all/resStorage/*
rm figures/USRB_all/discharge_in/*
rm figures/USRB_all/discharge_out/*

