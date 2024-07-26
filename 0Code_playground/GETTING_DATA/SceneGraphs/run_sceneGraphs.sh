#!/bin/bash

#SBATCH --account=ls_polle
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=12:00:00
#SBATCH --job-name="sceneGraph"
#SBATCH --mem-per-cpu=16384
#SBATCH --tmp=2000
#SBATCH --mail-type=BEGIN,END

# Activate the virtual environment
source /cluster/home/gmarsich/miniconda3/etc/profile.d/conda.sh
conda activate sceneGraphs_Gaia

# Run the Python script
# TODO: CREATE THE sceneGraph.py FILE
/cluster/home/gmarsich/miniconda3/envs/sceneGraphs_Gaia/bin/python /cluster/home/gmarsich/Thesis/WORKING_CODE/SceneGraphs/sceneGraph.py
