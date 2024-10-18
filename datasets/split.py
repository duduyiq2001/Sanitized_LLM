import pandas as pd
import numpy as np

# Load the original CSV file into a DataFrame
input_file = 'combined.csv'
df = pd.read_csv(input_file)

# Calculate the number of rows per split
num_files = 5
rows_per_file = len(df) // num_files

# Split the DataFrame into 5 parts
split_dfs = np.array_split(df, num_files)

# Save each part to a new CSV file with the same headers
for i, split_df in enumerate(split_dfs):
    output_file = f'combined_{i+1}.csv'
    split_df.to_csv(output_file, index=False)
    print(f'Saved {output_file}')
