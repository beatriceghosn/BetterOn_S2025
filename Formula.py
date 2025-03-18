import pandas as pd

# Load CSV file
file_path = "/Users/chuyinghuo/Downloads/BetterOn/Takes_Feb25.csv"  # Update with actual file path
df = pd.read_csv(file_path, skiprows = range)

df.columns = df.columns.str.strip()  # Clean column names
print("Columns in CSV:", df.columns)

if 'Take Length' not in df.columns:
    raise KeyError("CSV file is missing the 'Take Length' column!")

df['Take Length'] = pd.to_numeric(df['Take Length'], errors='coerce').fillna(0)
df['Take Count'] = df.groupby('Cohort')['Take Label'].transform(lambda x: x[x != ""].count())
df['Watches'] = 0  # Placeholder for missing column

# Define module difficulty mapping (or load from CSV)
difficulty_data = {
    "Your Baseline": 0.2,
    "Audience Connection": 1.75,
    "Keep Giving Those Gifts": 1.25,
    "The Moment Begins": 0.8
}

# Ensure correct column name for module reference
if 'Activity' not in df.columns:
    raise KeyError("CSV file is missing the 'Activity' column!")

# Map difficulty using the correct column
df['Module Average Difficulty'] = df['Activity'].map(difficulty_data).fillna(1)  # Default difficulty 1 if missing

# Compute weighted score with difficulty factor
df['Score'] = (df['Take Count'] * 4) + (df['Take Length'] * 1) + (df['Watches'] * 2) + (df['Module Average Difficulty'] * 3)

df['Rank'] = df.groupby('Cohort')['Score'].rank(ascending=False, method='dense')
df = df.sort_values(by=['Cohort', 'Rank'])

# Save ranked results
output_path = "/Users/chuyinghuo/Downloads/BetterOn/ranked_output.csv"
df.to_csv(output_path, index=False)

print(f"Ranked data saved to {output_path}")
