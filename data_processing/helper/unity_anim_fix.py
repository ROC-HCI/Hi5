# 1. Read an .anim file line by line
# 2. Find when a line contains 'attribute: localEulerAngles.y' and the next line contains 'path: R_Arm_Cut/R_Forearm/R_Wrist'
# 3. # Replace all the lines that contain 'attribute: ' by multiplying the value by -1 until a line contains "- curve:"
# 4. # Write all the unchanged and changed lines to a new file
# 5. Save it to a new file

import sys


def main():
    # Get the path to the .anim file
    anim_path = "female_short.anim"
    # Get the path to the output .anim file
    output_path = "new_female_short.anim"

    output_path2 = "final_female_short.anim"

    # Open the .anim file
    with open(anim_path, "r") as f:
        # Read the file line by line
        lines = f.readlines()

    # Open the output .anim file
    with open(output_path, "w") as f:
        # Iterate over the lines
        for i, line in enumerate(lines):
            # Check if the line contains 'attribute: localEulerAngles.y' and the next line ends with 'path: R_Arm_Cut/R_Forearm/R_Wrist'
            if 'attribute: localEulerAngles.y' in line and lines[i+1].endswith('path: R_Arm_Cut/R_Forearm/R_Wrist\n'):
                f.write(line)
                # Iterate over the lines until a line contains "- curve:"
                print("Found line: " + line)
                i += 1
                while not 'attribute:' in lines[i]:
                    # Check if the line contains 'value: '
                    if 'value: ' in lines[i]:
                        # Replace the line with the same line but with the value multiplied by -1
                        value = float(lines[i].split('value: ')[1])
                        lines[i] = lines[i].replace(str(value), str(value * -1))
                        print(f"Changing value from {value} to {value * -1}")
                    # Write the line to the output file
                    f.write(lines[i])
                    # Increment the line counter
                    i += 1
                print("Found line 2: " + lines[i])
                f.write(lines[i])
            # Write the line to the output file
            else:
                f.write(line)

    # Open the .anim file
    with open(output_path, "r") as f:
        # Read the file line by line
        lines = f.readlines()

    # Open the output .anim file
    with open(output_path2, "w") as f:
        # Iterate over the lines
        for i, line in enumerate(lines):
            # Check if the line contains 'attribute: m_LocalRotation.y' and the next line ends with 'path: R_Arm_Cut/R_Forearm/R_Wrist'
            if 'attribute: m_LocalRotation.y' in line and lines[i+1].endswith('path: R_Arm_Cut/R_Forearm/R_Wrist\n'):
                f.write(line)
                # Iterate over the lines until a line contains "- curve:"
                print("Found line: " + line)
                i += 1
                while not 'attribute:' in lines[i]:
                    # Check if the line contains 'value: '
                    if 'value: ' in lines[i]:
                        # Replace the line with the same line but with the value multiplied by -1
                        value = float(lines[i].split('value: ')[1])
                        lines[i] = lines[i].replace(str(value), str(value * -1))
                        print(f"Changing value from {value} to {value * -1}")
                    # Write the line to the output file
                    f.write(lines[i])
                    # Increment the line counter
                    i += 1
                print("Found line 2: " + lines[i])
                f.write(lines[i])
            # Write the line to the output file
            else:
                f.write(line)


if __name__ == "__main__":
    main()
