import pandas as pd
import sqlite3

RAW_FILE = "transactions.csv"
DB_FILE = "clean_finance.db"

def extract(path):
    """EXTRACT: read the raw CSV into a pandas DataFrame."""
    print("📥 Extracting data from", path)
    return pd.read_csv(path)

def quality_report(df):
    """Run data-quality checks and print what's wrong."""
    print("===== DATA QUALITY REPORT =====")
    print(f"Total rows read:         {len(df)}")
    print(f"Rows missing a date:     {df['date'].isna().sum()}")
    print(f"Rows missing an amount:  {df['amount'].isna().sum() + (pd.to_numeric(df['amount'], errors='coerce').isna() & df['amount'].notna()).sum()}")
    print(f"Duplicate rows:          {df.duplicated().sum()}")

def transform(df):
    """TRANSFORM: clean the data."""
    print("🧹 Transforming (cleaning) data...")

    # 1. Remove exact duplicate rows
    df = df.drop_duplicates()

    # 2. Convert 'amount' to numbers; bad values (like 'abc') become NaN
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    # 3. Drop rows that are missing a date or a valid amount
    df = df.dropna(subset=['date', 'amount'])

    print(f"✓ Clean rows remaining:  {len(df)}")
    return df

def load(df, db_path):
    """LOAD: write the clean data into an SQLite database."""
    print("💾 Loading clean data into", db_path)
    connection = sqlite3.connect(db_path)
    df.to_sql("transactions", connection, if_exists="replace", index=False)
    connection.close()
    print("Done! ✓")

if __name__ == "__main__":
    data = extract(RAW_FILE)
    quality_report(data)
    clean = transform(data)
    load(clean, DB_FILE)
