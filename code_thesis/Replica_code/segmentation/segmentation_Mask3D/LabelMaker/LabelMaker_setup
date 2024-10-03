I had to get a different version of setuptools:
	python3 -m pip install setuptools==69.5.1
	conda install setuptools==69.5.1
from https://github.com/pytorch/serve/issues/3176




I followed more or less the instructions given by the README here: https://github.com/cvg/labelmaker?tab=readme-ov-file



Clone the repository of LabelMaker, then open it. Write:
	bash env_v2/install_labelmaker_env.sh 3.10 11.8 2.0.0 10.4.0
to set up the environment for LabelMaker
(The first suggestion:
	bash env_v2/install_labelmaker_env.sh 3.9 11.3 1.12.0 9.5.0
gave error, and didn't work.)


To set up the environment for SDFStudio:
	bash env_v2/install_sdfstudio_env.sh 3.10 11.3
Then, download the checkpoints:
	bash env_v2/download_checkpoints.sh


To set up the scene:
	#
	# Download scene
	#
	export TRAINING_OR_VALIDATION=Training
	export SCENE_ID=47333462
	
	# activate environment
	conda activate labelmaker
	
	# modify the paths as you need in the following line
	python 3rdparty/ARKitScenes/download_data.py raw --split $TRAINING_OR_VALIDATION --video_id $SCENE_ID --download_dir ~/Desktop/LabelMaker/ARKitScenes/ --raw_dataset_assets lowres_depth confidence lowres_wide.traj lowres_wide lowres_wide_intrinsics vga_wide vga_wide_intrinsics
	
	
	#
	# Convert scene to LabelMaker workspace
	#
	# modify the paths as you need in the following two lines
	WORKSPACE_DIR=~/Desktop/LabelMaker/workspace/$SCENE_ID
	
	python scripts/arkitscenes2labelmaker.py --scan_dir ~/Desktop/LabelMaker/ARKitScenes/raw/$TRAINING_OR_VALIDATION/$SCENE_ID --target_dir $WORKSPACE_DIR
	
	
In my case, I will find things in this directory: /local/home/gmarsich/Desktop/LabelMaker/workspace/

