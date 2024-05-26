# Thesis - Editable 3D understanding
### Gaia Marsich

Contents of the repository:

| Element      | Description |
| :---        |    :----:   |
| Code_playground      | Ongoing tests and drafts       |
| info_environment   | Files useful to set up an environment equal to the one used to run the files in this repository|


## Characteristics of the computer that was used
The code has been run on a machine with:

- Python: `Python 3.10.12`

- OS: Ubuntu 22.04.4 LTS.

- GPU: NVIDIA Corporation GP102 [GeForce GTX 1080 Ti]

- CUDA: 12.1. Executing `nvcc --version` the result is:

```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2023 NVIDIA Corporation
Built on Mon_Apr__3_17:16:06_PDT_2023
Cuda compilation tools, release 12.1, V12.1.105
Build cuda_12.1.r12.1/compiler.32688072_0
```

A virtual environment was set up (the files in `info_environment` list the packages that were installed).

## Getting started
[//]: # (TODO: see Windows other than Ubuntu/Linux)
[//]: # (TODO: try with the yml file)
To set up everything from zero:
- update `apt`:
```
sudo apt update
```
- install Python, a package to handle virtual environment and `pip`:
```
sudo apt install python3 python3-venv python3-pip
```
- create a virual environment (here, `thesis_env`); the folder containing all the data concerning the environment will be created in the current location:
```
python3 -m venv thesis_env
```
- activate the environment;
```
source thesis_env/bin/activate
```
- install the necessary package, listed in the file `requirements.txt` that in in the folder `info_environment` of this repository:
```
pip install -r requirements.txt
```
- when you want to exit the environment, use:
```
deactivate
```
