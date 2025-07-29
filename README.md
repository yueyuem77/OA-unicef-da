# UNICEF Maternal Health Coverage Analysis

## This repository was created as part of a take-home data analysis assessment for the **Consultancy, Data & Analytics** position at UNICEF. It contains a full end-to-end workflow for analyzing maternal health coverage metrics across countries and generating a reproducible report.
Postion Applied: Administrative Data Analyst – Req. #581696
---

## 📁 Project Structure

```
Consultancy-Assessment/
├── data/
│   ├── raw/                  # Original input files (CSV/XLSX)
│   └── interim/              # Cleaning and merging datasets for validation
│   └── processed/            # Final Cleaned and merged datasets

├── outputs/
│   ├── weighted_results.csv  # Population-weighted averages by group
│   └── weighted_plot.png     # Visualization comparing coverage
├── scripts/
│   ├── pipeline.py       # Cleaning + merging all input data
│   └── weighted_coverage.py # Weighted calculation + plotting
├── notebooks/
│   └── report.ipynb # Final report notebook
├── README.md
└── requirements.txt
└── run_project.py            #executes the workflow end-to-end, producing the final output 
```

---

## 📊 Indicators

- **ANC4**: % of women (15–49) with ≥4 antenatal care visits  
- **SBA**: % of deliveries attended by skilled health personnel  
- **Births**: Projected live births in 2022 (UN WPP)  
- **Track Status**: On-track or off-track (based on U5MR classification)

---

## 🚀 How to Reproduce

### 1. Clone the repository

```bash
git clone https://github.com/yueyuem77/OA-unicef-da.git
cd your-repo-name
```

### 2. Load user profile: include create venv and install dependencies

```bash
source user_profile.sh
```

> If `country_converter` is used, make sure to install:
```bash
pip install country_converter
```
Place this file in the root directory and define variables like:

```bash
# user_profile.sh
export DATA_PATH="./data"
export REPORT_AUTHOR="First Last"
```

You can then access these environment variables in your Python scripts using:

```bash
import os
data_path = os.environ.get("DATA_PATH")
```

---

### 3. Run the full pipeline (ETL + analysis + reporting)

```bash
python run_project.py
```

This script:
- Cleans and merges raw ANC4, SBA, and births data
- Computes population-weighted coverage for each group (on-track/off-track)
- Exports the final HTML report include the Data Visualization and an Analysis

---

### 4. View the report

Open this file in your browser:

```
notebooks/report.html
```

---

## ✅ Notes

- Only country-level ISO3 codes were retained in the merged datasets
- Projected births from 2022 are used as weights
- All intermediate files are available for validation in `data/interim/` and final outputs in `data/processed/` and `outputs/`


