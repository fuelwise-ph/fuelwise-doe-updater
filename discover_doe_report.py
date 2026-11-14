
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

if not reports:
    raise RuntimeError("No CALABARZON reports detected.")

print("Report discovery test completed.")
