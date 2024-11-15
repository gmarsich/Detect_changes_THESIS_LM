# environment: sgm

'''Create the file objects.json'''

import os
import json
import time


start_time = time.time()

#
# Variables to change
#

frl_apartment = "frl_apartment_5"

basePath = "/local/home/gmarsich/Desktop/data_Replica"

path_listInstances = os.path.join(basePath, frl_apartment, "list_instances.txt")
path_folder_SGAligner = os.path.join(basePath, frl_apartment, "SGAligner")

if not os.path.exists(path_folder_SGAligner):
    os.makedirs(path_folder_SGAligner)

path_save_objectsJSON = os.path.join(path_folder_SGAligner, "objects.json")



#
# Create a dictionary containing some info.
# Save objects.json
#

obj_data = {"objects": []}

with open(path_listInstances, 'r') as file:
    i = 0
    for line in file:
        parts = line.split('\t')

        obj_id = parts[0]
        label = parts[1]

        obj_data["objects"].append({
            "count": i,
            "id": obj_id,
            "label": label,
        })

        i+=1

# Save the dictionary to a JSON file
with open(path_save_objectsJSON, 'w') as json_file:
    json.dump(obj_data, json_file, indent=2)


end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
