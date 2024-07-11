input_file = "/local/home/gmarsich/Desktop/Thesis/0Code_playground/requirements.txt"
output_file = "/local/home/gmarsich/Desktop/Thesis/0Code_playground/requirements_MOD.txt"

with open(input_file, 'r') as f_input, open(output_file, 'w') as f_output:
    for line in f_input:
        # Split the line by '='
        parts = line.split('=')
        
        if len(parts) >= 3:
            # Construct the modified line with first '=' replaced by '==' and everything after the second '=' removed
            modified_line = parts[0] + '==' + parts[1]
        else:
            # If there are less than 3 parts, use the original line
            modified_line = line
        
        modified_line += '\n'  # Add newline character
        
        # Write the modified line to output file
        f_output.write(modified_line)