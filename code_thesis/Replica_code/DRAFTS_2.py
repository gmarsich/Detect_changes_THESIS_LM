from SceneGraph import SceneGraph
import open3d as o3d 
path = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Scene_Graphs/sceneGraph_LabelMaker'




path_2 = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/scannet200_mask3d_1/mesh_labelled.ply'
pcd_2 = o3d.io.read_point_cloud(path_2)

print(len(pcd_2.points))

graph = SceneGraph()
graph.load_SceneGraph(path)

pcd = graph.get_pointCloud('-1', True)

print(len(pcd.points))