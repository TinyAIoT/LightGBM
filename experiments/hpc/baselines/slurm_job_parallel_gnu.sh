#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=192
#SBATCH --partition=zen4
#SBATCH --time=24:00:00
#SBATCH --mem=128G

#SBATCH --job-name=toad
#SBATCH --mail-type=ALL
#SBATCH --mail-user=n_herr03@uni-muenster.de
#SBATCH --output=/scratch/tmp/%u/toad/report/%j.out
#SBATCH --error=/scratch/tmp/%u/toad/report/%j.error
# Load modules

# TODO: adjust modules and requirements
# TODO: load relevant software stack from your HPC environment
module load palma/2022b
module load GCC/12.2.0
module load scikit-learn/1.2.1
module load parallel/20230722
module load tqdm
pip install --user lightgbm

# Make sure any threaded libraries don't spawn extra threads

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1


# Paths, environment setup

home="$HOME"/toad
wd="$WORK"/toad


log_path="$WORK"/toad/report/baselines/sublogs/toad_"$SLURM_JOB_ID"
mkdir -p "$log_path"

result_dir=$wd/results_baselines/$SLURM_JOB_ID
mkdir -p "$result_dir"

# Unused as we do not evaluate results currently:
# result_dir=$wd/results
# mkdir -p "$result_dir"

data_dir=$WORK/toad/data/{$1}
random=1
dataset=breastcancer
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --dataset) dataset="$2"; shift ;;
    --randomseed) random="$2"; shift ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done
# Arrays
models=("lgbm_quant" "ccp" "cegb" "rf" "rf_guo")
datasets=($dataset)
trees=(1 2 4 8 16 32 64 128 256 512 1024)
depths=(1 2 4 8)
alpha=(0.0 0.5 0.25 0.125 0.0625 0.03125 0.015625 0.0078125)

# Export variables for job environment (parallel will inherit env, but --env is explicit below)

export data_dir result_dir log_path
PARALLEL_JOBS=$(( SLURM_CPUS_ON_NODE > 1 ? SLURM_CPUS_ON_NODE-1 : 1 ))



# =========================================================================================================
# ====== Chunked job execution with GNU Parallel (recommended as job management overhead is reduced) ======
# =========================================================================================================

# Option 1 (preferred): Chunked execution with (pseudo-)balanced chunks
# Adapt chunk size (max_chunk_trees) and max_rows_per_chunk to your needs or introduce other balancing criteria

# Create chunked job files directly instead of single joblist
chunk_dir="$log_path"/joblist_chunks
mkdir -p "$chunk_dir"
max_chunk_trees=1050
max_chunk_nodes=530000 # 1014 trees * 2 ^ 8 depth * 2 for ~ multiclass
max_rows_per_chunk=10 # Additional safeguard to limit chunk size
rm -f "$chunk_dir"/joblist.chunk.* # this removes any old chunk files
chunk_index=0
current_chunk_tree_count=0
current_chunk_node_count=0
current_row_count=0
chunk_file="$chunk_dir"/joblist.chunk."$chunk_index"
touch "$chunk_file"
for model in "${models[@]}"; do
  for dataset in "${datasets[@]}"; do
    for tree in "${trees[@]}"; do
      for depth in "${depths[@]}"; do
        for al in "${alpha[@]}"; do
          # if (( current_chunk_tree_count + tree > max_chunk_trees )); then
          node_count=$((tree * 2**depth))
          if [ "$model" = "covtype_multi" ]; then
            node_count=$((node_count * 2))
          fi
          if (( current_chunk_node_count + node_count > max_chunk_nodes || current_row_count >= max_rows_per_chunk )); then
            ((chunk_index+=1))
            chunk_file="$chunk_dir"/joblist.chunk."$chunk_index"
            touch "$chunk_file"
            current_chunk_node_count=0
            current_row_count=0
          fi
          echo "$model $dataset $tree $depth $al $random" >> "$chunk_file"
          ((current_chunk_node_count+=node_count))
          ((current_row_count+=1))
        done
      done
    done
  done
done
total_jobs=$(ls "$chunk_dir"/joblist.chunk.* | wc -l)
echo "Total chunked job files: $total_jobs"

# Run chunks in parallel
parallel -j "$PARALLEL_JOBS" --lb --joblog "$log_path/parallel_chunk_joblog.txt" \
  ./experiments/hpc/baselines/runBatchOfExperiments.sh {1} "$data_dir" "$result_dir" "$log_path" ::: "$chunk_dir"/joblist.chunk.*

# End of script
