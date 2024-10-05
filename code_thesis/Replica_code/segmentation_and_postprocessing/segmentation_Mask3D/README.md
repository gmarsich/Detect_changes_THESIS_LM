First of all you need to get the segmentation of the scene with LabelMaker.
Enter the `LabelMaker` folder and follow the instructions given by the `LabelMaker.ipynb` file, specifically in the section "LabelMaker - 5. Mask3D".
The environment that has been used is `labelmaker`, installed as explained in `LabelMaker.ipynb`.

Move the folder `scannet200_mask3d_1` that you will get to the folder `data_Replica/[frl_apartment_i]`.


Afterwards, enter the folder `postprocessing` and using the environment `sceneGraphs_groundTruth_Replica` execute `get_matrixDistance_listObjects_and_get_plyRightFormat.py`.


