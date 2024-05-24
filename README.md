# Thesis - Editable 3D understanding
### Gaia Marsich

Python: `Python 3.10.12`

OS: Ubuntu 22.04.4 LTS.

GPU: NVIDIA Corporation GP102 [GeForce GTX 1080 Ti]

CUDA: 12.1. Executing `nvcc --version` the result is:

```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2023 NVIDIA Corporation
Built on Mon_Apr__3_17:16:06_PDT_2023
Cuda compilation tools, release 12.1, V12.1.105
Build cuda_12.1.r12.1/compiler.32688072_0
```

A virtual environment is used, created like this...







| Element      | Description |
| :---        |    :----:   |
| Code_playground      | Ongoing tests and drafts       |
| info_environment   | Files useful to set up an environment equal to the one used to run the files in this repository|




How I created the virtual environment:

sudo apt update
sudo apt install python3 python3-venv python3-pip
python3 -m venv thesis_env
source thesis_env/bin/activate
pip install -r requirements.txt


deactivate


