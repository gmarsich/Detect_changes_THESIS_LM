# environment: sceneGraphs_groundTruth_Replica

'''In this script I save a scene graph given the frl apartment. The files may come from the ground truth or from LabelMaker.'''

from SceneGraph import SceneGraph # local file
import os
import time

start_time = time.time()

#
# Variables
#

frl_apartment = 'frl_apartment_0'
basePath = '/local/home/gmarsich/Desktop/data_Replica/'

namePCD = frl_apartment + '_withIDs.ply'
nameDistanceMatrix = 'matrix_distances_file<function distance_Euclidean_closest_points at 0x7f774e90e830>.txt'
nameAssociations = 'associations_objectIdIndex.json'
nameListInstances = 'list_instances.txt'
nameColorDict = 'colorDict_frlApartments.json'

path_save_sceneGraph = os.path.join(basePath, frl_apartment, 'Scene_Graphs')


#
# Automatic variables: they should be ok like this
#

os.makedirs(path_save_sceneGraph, exist_ok=True)

path_plyFile = os.path.join(basePath, frl_apartment, namePCD)
path_distanceMatrix = os.path.join(basePath, frl_apartment, nameDistanceMatrix)
path_associationsObjectIdIndex = os.path.join(basePath, frl_apartment, nameAssociations)
path_listInstances = os.path.join(basePath, frl_apartment, nameListInstances)
path_colorDict_frlApartments = os.path.join(basePath, nameColorDict)



#
# Get and save the scene graph
#

sceneGraph = SceneGraph()
sceneGraph.populate_SceneGraph(path_plyFile, path_distanceMatrix, path_associationsObjectIdIndex, path_listInstances, path_colorDict_frlApartments)

sceneGraph.save_SceneGraph(path_save_sceneGraph)


end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")


# TIMINGS:
# frl_apartment_0 GT: 26.915117 seconds
# frl_apartment_1 GT: 27.084913 seconds
# frl_apartment_2 GT: 28.079581 seconds
# frl_apartment_3 GT: 27.812196 seconds
# frl_apartment_4 GT: 28.006293 seconds
# frl_apartment_5 GT: 26.807828 seconds

# frl_apartment_0 LabelMaker: 23.614874 seconds
# frl_apartment_1 LabelMaker: 20.076981 seconds
# frl_apartment_2 LabelMaker: 23.937329 seconds
# frl_apartment_3 LabelMaker: 23.694971 seconds
# frl_apartment_4 LabelMaker: 21.406928 seconds
# frl_apartment_5 LabelMaker: 21.267375 seconds

