# HPC Running

Depending on the cluster you might want to choose a different parallelisation strategy.
We decided to distribute the training of multiple models across CPUs, which works fine for all approaches.
Notably, lightgbm is also GPU/CUDA optimized if you train those extensively.

The script has multiple settings depending on your cluster (e.g. `partition`). Please adapt it to your needs. We marked multiple TODOs and comments to help you go through the script.
In case the less settings should be tested the parameters `--start`, `--step`, and `--end` allows to test less settings for
`toad_penalty_feature` and `toad_penalty_threshold` (`sbatch slurm_job_parallel_gnu.sh --start -10 --step 1 --end 15`). The default produces `(0 0.0009765625 0.001953125 0.00390625 0.0078125 0.015625 0.03125 0.0625 0.125 0.25 0.5 1.0 2.0 4.0 8.0 16.0 32.0 64.0 128.0 256.0 512.0 1024.0 2048.0 4096.0 8192.0 16384.0 32768.0)` for both settings.
In case you have a dataset with very little features you might want to experiment more with the threshold penalty than the feature penalty.
Currently a maximum of 10 settings is chunked per job.
