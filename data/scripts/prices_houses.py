import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib.parse

areas = [
    'el-poblado',
    'laureles',
    'envigado',
    'sabaneta',
    'belen',
    'robledo',
    'doce-de-octubre',
    'ciudad-del-rio',
    'guayabal',
    'manalita'
]

base_url = 'https://www.metrocuadrado.com/casas/venta/medellin/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

prices = []
areas_scraped = []
addresses = []
descriptions = []
listing_urls = []
sizes = []
bedrooms = []
bathrooms = []

def scrape_page(area, url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve page {url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    property_list = soup.find_all('div', class_='sc-jfzlTM jFwMm mb-3 col-12 col-sm-7 col-lg-4')  # Adjusted based on observed outer div

    for property_card in property_list:
        try:
            title = property_card.find('h3', class_='sc-ckVGcZ cFCiUO font-weight-light card-title').get_text(strip=True)
            addresses.append(title)
            areas_scraped.append(area.capitalize())

            price = property_card.find('span', class_='price').get_text(strip=True)
            prices.append(price)

            size = property_card.find('span', text='Área(m²)').find_next('span').get_text(strip=True)
            sizes.append(size)

            beds = property_card.find('span', text='Hab.').find_next('span').get_text(strip=True)
            bedrooms.append(beds)

            baths = property_card.find('span', text='Baños').find_next('span').get_text(strip=True)
            bathrooms.append(baths)

            description = property_card.find('p', class_='description').get_text(strip=True) if property_card.find('p', class_='description') else "No description"
            descriptions.append(description)

            link = property_card.find('a', href=True)['href']
            full_link = urllib.parse.urljoin(base_url, link)
            listing_urls.append(full_link)

        except AttributeError:
            classes = property_card.get('class')
            print(f"Missing information for card with classes: {classes}")

pages_per_area = 1  # Adjust based on the number of available pages

for area in areas:
    print(f"Scraping area: {area.capitalize()}")
    for page in range(1, pages_per_area + 1):
        if page == 1:
            url = f"{base_url}{area}/"
        else:
            url = f"{base_url}{area}/?page={page}"

        print(f"  Scraping page {page} for {area.capitalize()}...")
        scrape_page(area, url)
        time.sleep(1)  # Be courteous with a short delay between requests

df = pd.DataFrame({
    'Area': areas_scraped,
    'Price': prices,
    'Address': addresses,
    'Description': descriptions,
    'Size (m²)': sizes,
    'Bedrooms': bedrooms,
    'Bathrooms': bathrooms,
    'Listing URL': listing_urls
})

print(df.head())

df.to_csv('medellin_rent_prices_by_area.csv', index=False)
print("Data saved to 'medellin_rent_prices_by_area.csv'")
