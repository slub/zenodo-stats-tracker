import requests
import csv
import os
import glob
from datetime import datetime, timedelta

RECORDS_LIST = "config/records.txt"


def get_last_report_data():
    # Find the most recent stats file in the data folder
    files = sorted(glob.glob("data/stats_*.csv"))
    if not files:
        return {}

    last_data = {}
    with open(files[-1], mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["record_id"] != "GRAND TOTAL":
                last_data[row["record_id"]] = {
                    "v": int(row["all_time_views"]),
                    "uv": int(row["all_time_unique_views"]),
                    "d": int(row["all_time_downloads"]),
                    "ud": int(row["all_time_unique_downloads"]),
                }
    return last_data


def fetch_monthly_report():
    last_report = get_last_report_data()
    today = datetime.now()
    month_str = (today.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")

    with open(RECORDS_LIST, "r") as f:
        ids = [line.strip() for line in f if line.strip()]

    report_rows = []
    grand_totals = [0] * 8

    for rid in ids:
        res = requests.get(f"https://zenodo.org/api/records/{rid}")
        if res.status_code == 200:
            stats = res.json().get("stats", {})
            # New Cumulative
            cv, cuv = stats.get("views", 0), stats.get("unique_views", 0)
            cd, cud = stats.get("downloads", 0), stats.get("unique_downloads", 0)

            # Calculate Delta (Current - Last Month's All Time)
            prev = last_report.get(rid, {"v": 0, "uv": 0, "d": 0, "ud": 0})
            mv, muv = cv - prev["v"], cuv - prev["uv"]
            md, mud = cd - prev["d"], cud - prev["ud"]

            row = [rid, mv, muv, md, mud, cv, cuv, cd, cud]
            report_rows.append(row)
            for i in range(len(row) - 1):
                grand_totals[i] += row[i + 1]

    filename = f"data/stats_{month_str}.csv"
    with open(filename, mode="w", newline="") as f:
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
    fetch_monthly_report()
