# Optional
import random

# Input and output file paths
print("Examples: ./genetic-variant-annotation/homo_sapiens-chrY.gvf\n ./genetic-variant-annotation/homo_sapiens-chrY-short.gvf")
input_file = input(str("Insert your input file path: "))
output_file = input(str("Insert your output file path: "))

# Read all lines from input file
with open(input_file, 'r') as f:
    lines = f.readlines()

# Randomize the order of lines
random.shuffle(lines)

# Write randomized lines to output file
with open(output_file, 'w') as f:
    f.writelines(lines)

print(f"Randomization completed. Randomized file saved as '{output_file}'.")
