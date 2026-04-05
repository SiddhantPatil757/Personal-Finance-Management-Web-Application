import os
import pandas as pd

# Get the folder where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

files = ["income.csv", "expenses.csv", "savings.csv"]

for file in files:
    file_path = os.path.join(base_dir, file)

    df = pd.read_csv(file_path)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])

    clean_path = os.path.join(base_dir, file.replace(".csv", "_clean.csv"))
    df.to_csv(clean_path, index=False)

print("All files cleaned successfully!")
