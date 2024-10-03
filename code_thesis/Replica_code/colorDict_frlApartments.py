# environment: sceneGraphs_groundTruth_Replica

'''With this script I want to get a file colorDict_frlApartments.json that is a dictionary containing all the possible labels that appear
in the frl apartments from Replica, and for each label assigns a unique color. The file is saved in the same folder of where this same script is saved.'''

import random
import json
import os


#
# Variables
#

path_listInstances_0 = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_0/list_instances.txt'
path_listInstances_1 = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_1/list_instances.txt'
path_listInstances_2 = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_2/list_instances.txt'
path_listInstances_3 = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_3/list_instances.txt'
path_listInstances_4 = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_4/list_instances.txt'
path_listInstances_5 = '/local/home/gmarsich/Desktop/data_Replica/frl_apartment_5/list_instances.txt'

random.seed(42)

# The output is set to be saved in the folder of this same script

current_dir = os.path.dirname(os.path.abspath(__file__))
path_output = os.path.join(current_dir, 'colorDict_frlApartments.json')



#
# Create colorDict_frlApartments.json
#

def generate_unique_color(used_colors):
    while True:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if color not in used_colors:
            used_colors.add(color)
            return color
        

list_paths = [path_listInstances_0, path_listInstances_1, path_listInstances_2,
              path_listInstances_3, path_listInstances_4, path_listInstances_5]

data_dict = {}

used_colors = set()

for path in list_paths:
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
        continue

    for line in lines:
        line = line.strip() # removes the \n or any other leading/trailing whitespace
        parts = line.split('\t')
        label = parts[1]
        if label not in data_dict:
            color = generate_unique_color(used_colors)
            data_dict[label] = color

with open(path_output, 'w') as json_file:
    json.dump(data_dict, json_file, indent=4)

print(f'Data saved to {path_output}') 
