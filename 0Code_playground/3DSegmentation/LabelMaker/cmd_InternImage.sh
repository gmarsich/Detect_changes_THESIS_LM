#!/bin/bash

cd ~/Desktop/LabelMaker

conda activate labelmaker
export WORKSPACE_DIR=/local/home/gmarsich/data2TB/LabelMaker/processed_ARKitScenes_TODO/40753679
python models/internimage.py --workspace $WORKSPACE_DIR

# export WORKSPACE_DIR=/local/home/gmarsich/data2TB/LabelMaker/processed_ARKitScenes_TODO/42898070
# python models/internimage.py --workspace $WORKSPACE_DIR

# export WORKSPACE_DIR=/local/home/gmarsich/data2TB/LabelMaker/processed_ARKitScenes_TODO/48018708
# python models/internimage.py --workspace $WORKSPACE_DIR
