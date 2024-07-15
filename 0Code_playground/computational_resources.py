import os

# Get the number of CPUs
cpu_count = os.cpu_count()

print(f"Number of CPUs: {cpu_count}")