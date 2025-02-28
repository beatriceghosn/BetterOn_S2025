import pandas as pd

# Load CSV file
file_path = "/Users/chuyinghuo/Downloads/BetterOn/Takes_Feb25.csv"  # Update with your actual file path
df = pd.read_csv(file_path)

# Clean column names by stripping spaces
df.columns = df.columns.str.strip()

# Check available columns (for debugging)
print("Columns in CSV:", df.columns)

# Ensure 'Take Length' exists (Your CSV preview doesn't have 'Watches', so we remove that check)
if 'Take Length' not in df.columns:
    raise KeyError("CSV file is missing the 'Take Length' column!")

# Convert 'Take Length' to numeric (handle non-numeric cases)
df['Take Length'] = pd.to_numeric(df['Take Length'], errors='coerce').fillna(0)

# Count takes per cohort based on 'Take Label'
df['Take Count'] = df.groupby('Cohort')['Take Label'].transform(lambda x: x[x != ""].count())

# Placeholder for Watches (since it's missing in your CSV)
df['Watches'] = 0  # You can remove this if 'Watches' isn't needed

# Compute weighted score
df['Score'] = (df['Take Count'] * 1) + (df['Take Length'] * 2) + (df['Watches'] * 3)

# Rank within each cohort
df['Rank'] = df.groupby('Cohort')['Score'].rank(ascending=False, method='dense')

# Reorder the dataframe based on rank
df = df.sort_values(by=['Cohort', 'Rank'])

# Save ranked results
output_path = "/Users/chuyinghuo/Downloads/BetterOn/ranked_output.csv"
df.to_csv(output_path, index=False)

print(f"Ranked data saved to {output_path}")
