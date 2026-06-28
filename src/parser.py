import time
import requests
import pandas as pd
import logging

logging.basicConfig(filename='../scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
TARGET_URL = "https://www.otodom.pl/_next/data/Jar5lZW7hsz3OyHbE0mIz/pl/wyniki/wynajem/mieszkanie/wielkopolskie/poznan.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "x-nextjs-data": "1"
}

def scrape_poznan_rent():
    logging.info("Starting scraper...")

    all_scraped_data = []

    first_page_json = fetch_page_data(TARGET_URL, 1, HEADERS)
    if not first_page_json:
        logging.error("Could not fetch page 1. Exiting.")
        return

    total_pages = first_page_json['pageProps']['data']['searchAds']['pagination'].get('totalPages', 1)
    logging.info(f"Found {total_pages} total pages to scrape!")

    for current_page in range(1, total_pages + 1):
        logging.info(f"Scraping page {current_page}...")
        page_json = fetch_page_data(TARGET_URL, current_page, HEADERS)

        if page_json:
            try:
                raw_apartments = page_json['pageProps']['data']['searchAds']['items']
            except KeyError:
                logging.warning(f"Data missing on page {current_page}")
                raw_apartments = []
            cleaned_apartments = parse_apartments(raw_apartments)
            all_scraped_data.extend(cleaned_apartments)

        time.sleep(2)

    df = pd.DataFrame(all_scraped_data)
    logging.info(f"Scraping complete! Final dataset shape: {df.shape}")

    df.to_csv("../data/raw_rent_data.csv", index=False)
    logging.info("Saved to data/raw_rent_data.csv")

def fetch_page_data(url, page_number, headers):
    params = {
        "searchingCriteria": ["wynajem", "mieszkanie", "wielkopolskie", "poznan"],
        "page": str(page_number)
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        logging.error(f"Failed to fetch page {page_number}. Error: {exc}")
        return None

def get_neighborhood(location_data):
    if not location_data:
        return None

    reverse_geo = location_data.get("reverseGeocoding")
    if not reverse_geo:
        return None

    locations_list = reverse_geo.get("locations", [])

    district = None
    residential = None
    for loc in locations_list:
        if loc.get('locationLevel') == 'district':
            district = loc.get('name')
        if loc.get('locationLevel') == 'residential':
            residential = loc.get('name')

    return residential if residential else district

def parse_apartments(apartments_list):
    page_data = []
    for apartment in apartments_list:
        tags = [tag.get('value') for tag in apartment.get("tags", [])]

        apartment_data = {
            "id": apartment.get("id"),
            "title": apartment.get("title"),
            "total_price": apartment.get("totalPrice"),
            "rent_price": apartment.get("rentPrice"),
            "area": apartment.get("areaInSquareMeters"),
            "rooms": apartment.get("roomsNumber"),
            "floor": apartment.get("floorNumber"),
            "isPrivateOwner": apartment.get("isPrivateOwner"),
            "location": get_neighborhood(apartment.get("location")),

            "has_ac": "AIR_CONDITIONING" in tags,
            "has_balcony": "BALCONY" in tags,
            "has_terrace": "TERRACE" in tags,
            "has_parking": "PARKING_SPOT" in tags,
            "has_storage": "STORAGE_ROOM" in tags,
            "is_secure": "SECURE_BUILDING" in tags
        }
        page_data.append(apartment_data)

    return page_data

if __name__ == "__main__":
    scrape_poznan_rent()