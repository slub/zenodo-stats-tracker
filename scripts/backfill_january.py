import requests
import csv
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

RECORDS_LIST = "config/records.txt"
OUTPUT_FILE = "data/stats_2026-01.csv"


def get_record_ids():
    with open(RECORDS_LIST, "r") as f:
        return [line.strip() for line in f if line.strip()]


def create_january_report():
    os.makedirs("data", exist_ok=True)
    ids = get_record_ids()
    target_date = datetime(2026, 1, 31)

    report_rows = []
    grand_totals = [0] * 8  # To track all columns

    for rid in ids:
        response = requests.get(f"https://zenodo.org/api/records/{rid}")
        if response.status_code == 200:
            data = response.json()
            stats = data.get("stats", {})

            # Calculate months since creation
            created_str = data.get("created").split("T")[0]
            created_dt = datetime.strptime(created_str, "%Y-%m-%d")
            diff = relativedelta(target_date, created_dt)
            months_active = (
                (diff.years * 12) + diff.months + 1
            )  # +1 to include partial first month

            # Totals from API (Cumulative)
            cum_v = stats.get("views", 0)
            cum_uv = stats.get("unique_views", 0)
            cum_d = stats.get("downloads", 0)
            cum_ud = stats.get("unique_downloads", 0)

            # Monthly Averages (Estimated for January)
            m_v, m_uv = int(cum_v / months_active), int(cum_uv / months_active)
            m_d, m_ud = int(cum_d / months_active), int(cum_ud / months_active)

            row = [rid, m_v, m_uv, m_d, m_ud, cum_v, cum_uv, cum_d, cum_ud]
            report_rows.append(row)
            for i in range(len(row) - 1):
                grand_totals[i] += row[i + 1]

    with open(OUTPUT_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "record_id",
                "month_views",
                "month_unique_views",
                "month_downloads",
                "month_unique_downloads",
                "all_time_views",
                "all_time_unique_views",
                "all_time_downloads",
                "all_time_unique_downloads",
            ]
        )
        writer.writerows(report_rows)
        writer.writerow(["GRAND TOTAL"] + grand_totals)


if __name__ == "__main__":
    create_january_report()
