import os

# Define the directory containing the .txt files
label_dir = 'dataset/labels/val'

# Image dimensions
img_width = 3072
img_height = 4080

def normalize(value, max_value):
    return value / max_value

for filename in os.listdir(label_dir):
    if filename.endswith('.txt'):
        filepath = os.path.join(label_dir, filename)
        
        with open(filepath, 'r') as file:
            lines = file.readlines()

        with open(filepath, 'w') as file:
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    x, y, radius = map(float, parts)
                    class_id = 0
                    width = (2 * radius) / img_width
                    height = (2 * radius) / img_height
                    file.write(f"{class_id} {x} {y} {width} {height}\n")
                else:
                    print(f"Skipping invalid line in {filename}: {line}")

print("Normalization complete.")

