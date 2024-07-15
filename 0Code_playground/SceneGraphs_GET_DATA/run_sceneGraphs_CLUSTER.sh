#!/bin/bash

#SBATCH --account=ls_polle
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --time=4:00:00
#SBATCH --job-name="sceneGraph"
#SBATCH --mem-per-cpu=8192
#SBATCH --tmp=32000
#SBATCH --mail-type=BEGIN,END

# Activate your virtual environment if needed
source /cluster/home/gmarsich/miniconda3/etc/profile.d/conda.sh
conda activate sceneGraphs_Gaia

# Run your Python script
/cluster/home/gmarsich/miniconda3/envs/sceneGraphs_Gaia/bin/python /cluster/home/gmarsich/Thesis/0Code_playground/SceneGraphs_GET_DATA/sceneGraph_GET_DATA.py
