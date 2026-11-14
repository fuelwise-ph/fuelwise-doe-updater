
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote

URL = (
    "https://doe.gov.ph/data-and-prices/"
    "liquid-fuels/retail-pump-prices/"
    "south-luzon-pump-prices"
)

response = requests.get(URL, timeout=60)
response.raise_for_status()

print("HTTP Status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

reports = []

for link in soup.find_all("a", href=True):
    href = urljoin(URL, link["href"])
    decoded = unquote(href)

    if "calabarzon" in decoded.lower() and ".pdf" in decoded.lower():
        if href not in reports:
            reports.append(href)

print("\nDETECTED CALABARZON REPORTS")

for report in reports[:20]:
    print(unquote(report))

print("\nTotal reports detected:", len(reports))

from datetime import datetime
import re

dated_reports = []

for report in reports:
    decoded = unquote(report)

    match = re.search(
        r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})",
        decoded
    )

    if match:
        try:
            day, month, year = match.groups()

            report_date = datetime.strptime(
                f"{day} {month[:3]} {year}",
                "%d %b %Y"
            )

            dated_reports.append((report_date, report))

        except ValueError:
            continue

if dated_reports:
    latest_date, latest_url = max(
        dated_reports,
        key=lambda item: item[0]
    )

    print("\nLATEST DATED CALABARZON REPORT")
    print("Period end:", latest_date.strftime("%Y-%m-%d"))
    print("PDF URL:", latest_url)

    import json

    report_data = {
        "region": "CALABARZON",
        "source": "Department of Energy",
        "period_end": latest_date.strftime("%Y-%m-%d"),
        "pdf_url": latest_url
    }

    with open("latest_report.json", "w") as file:
        json.dump(report_data, file, indent=4)

    print("JSON file created: latest_report.json")

else:
    print("WARNING: No dated reports found.")

if not reports:
    raise RuntimeError("No CALABARZON reports detected.")

print("Report discovery test completed.")
