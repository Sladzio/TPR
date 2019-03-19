#!/bin/bash -l

#SBATCH -N 1
#SBATCH --cpus-per-task=12
#SBATCH --time=01:00:00
#SBATCH -p plgrid
#SBATCH --output="output.out"
#SBATCH --error="error.err"

srun /bin/hostname

module load plgrid/tools/python/3.4.2
pip3 install --user mpi4py

cd $SLURM_SUBMIT_DIR

	for NUMBER_OF_PROC in {1,2,4,8,12,24}
	do
        for NUMBER_OF_POINTS in 1000000 1000000000 10000000000
        do
            mpiexec  -np $NUMBER_OF_PROC main.py $NUMBER_OF_POINTS scalable >> results_scalable.txt
            mpiexec  -np $NUMBER_OF_PROC main.py $NUMBER_OF_POINTS non_scalable >> results_non_scalable.txt
        done
	done