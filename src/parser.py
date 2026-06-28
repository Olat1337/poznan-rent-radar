import time
import requests
import pandas as pd

TARGET_URL = "https://www.otodom.pl/_next/data/Jar5lZW7hsz3OyHbE0mIz/pl/wyniki/wynajem/mieszkanie/wielkopolskie/poznan.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "x-nextjs-data": "1"
}

def scrape_poznan_rent():
    print("Starting scraper...")

    all_scraped_data = []

    first_page_json = fetch_page_data(TARGET_URL, 1, HEADERS)
    if not first_page_json:
        print("Could not fetch page 1. Exiting.")
        return

    total_pages = first_page_json['pageProps']['data']['searchAds']['pagination'].get('totalPages', 1)
    print(f"Found {total_pages} total pages to scrape!")

    for current_page in range(1, total_pages + 1):
        print(f"Scraping page {current_page}...")
        page_json = fetch_page_data(TARGET_URL, current_page, HEADERS)

        if page_json:
            raw_apartments = page_json['pageProps']['data']['searchAds']['items']
            cleaned_apartments = parse_apartments(raw_apartments)
            all_scraped_data.extend(cleaned_apartments)

        time.sleep(2)

    df = pd.DataFrame(all_scraped_data)
    print(f"Scraping complete! Final dataset shape: {df.shape}")

    df.to_csv("../data/raw_rent_data.csv", index=False)
    print("Saved to data/raw_rent_data.csv")

def fetch_page_data(url, page_number, headers):
    params = {
        "searchingCriteria": ["wynajem", "mieszkanie", "wielkopolskie", "poznan"],
        "page": str(page_number)
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch page {page_number}. Status: {response.status_code}")
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
        apartment_data = {
            "id": apartment.get("id"),
            "title": apartment.get("title"),
            "total_price": apartment.get("totalPrice"),
            "rent_price": apartment.get("rentPrice"),
            "area": apartment.get("areaInSquareMeters"),
            "rooms": apartment.get("roomsNumber"),
            "floor": apartment.get("floorNumber"),
            "isPrivateOwner": apartment.get("isPrivateOwner"),
            "location": get_neighborhood(apartment.get("location"))
        }
        page_data.append(apartment_data)
    return page_data

if __name__ == "__main__":
    scrape_poznan_rent()