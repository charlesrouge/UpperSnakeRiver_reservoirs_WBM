###!/bin/bash

## set the working directory
set -x
cd $PBS_O_WORKDIR
cd ..
export MAIN_DIR=`pwd`
cd $PBS_O_WORKDIR

## Beginning of run: time
echo "Begins at $(date)" > output.txt

# My run-independent exports
export HOME=/home/fs01/cjr276/wbmresvis
export FIELDS=$MAIN_DIR/input_files/fields_morris.csv
export NUM_FIELDS=$(($(echo $(wc -l < $FIELDS))-1))
export SCRATCH=/scratch/cjr276

###############################
# My run-dependent exports
export OUTPUT_DIR=$SCRATCH/RUNS/reservoir_rule/6_morris_0
export ENS_SIZE=400
export NUM_VARS=7
# Maximal number of Morris analysis results in same folder
export MAX_LINES=500  
###############################






###############################
# Plot results

if [ $DO_PLOTMORRIS == 1 ]; then

	# Make figures directories
	if [ ! -d $MAIN_DIR/analyze_morris/figures ]; then mkdir $MAIN_DIR/analyze_morris/figures; fi
	export FIG_DIR=$MAIN_DIR/analyze_morris/figures

	# Create directories for the different fields in the figures folder
	m=1
	while [ $NUM_FIELDS -ge $m ]; do	
		m=$(($m+1))
		awk "NR==$(echo $m){print}" $FIELDS &> current_line.txt
		awk 'BEGIN {FS= ","}; {printf("%s\n",$1)}' current_line.txt &> current_field.txt
		if [ ! -d $FIG_DIR/$(sed -n "1p" < current_field.txt) ]; then mkdir $FIG_DIR/$(sed -n "1p" < current_field.txt); fi
	done
	rm current_line.txt current_field.txt

	# Run the Python code for figures
	mpirun mpi_wrapper_plotter.exe $NUM_FIELDS

fi

###############################

## End of run: time
echo "Ends at $(date)" >> output.txt

####################################
# Reorder resuts in a new file system with Python
source /etc/profile.d/modules.sh
module load python-2.7.5

### Each core deals with a results field

# Read the field
awk "NR==$(echo $(($1+2))){print}" $FIELDS &> line_$1.txt
awk 'BEGIN {FS= ","}; {printf("%s\n",$1)}' line_$1.txt &> field_$1.txt
MY_FIELD=$(sed -n "1p" < field_$1.txt)
rm field_$1.txt

# Reservoir type results?
QTY_TYPE=1

# Call the main Python routine to get figures
python $HOME/viswbm/morris/analyze.py \
	-d $MAIN_DIR/ \
	-r $OUTPUT_DIR/results/ \
	-q $MY_FIELD \
	-t $QTY_TYPE \
	-n $ENS_SIZE \
	-m 2 \
	-o $HOME/data/reservoirs/ \
	-s daily

# A bit of cleaning
rm line_$1.txt























