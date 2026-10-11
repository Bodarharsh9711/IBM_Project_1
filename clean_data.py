import pandas as pd

INPUT_FILE = "sample_data.csv"
OUTPUT_FILE = "cleaned_data.csv"

# ── 1. Load ────────────────────────────────────────────────────────────────────
df = pd.read_csv(INPUT_FILE)

print("=== Raw data ===")
print(df.to_string(index=False))
print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
print("\nMissing values per column:")
print(df.isnull().sum().to_string())

# ── 2. Fix dtypes before filling ───────────────────────────────────────────────
df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce")

# ── 3. Fill missing values ─────────────────────────────────────────────────────
# Numeric: fill with column median
df["age"] = df["age"].fillna(df["age"].median()).astype(int)
df["salary"] = df["salary"].fillna(df["salary"].median()).astype(int)

# Categorical: fill with the most frequent value (mode)
df["name"] = df["name"].fillna("Unknown")
df["email"] = df["email"].fillna("no-email@example.com")
df["department"] = df["department"].fillna(df["department"].mode()[0])

# Date: fill with the median hire date
median_date = df["hire_date"].dropna().sort_values().iloc[len(df["hire_date"].dropna()) // 2]
df["hire_date"] = df["hire_date"].fillna(median_date)

# ── 4. Remove duplicate rows (if any) ─────────────────────────────────────────
before_dedup = len(df)
df = df.drop_duplicates()
removed = before_dedup - len(df)
if removed:
    print(f"\nRemoved {removed} duplicate row(s).")

# ── 5. Validate ────────────────────────────────────────────────────────────────
# Age must be a plausible working age (18–80)
invalid_age = df[(df["age"] < 18) | (df["age"] > 80)]
if not invalid_age.empty:
    print(f"\nWarning: {len(invalid_age)} row(s) with age outside 18–80:")
    print(invalid_age[["id", "name", "age"]].to_string(index=False))

# Salary must be positive
invalid_salary = df[df["salary"] <= 0]
if not invalid_salary.empty:
    print(f"\nWarning: {len(invalid_salary)} row(s) with non-positive salary.")

# ── 6. Report ──────────────────────────────────────────────────────────────────
print("\n=== Cleaned data ===")
print(df.to_string(index=False))
print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
print("\nMissing values after cleaning:")
print(df.isnull().sum().to_string())

# ── 7. Save ────────────────────────────────────────────────────────────────────
df.to_csv(OUTPUT_FILE, index=False, date_format="%Y-%m-%d")
print(f"\nCleaned data saved to '{OUTPUT_FILE}'.")
