import time
import requests
import pandas as pd
import logging
import re

logging.basicConfig(filename='../scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Base URL to fetch the HTML and extract the Build ID
BASE_HTML_URL = "https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/wielkopolskie/poznan"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "x-nextjs-data": "1"
}


def get_current_build_id():
    """Fetches the main HTML page and extracts the dynamic Next.js Build ID."""
    logging.info("Fetching current Next.js Build ID...")
    try:
        response = requests.get(BASE_HTML_URL, headers={"User-Agent": HEADERS["User-Agent"]}, timeout=20)
        response.raise_for_status()

        # Next.js stores the build ID inside the __NEXT_DATA__ script tag
        match = re.search(r'"buildId":"([^"]+)"', response.text)
        if match:
            build_id = match.group(1)
            logging.info(f"Successfully extracted Build ID: {build_id}")
            return build_id
        else:
            logging.error("Could not find 'buildId' in the HTML response.")
            return None
    except requests.RequestException as exc:
        logging.error(f"Failed to fetch base HTML page to get Build ID. Error: {exc}")
        return None


def scrape_poznan_rent():
    logging.info("Starting scraper...")

    # 1. Dynamically get the Build ID
    build_id = get_current_build_id()
    if not build_id:
        logging.error("Exiting because Build ID could not be found.")
        return

    # 2. Construct the dynamic Target URL
    dynamic_target_url = f"https://www.otodom.pl/_next/data/{build_id}/pl/wyniki/wynajem/mieszkanie/wielkopolskie/poznan.json"

    all_scraped_data = []

    # 3. Fetch the first page using the dynamic URL
    first_page_json = fetch_page_data(dynamic_target_url, 1, HEADERS)
    if not first_page_json:
        logging.error("Could not fetch page 1. Exiting.")
        return

    total_pages = first_page_json['pageProps']['data']['searchAds']['pagination'].get('totalPages', 1)
    logging.info(f"Found {total_pages} total pages to scrape!")

    # 4. Loop through all pages
    for current_page in range(1, total_pages + 1):
        logging.info(f"Scraping page {current_page}...")
        page_json = fetch_page_data(dynamic_target_url, current_page, HEADERS)

        if page_json:
            try:
                raw_apartments = page_json['pageProps']['data']['searchAds']['items']
            except KeyError:
                logging.warning(f"Data missing on page {current_page}")
                raw_apartments = []

            cleaned_apartments = parse_apartments(raw_apartments)
            all_scraped_data.extend(cleaned_apartments)

        time.sleep(2)

    # 5. Save the data
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