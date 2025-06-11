# 🌍 ETL Project – Country GDP Data, but With Style

## 🧠 Overview
This project is a full ETL (Extract, Transform, Load) pipeline built to turn raw Country GDP data into clean, structured insights.

We extract a table from the web, enhance it with real-world exchange rates, and load the final product into both a CSV file and a local SQLite database — all while keeping detailed logs of every step.

Because data science without traceability is just expensive guessing.

---

## 🗂️ Project Structure
```
project_root/
│
├── data/                     # Raw and processed data lives here
│   ├── exchange_rates.csv    # Daily exchange rates
│   └── output/               # Output directory for transformed results
│       └── country_gdp_transformed.csv
│
├── logs/                     # ETL process logs
│   ├── etl_progress.log
│   ├── test_extract.log
│   ├── test_transform.log
│   └── test_db_operations.log
│
├── src/                      # Core ETL logic
│   ├── extractor.py          # Extracts data from the web
│   ├── transformer.py        # Handles currency conversion & transformation
│   ├── loader.py             # Loads data into CSV and SQLite
│   └── main.py               # Orchestrates the ETL pipeline
│
├── tests/                    # Test suite
│   └── __init__.py
│
├── .gitignore                # Files to ignore in version control
├── README.md                 # You're reading it
└── requirements.txt          # Project dependencies
```

---

## 📦 Requirements
- Python 3.x
- Packages used:
  - `requests`
  - `pandas`
  - `beautifulsoup4`
  - `lxml`
  - `html5lib`

Install them all with:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Use

1. Make sure `exchange_rates.csv` is present in the `data/` directory.
2. Run the main script to launch the ETL process:

```bash
python src/main.py
```

The output will be stored in `data/output/`, and a SQLite database will be updated or created alongside it.

---

## 📝 Logging

Every action the pipeline takes — from extraction to transformation to loading — is logged with timestamps. You’ll find those logs in the `logs/` folder, neatly organized by stage.

---

## ⚖️ License

This project is licensed under the MIT License.  
Feel free to use, modify, break, or build upon it — just don't forget to give credit where credit is due.