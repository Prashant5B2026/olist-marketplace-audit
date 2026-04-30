# Olist Marketplace Health Audit

Analysis of the Olist Brazilian E-Commerce dataset asking who drives customer trust loss on a multi-seller marketplace: the platform, sellers, or logistics.

Portfolio project in active development. The full case study lands on Day 5.

## Project structure

```
olist-marketplace-audit/
├── data/
│   ├── raw/              # 9 CSVs from the Olist Kaggle dataset (gitignored)
│   └── processed/        # SQLite DB (gitignored, built by src/ingest.py)
├── notebooks/            # numbered analysis notebooks
├── src/                  # reusable Python modules
├── reports/figures/      # exported charts for the README
├── requirements.txt
└── README.md
```

## Data

Raw CSVs are not committed to the repo. Download the Brazilian E-Commerce Public Dataset by Olist from Kaggle and place all 9 CSV files into `data/raw/`:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Then run `python -m src.ingest` to build `data/processed/olist.db`.

## Status

Day 1 of 5: scaffolding and data quality audit complete.
