import requests
import pandas as pd

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


url = "https://www.otodom.pl/_next/data/Jar5lZW7hsz3OyHbE0mIz/pl/wyniki/wynajem/mieszkanie/wielkopolskie/poznan.json"

params = {
    "searchingCriteria": ["wynajem", "mieszkanie", "wielkopolskie", "poznan"],
    "page": "1"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "x-nextjs-data": "1"
}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("Success! JSON data fetched.")

    # Inspecting the data layers
    print("Root keys:", data.keys())
    print("pageProps keys:", data['pageProps'].keys())
    print("searchAds structure:", data['pageProps']['data']['searchAds'].keys())

    apartments_list = data['pageProps']['data']['searchAds']['items']
    print(len(apartments_list))

    first_ad = apartments_list[0]
    print(first_ad.keys())

    parsed_data = []
    location = apartments_list[0].get('location')

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
        parsed_data.append(apartment_data)

    df = pd.DataFrame(parsed_data)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)

else:
    print(f"Access denied or error occurred. Status code: {response.status_code}")