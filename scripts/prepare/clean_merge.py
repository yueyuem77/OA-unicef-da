import pandas as pd
from pathlib import Path
import re
import sys

def strip_colnames(df):
    ''''Remove the human-readable part of column names, e.g. "OBS_VALUE: Value" → "OBS_VALUE"'''
    df = df.rename(columns=lambda c: c.split(':', 1)[0].strip())
    
    # print("  ➤ Columns after strip:", list(df.columns))
    return df


def load_and_clean(dataset_name, raw_path, out_path):
    print(f"Loading {dataset_name} data...")
    df = pd.read_csv(raw_path / f"{dataset_name}.csv")
    print(f"  ➤ Loaded {df.shape[0]} rows, {df.shape[1]} columns")

    print("Cleaning column names...")
    df = strip_colnames(df)
    df['year'] = df['TIME_PERIOD'].astype(int)

    print("Cleaning the ISO3 codes...")
    df['iso3'] = df['REF_AREA'].str.split(':').str[0].str.strip()
    # Keep only 3-letter codes (likely ISO3)
    before = df.shape[0]
    df = df[df['iso3'].str.fullmatch(r'[A-Z]{3}')]
    after = df.shape[0]
    print(f"  ➤ Dropped non-ISO3 rows: {before - after} ({before} → {after})")
  

    # Keep only most recent year per country
    df = df.sort_values(['iso3', 'year'], ascending=[True, False])
    df = df.drop_duplicates(subset='iso3')
    print(f"  ➤ Kept most recent year per country: {df.shape[0]} rows")

    print(f"Saving cleaned data to {out_path / f'{dataset_name}_cleaned.csv'}")
    df.to_csv(out_path / f"{dataset_name}_cleaned.csv", index=False)
    
    return df

def merge_all(anc4, sba, raw_path, out_path):
    print("Merging ANC4, SAB, births, and track-status data...")

    # Merge ANC4 and SAB on iso3 and year
    merged = anc4.merge(sba, on=['iso3', 'year'], suffixes=('_anc4', '_sab'))
    merged = merged.rename(columns={
        'OBS_VALUE_anc4': 'anc4_coverage',
        'OBS_VALUE_sab': 'sab_coverage'
    })
    merged = merged[['iso3', 'year', 'anc4_coverage', 'sab_coverage']]
    merged.to_csv(out_path / f"merged_anc4_sab_cleaned.csv", index=False)
    print(f"  ➤ Merged ANC4 & SAB: {merged.shape[0]} rows")

    # Load births
    births_file = raw_path / "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"
    births = pd.read_excel(births_file,sheet_name= "Projections" ,skiprows=16)
    births = births[births['Year'] == 2022].copy()
    births = births.rename(columns={
        'ISO3 Alpha-code': 'iso3',
        'Births (thousands)': 'births_2022'
    })[['iso3', 'births_2022']]
    merged = merged.merge(births, on='iso3', how='left')
    print(f"  ➤ Merged with births: {merged.shape[0]} rows")
    # print(merged.head())
    # Load status
    status_file = raw_path / "On-track and off-track countries.xlsx"
    status = pd.read_excel(status_file)
    status = status.rename(columns={
        'ISO3Code': 'iso3',
        'Status.U5MR': 'track_status'
    })[['iso3', 'track_status']]
    merged = merged.merge(status, on='iso3', how='left')
    print(f"  ➤ Merged with status: {merged.shape[0]} rows")

    # Save final merged file
    out_file = out_path / "coverage_2022_merged.csv"
    merged.to_csv(out_file, index=False)
    print(f"  ✅ Final merged dataset saved to: {out_file}")
    return merged

def main():

    ROOT     = Path.cwd()
    print("Root directory:", ROOT)
    RAW  = ROOT / "data" / "raw"
    OUT  = ROOT / "data" / "interim"    
    OUT.mkdir(parents=True, exist_ok=True)

    birth_file_name = "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"
    # Load & clean
    anc4 = load_and_clean('ANC4_2018_2022', RAW, OUT)
    sba = load_and_clean('SAB_2018_2022', RAW, OUT)
    merged = merge_all(anc4, sba, RAW, OUT)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)
