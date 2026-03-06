#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=128
#SBATCH --partition=zen2-128C-496G
#SBATCH --time=24:00:00
#SBATCH --mem=400G

#SBATCH --job-name=testsubtoad
#SBATCH --mail-type=ALL
#SBATCH --mail-user=n_herr03@uni-muenster.de
#SBATCH --output=/scratch/tmp/%u/toad/report/%j.out 
#SBATCH --error=/scratch/tmp/%u/toad/report/%j.error 
# Load modules

# TODO: load relevant software stack from your HPC environment
# Below are packages we used that are necessary, however a clust might require more...
# E.g. we have module load palma/2024a
module load palma/2024a
module load GCCcore/13.3.0
module load CMake/3.29.3
module load parallel/20240722
NUMBER_OF_CPUS_PER_JOB=1
export OPENBLAS_NUM_THREADS=$NUMBER_OF_CPUS_PER_JOB
export MKL_NUM_THREADS=$NUMBER_OF_CPUS_PER_JOB
export OMP_NUM_THREADS=$NUMBER_OF_CPUS_PER_JOB
# TODO: Or your folders
home="$HOME"/toad
wd="$WORK"/toad

cd $home
git submodule init
git submodule update
# Build application (use available CPUs)
cmake -B build -S . -DUSE_CUDA=0 -DUSE_DEBUG=ON
cmake --build build -j "$SLURM_CPUS_ON_NODE"

log_path="$wd"/report/sublogs/toad_"$SLURM_JOB_ID"
echo $log_path
mkdir -p "$log_path"

model_dir=$wd/models/$SLURM_JOB_ID
echo $model_dir
mkdir -p "$model_dir"

result_dir=$wd/result
echo $result_dir
# TODO: Adapt if you want to have a specific forestsize
ms=6400000
# point to built lightgbm binary (adjust if different)
lgbm="./lightgbm"

# Configure parameter ranges for experiments (fp, tp, datasets, trees, depth)

# fp/tp range is 2^start ... 2^end with step size step in the exponent + the value 0 (always includes 0 independently of start/step/end)
# Defaults for start/step/end
dataset="breastcancer"
randomseed=1
start=-10
step=1
end=15
# user needs to execute this script with -- e.g. sbatch slurm_job_parallel_gnu.sh --start -10 --step 1 --end 15
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --start) start="$2"; shift ;;
    --step) step="$2"; shift ;;
    --end) end="$2"; shift ;;
    --dataset) dataset="$2"; shift ;;
    --randomseed) randomseed="$2"; shift ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done
echo "Using start=$start step=$step end=$end"

# Arrays
datasets=($dataset)
random=$randomseed
data_dir=$WORK/toad/data/$random/

trees=(1 2 4 8 16 32 64 128 256 512 1024)
depths=(1 2 4 8)

# build tp/fp arrays (small loop; using python for float math is OK)
tp=(0)
fp=(0)
for i in $(seq "$start" "$step" "$end"); do
  val=$(python3 -c "print(float(2**$i))")
  tp+=("$val")
  fp+=("$val")
done

# Prepare job list file for GNU Parallel (Option 1-5)
joblist="$log_path/joblist.txt"
rm -f "$joblist"

for dataset in "${datasets[@]}"; do
  for tree in "${trees[@]}"; do
    for depth in "${depths[@]}"; do
      for fp_val in "${fp[@]}"; do
        for tp_val in "${tp[@]}"; do
          echo "$dataset $tree $depth $fp_val $tp_val $random">> "$joblist"
        done
      done
    done
  done
done

total_jobs=$(wc -l < "$joblist")
echo "Total jobs: $total_jobs"


# Export variables for job environment (parallel will inherit env, but --env is explicit below)
export lgbm ms data_dir model_dir log_path result_dir
PARALLEL_JOBS_THEORETICAL=$(((SLURM_CPUS_ON_NODE-1)/NUMBER_OF_CPUS_PER_JOB))
# make sure value is > 1
PARALLEL_JOBS=$(( PARALLEL_JOBS_THEORETICAL > 1 ? PARALLEL_JOBS_THEORETICAL : 1 ))

# Option 1 (preferred): Chunked execution with (pseudo-)balanced chunks
# Adapt chunk size (max_chunk_trees) and max_rows_per_chunk to your needs or introduce other balancing criteria

# Create chunked job files directly instead of single joblist
chunk_dir="$log_path/joblist_chunks"
mkdir -p "$chunk_dir"
max_chunk_trees=1050
max_chunk_nodes=270000 # 1024 trees * 2 ^ 8 depth
max_rows_per_chunk=10 # Additional safeguard to limit chunk size
rm -f "$chunk_dir"/joblist.chunk.* # this removes any old chunk files
chunk_index=0
current_chunk_tree_count=0
current_chunk_node_count=0
current_row_count=0
chunk_file="$chunk_dir"/joblist.chunk."$chunk_index"
touch "$chunk_file"
for dataset in "${datasets[@]}"; do
  for tree in "${trees[@]}"; do
    for depth in "${depths[@]}"; do
      for fp_val in "${fp[@]}"; do
        for tp_val in "${tp[@]}"; do
          node_count=$((tree * 2**depth))
          if (( current_chunk_node_count + node_count > max_chunk_nodes || current_row_count >= max_rows_per_chunk )); then
            ((chunk_index+=1))
            chunk_file="$chunk_dir"/joblist.chunk."$chunk_index"
            touch "$chunk_file"
            current_chunk_node_count=0
            current_row_count=0
          fi
          echo "$dataset $tree $depth $fp_val $tp_val $random" >> "$chunk_file"
          ((current_chunk_node_count+=node_count))
          ((current_row_count+=1))
        done
      done
    done
  done
done
total_jobs=$(ls "$chunk_dir"/joblist.chunk.* | wc -l)
echo "Total chunked job files: $total_jobs"
echo "$PARALLEL_JOBS"
# Run chunks in parallel
parallel -j "$PARALLEL_JOBS" --lb --joblog "$log_path/parallel_chunk_joblog.txt" \
  $home/experiments/hpc/runBatchOfExperiments.sh {1} "$lgbm" "$ms" "$data_dir" "$model_dir" "$result_dir" ::: "$chunk_dir"/joblist.chunk.*
# End of script
