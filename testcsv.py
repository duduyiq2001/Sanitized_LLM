import pandas as pd

# Load the CSV file
file_path = "./datasets/combined_1.csv"
data = pd.read_csv(file_path)

# Filter rows where label == 1
label_1_rows = data[data['label'] == 1]

# Display the filtered rows
print(label_1_rows)
