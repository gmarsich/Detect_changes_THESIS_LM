# environment: sceneGraphs_groundTruth_Replica

'''In this script I save the scene graphs given the frl apartment. The files may come from the ground truth or from LabelMaker.
Be aware the that the scene graph that is generated '''

from SceneGraph import SceneGraph # local file
import os


#
# Variables
#

frl_apartment = 'frl_apartment_0'
basePath = '/local/home/gmarsich/Desktop/data_Replica/'

namePCD = 'frl_apartment_0_withIDs.ply'
nameDistanceMatrix =
nameAssociations =
nameListInstances =
nameColorDict =


#
# Automatic variables: they should be ok like this
#

path_plyFile = os.path.join()
path_distanceMatrix =
path_associationsObjectIdIndex =
path_listInstances =
path_colorDict_frlApartments = 



#
# Get and save the scene graph
#

sceneGraph = SceneGraph()
sceneGraph.populate_SceneGraph(path_plyFile, path_distanceMatrix, path_associationsObjectIdIndex, path_listInstances, path_colorDict_frlApartments)