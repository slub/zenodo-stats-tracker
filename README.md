# Zenodo Stats Tracker

This repository automatically tracks monthly growth in views and downloads for specific Zenodo records.

## How it works
- **Data Source:** Every month, the script fetches the "All-Time" statistics from the Zenodo REST API.
- **Monthly Growth:** The script compares the new totals against the previous month's file. 
- **Delta Calculation:** `Monthly Stats = (Current All-Time Total) - (Previous Month All-Time Total)`
- **Output:** A new CSV file is generated in the `data/` folder for each month (e.g., `stats_2026-02.csv`).

## Management
- **Records:** To track new entries, add the Zenodo Record ID to `data/records.txt`.
- **Automation:** A GitHub Action runs on the 1st of every month to generate the report.
- **Totals:** Each file includes a **GRAND TOTAL** row representing the sum of all tracked records.
