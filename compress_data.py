import pandas as pd
import os

input_file = "TN_soil_dataset.csv"
output_file = "TN_soil_dataset.csv.gz"

if os.path.exists(input_file):
    print(f"Reading {input_file}...")
    # Read only necessary columns to save memory/time if needed, but full file is safer
    df = pd.read_csv(input_file)
    print(f"Compressing to {output_file}...")
    df.to_csv(output_file, index=False, compression="gzip")
    print("Done.")
else:
    print(f"{input_file} not found.")
