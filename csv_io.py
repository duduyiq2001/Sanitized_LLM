


import pandas as pd

import os

def read_set(set_name: str, num_of_rows: int, offset: int) -> pd.DataFrame:
    """
    Reads a specified number of rows from a CSV file, with an offset.

    Args:
        set_name (str): The path or name of the CSV file to read.
        num_of_rows (int): The number of rows to read from the file.
        offset (int): The number of rows to skip before starting to read.

    Returns:
        pd.DataFrame: A DataFrame containing the selected rows.
    """
    # Read the CSV file with the specified number of rows and offset
    df = pd.read_csv(set_name, skiprows=offset, nrows=num_of_rows)

    return df


def save_result(result_csv: str, df: pd.DataFrame):
    """
    Saves the DataFrame to a CSV file. If the CSV file exists, appends the data to it.

    Args:
        result_csv (str): The path or name of the CSV file to save the result to.
        df (pd.DataFrame): The DataFrame containing the data to save.
    """
    # Check if the file exists
    if os.path.exists(result_csv):
        # Append to the file, without writing the header again
        df.to_csv(result_csv, mode='a', header=False, index=False)
    else:
        # Write to a new file, including the header
        df.to_csv(result_csv, mode='w', header=True, index=False)


def get_size(csv)-> int:
    '''
    get the num of rows without loading the entire thing into memory
    '''
    with open(csv, 'r') as file:
        num_rows = sum(1 for _ in file) - 1  # Subtract 1 to exclude the header
    return num_rows
