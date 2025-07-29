# UNICEF Maternal Health Coverage Analysis

This repository contains a data processing and analysis pipeline to assess maternal health coverage across countries, using population-weighted indicators for antenatal care and skilled birth attendance. The project focuses on comparing coverage between "on-track" and "off-track" countries based on under-five mortality classifications.

---

## 📁 Project Structure

```
Consultancy-Assessment/
├── data/
│   ├── raw/                  # Original input files (CSV/XLSX)
│   └── interim/              # Cleaned and merged datasets
├── outputs/
│   ├── weighted_results.csv  # Population-weighted averages by group
│   └── weighted_plot.png     # Visualization comparing coverage
├── scripts/
│   ├── prepare/
│   │   └── pipeline.py       # Cleaning + merging all input data
│   └── analysis/
│       └── weighted_coverage.py # Weighted calculation + plotting
├── notebooks/
│   └── 02_weighted_coverage_report.ipynb # Final report notebook
├── README.md
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
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create virtual environment & install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> If `country_converter` is used, make sure to install:
```bash
pip install country_converter
```

### 3. Run the data preparation pipeline

```bash
python scripts/prepare/pipeline.py
```

This loads, cleans, and merges:
- ANC4 and SBA datasets
- 2022 births projection from UN WPP
- On-/off-track country status

Outputs: `data/interim/coverage_2022_merged.csv`

---

### 4. Run the analysis

```bash
python scripts/analysis/weighted_coverage.py
```

This computes population-weighted coverage for on-track and off-track groups and saves the final plot and results to the `outputs/` folder.

---

### 5. View the report

Open the final HTML report:
```
notebooks/02_weighted_coverage_report.html
```

---

## ✅ Notes

- All intermediate data files are saved to the `interim/` and `outputs/` folders for transparency and reproducibility.
- The pipeline assumes that all raw files are correctly placed under `data/raw/`.

---

## 📄 License

This repository is provided for assessment and educational purposes.
