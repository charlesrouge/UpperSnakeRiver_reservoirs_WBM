# UpperSnakeRiver_reservoirs_WBM

This repository contains data and code corresponding to the paper "Coordination and Control: Limits in Standard Representations of Multi-Reservoir Operations in Hydrological Modeling" by Charles Rougé, Patrick M. Reed, Danielle S. Grogan, Shan Zuidema, Alexander Prusevich, Stanley Glidden, Jonathan R. Lamontagne, and Richard B. Lammers

The code uses the results from the experiment described in Section 3 of the paper to draw Figures 5 to 10 as in the paper.

Repository overview:

=> Folder "code" contains the code to generate the figures from the paper. It has its own readme that details the files it contains. To generate figures, please follow these steps:
1) download the whole repository
2) open a (Linux) terminal and navigate to the "code" directory
3) type "sh Paper_figures_main.sh" to generate all figures (PNG format). They will be stored in a "figures" directory created in the main directory.

=> Folder "data" contains 3 sub-folders (each have their own readme for details on how to read the data):
1) Sub-folder "WBM_results_extracted" contains results from all 400 members of the ensemble of simulation described in the paper. Since each simulation could generate as much as 4GB of data, only the data immediately useful for figure generation has been uploaded here.
2) Sub-folder "Morris_indices" lists the results from using the SALib python library on the data from "WBM_results_extracted"
3) Sub-folder "reservoirs" lists the data on the reservoirs that are the main focus of this paper, including historical data used to generate the figures.

Licensed under the GNU Lesser General Public License.
