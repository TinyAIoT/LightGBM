#!/bin/bash

#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=normal,zen4
#SBATCH --mem=18GB
#SBATCH --time=0-01:00:00
#SBATCH --job-name=data_downloader
#SBATCH --mail-type=ALL
#SBATCH --output /scratch/tmp/%u/toad/download_datasets_%j.log

#load modules 
module purge
# TODO: load relevant software stack from your HPC environment
module load palma/2023a
module load foss/2023a scikit-learn/1.3.1
pip install wget
pip install ucimlrepo

# place of code
home="$HOME"/seed10toad
wd="$WORK"/toad


python "$home"/experiments/python/get_dataset.py --directory "$wd"/data
