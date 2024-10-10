The environment that should be used is `sceneGraphs_groundTruth_Replica`.

Execute `A_get_matrixDistance_listObjects.py` changing the variables at the beginning and then execute `B_colorDict_frlApartments.py`. You need to execute the first file before the others because the output will be used to align the scenes (one needs to get the points belonging to the reference elements, i.e., stair, ceiling, floor, wall(s)).
Then, enter the folder `alignment_and_postprocessing` and execute, changing the variables, firstly `A_get_transformationMatrix` and then `B_postprocessing_get_plyRightFormat.py`.