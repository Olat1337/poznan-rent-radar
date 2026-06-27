import requests

url = "https://www.otodom.pl/_next/data/Jar5lZW7hsz3OyHbE0mIz/pl/wyniki/wynajem/mieszkanie/wielkopolskie/poznan.json"

params = {
    "searchingCriteria": ["wynajem", "mieszkanie", "wielkopolskie", "poznan"],
    "page": "2"
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

else:
    print(f"Access denied or error occurred. Status code: {response.status_code}")