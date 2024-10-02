import torch
import sys

print(sys.version)

print("\nCUDA available: ", torch.cuda.is_available())
print("CUDA version: ", torch.version.cuda)
print("PyTorch version: ", torch.__version__)
print("Number of GPUs: ", torch.cuda.device_count())
if torch.cuda.is_available():
    print("CUDA Device Name: ", torch.cuda.get_device_name(0))

print("______________________________________________________\n")

# Create a tensor and move it to GPU
x = torch.rand(3, 3)
x = x.to('cuda')

print("Tensor on GPU:", x)
