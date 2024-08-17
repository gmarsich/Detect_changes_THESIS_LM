import numpy as np

np.random.seed(42)
list_colors_tmp = (np.random.rand(4, 3) * 255).astype(np.uint8) 



list_colors = []
for i in range(4):
    list_colors.extend([list_colors_tmp[i]] * 3)


list_colors = np.asarray(list_colors).astype(np.uint8) 

print(list_colors)

