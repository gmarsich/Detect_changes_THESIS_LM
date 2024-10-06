# environment: sceneGraphs_groundTruth_Replica

'''In this script I save a scene graph given the frl apartment. The files may come from the ground truth or from LabelMaker.'''

from SceneGraph import SceneGraph # local file
import os


#
# Variables
#

frl_apartment = 'frl_apartment_1'
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



