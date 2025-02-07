#!/bin/bash
 
#SBATCH --nodes=1                   # the number of nodes you want to reserve
#SBATCH --ntasks-per-node=1         # the number of tasks/processes per node
#SBATCH --cpus-per-task=32          # the number cpus per task
#SBATCH --partition=normal          # on which partition to submit the job
#SBATCH --time=1-00:00:00             # the max wallclock time (time limit your job will run)
 
#SBATCH --job-name=toad         # the name of your job
#SBATCH --mail-type=ALL             # receive an email when your job starts, finishes normally or is aborted
#SBATCH --mail-user=jan.stenkamp@uni-muenster.de # your mail address
#SBATCH -o ./report/output.%j.out
 
# LOAD MODULES HERE IF REQUIRED
module load palma/2024a
module load GCCcore/13.3.0
module load CMake/3.29.3

# BUILD THE APPLICATION IF REQUIRED
cmake -B build -S . -DUSE_CUDA=0 -DUSE_DEBUG=ON
cmake --build build -j4

# START THE APPLICATION
sh runExperiments.sh "../lightgbm"
