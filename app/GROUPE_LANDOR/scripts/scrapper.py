from pathlib import Path

import requests
from bs4 import BeautifulSoup
import os

url = "https://www.cmf.tn/?q=consultation-des-tats-financier-des-soci-t-s-faisant-ape"

params = {
    "field_societesape_value": "GROUPE LAND'OR",
    "page": 0
}


# Build save_dir relative to this file's location
BASE_DIR = Path(__file__).resolve().parents[3]  # go up to FiscalTrack
save_dir = BASE_DIR / "input" / "GROUPE LANDOR"

os.makedirs(save_dir, exist_ok=True)

MIN_YEAR = 2014
MAX_YEAR = 2024

page = 0
while True:
    params["page"] = page
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.find_all("div", class_="views-row")
    if not rows:
        print("No more rows on page", page)
        break

    for row in rows:
        # Extract year
        year_div = row.select_one(".field-name-field-exercice .field-item")
        if not year_div:
            continue

        try:
            year = int(year_div.text.strip())
        except:
            continue

        # Filter by year
        if not (MIN_YEAR <= year <= MAX_YEAR):
            continue

        # Extract PDF link
        pdf_tag = row.find("a", href=True)
        if not pdf_tag:
            continue

        pdf_link = pdf_tag["href"]
        if pdf_link.startswith("/"):
            pdf_link = "https://www.cmf.tn" + pdf_link

        pdf_data = requests.get(pdf_link).content
        filename = save_dir / f"LANDOR_{year}.pdf"

        with open(filename, "wb") as f:
            f.write(pdf_data)

        print(f"Saved: {filename}")

    page += 1

print("Finished downloading PDFs for years 2014–2024.")
