#!/bin/bash

###############################
# Environment and variables

# Which figures to plot
# Main body
FIG5=0
FIG6=1
FIG7=0
FIG8=0
FIG9=0
FIG10=0
FIG11=0
# Supplementary material
SUPP1=0
SUPP2=0

# Morris ensemble size in paper
ENS_SIZE=400

# Call Python if needed
#source /etc/profile.d/modules.sh
#module load python-2.7.5

cd ..  # to main directory

###############################
# If it does not exist, create directories and subdirectories for the figures

if [ ! -d figures ]; then
	mkdir figures
	mkdir figures/in_paper  # where to store the figure in the main body of the paper
	mkdir figures/supp_info  # where to store supplementary figures
	mkdir figures/USRB_all  # where the Python code produces figures for the whole basin
	cd figures/USRB_all
	mkdir discharge_in discharge_out resStorage  # create subdirectories where figures from th different fields will be stored
	cd ../..  # back to main directory
fi



###############################
# Figure 5 and Supplementary Material 2

if [ $FIG5 = 1 ] | [ $SUPP2 = 1 ]; then

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

	if [ $SUPP2 = 1 ]; then
	  python code/analyze.py \
		  -q discharge_in \
		  -n $ENS_SIZE \
		  -m 2
	fi

	# Get panels

	if [ $FIG5 = 1 ]; then
	  mv figures/USRB_all/resStorage/Jackson_9-16_1.png figures/in_paper/Fig5_a.png
	  mv figures/USRB_all/discharge_out/Jackson_9-16_1.png figures/in_paper/Fig5_b.png
	fi

	if [ $SUPP2 = 1 ]; then
	  mv figures/USRB_all/discharge_in/Jackson_9-16_1.png figures/supp_info/SI2_1_a.png
	  mv figures/USRB_all/discharge_out/Jackson_9-16_1.png figures/supp_info/SI2_1_b.png
	  mv figures/USRB_all/resStorage/Jackson_9-16_1.png figures/supp_info/SI2_1_c.png
	  mv figures/USRB_all/discharge_in/Palisades_9-16_1.png figures/supp_info/SI2_2_a.png
	  mv figures/USRB_all/discharge_out/Palisades_9-16_1.png figures/supp_info/SI2_2_b.png
	  mv figures/USRB_all/resStorage/Palisades_9-16_1.png figures/supp_info/SI2_2_c.png
	  mv figures/USRB_all/discharge_in/AmericanFalls_9-16_1.png figures/supp_info/SI2_3_a.png
	  mv figures/USRB_all/discharge_out/AmericanFalls_9-16_1.png figures/supp_info/SI2_3_b.png
	  mv figures/USRB_all/resStorage/AmericanFalls_9-16_1.png figures/supp_info/SI2_3_c.png
	  mv figures/USRB_all/discharge_in/Minidoka_9-16_1.png figures/supp_info/SI2_4_a.png
	  mv figures/USRB_all/discharge_out/Minidoka_9-16_1.png figures/supp_info/SI2_4_b.png
	  mv figures/USRB_all/resStorage/Minidoka_9-16_1.png figures/supp_info/SI2_4_c.png
	  mv figures/USRB_all/discharge_in/Milner_9-16_1.png figures/supp_info/SI2_5_a.png
	  mv figures/USRB_all/discharge_out/Milner_9-16_1.png figures/supp_info/SI2_5_b.png
	  mv figures/USRB_all/resStorage/Milner_9-16_1.png figures/supp_info/SI2_5_c.png
	fi

fi

###############################
# Figure 6

if [ $FIG6 = 1 ]; then

fi

###############################
# Figure 7

if [ $FIG7 = 1 ]; then

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
	mv figures/USRB_all/discharge_in/Minidoka_2013_1.png figures/in_paper/Fig7_a.png
	mv figures/USRB_all/discharge_out/Minidoka_2013_1.png figures/in_paper/Fig7_b.png
	mv figures/USRB_all/resStorage/Minidoka_2013_1.png figures/in_paper/Fig7_c.png

fi

###############################
# Figure 8

if [ $FIG8 = 1 ]; then

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
	mv figures/USRB_all/resStorage/Jackson_12-13_1.png figures/in_paper/Fig8_a.png
	mv figures/USRB_all/resStorage/Palisades_12-13_1.png figures/in_paper/Fig8_b.png
	mv figures/USRB_all/resStorage/AmericanFalls_12-13_1.png figures/in_paper/Fig8_c.png

fi

###############################
# Figures 9 and 10

if [ $FIG9 = 1 ] | [ $FIG10 = 1 ]; then

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
	if [ $FIG9 = 1 ]; then
	  mv figures/USRB_all/resStorage/Jackson_2011_1.png figures/in_paper/Fig9_a.png
	  mv figures/USRB_all/discharge_out/Jackson_2011_1.png figures/in_paper/Fig9_b.png
	fi
	if [ $FIG10 = 1 ]; then
	  mv figures/USRB_all/resStorage/Palisades_2011_1.png figures/in_paper/Fig10_a.png
	  mv figures/USRB_all/discharge_out/Palisades_2011_1.png figures/in_paper/Fig10_b.png
	fi

fi

###############################
# Some cleaning
rm analysis_dates.txt
rm figures/USRB_all/resStorage/*
rm figures/USRB_all/discharge_in/*
rm figures/USRB_all/discharge_out/*

