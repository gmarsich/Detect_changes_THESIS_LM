from SceneGraph import SceneGraph, update_changes
import open3d as o3d 

path_0 = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/Scene_Graphs/sceneGraph_GT'
path_1 = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/Scene_Graphs/sceneGraph_GT'

graph_0 = SceneGraph()
graph_0.load_SceneGraph(path_0)

graph_1 = SceneGraph()
graph_1.load_SceneGraph(path_1)








list_newID_added = ['136', '127']
list_oldID_removed = ['71', '45']
dict_oldIDnewID_moved = {'77': '34', '4': '103'}
dict_oldIDnewID_still = {'10': '27', '120': '89'}

list_IDs_0 = ['10', '4', '71', '77', '45', '120']
list_IDs_1 = ['27', '103', '136', '34', '127', '89']

deepcopy_old_SceneGraph, deepcopy_new_SceneGraph = update_changes(graph_0, graph_1, list_newID_added, list_oldID_removed, dict_oldIDnewID_moved, dict_oldIDnewID_still)



list_vertices, list_centroids, list_colors_vertices, list_labels, PCDs, list_edges, list_pairs_edges = deepcopy_old_SceneGraph.get_visualisation_SceneGraph(list_IDs_0, threshold=5, color = 'withUpdates')
deepcopy_old_SceneGraph.draw_SceneGraph_PyViz3D(list_centroids, list_colors_vertices, list_labels, list_pairs_edges, PCDs, wantLabels = True)

# list_vertices, list_centroids, list_colors_vertices, list_labels, PCDs, list_edges, list_pairs_edges = deepcopy_new_SceneGraph.get_visualisation_SceneGraph(list_IDs_1, threshold=5, color = 'withUpdates')
# deepcopy_new_SceneGraph.draw_SceneGraph_PyViz3D(list_centroids, list_colors_vertices, list_labels, list_pairs_edges, PCDs, wantLabels = True)