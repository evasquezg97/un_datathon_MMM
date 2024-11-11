import pandas as pd
from geopy.geocoders import Nominatim, OpenCage
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from tqdm import tqdm
import time
import logging
import pickle
import os

# Configure logging
logging.basicConfig(
    filename='geocoding.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def load_cache(cache_file='geocoding_cache.pkl'):
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    else:
        return {}

def save_cache(cache, cache_file='geocoding_cache.pkl'):
    with open(cache_file, 'wb') as f:
        pickle.dump(cache, f)

def geocode_address_nominatim(geocoder, address):
    try:
        location = geocoder(address)
        print(location)
        if location:
            return (location.latitude, location.longitude)
        else:
            return (None, None)
    except (GeocoderServiceError, GeocoderTimedOut) as e:
        logging.error(f"Nominatim geocoding error for address '{address}': {e}")
        return (None, None)

def geocode_address_opencage(geocoder, address):
    try:
        location = geocoder.geocode(address)
        if location and location.geometry:
            return (location.geometry['lat'], location.geometry['lng'])
        else:
            return (None, None)
    except (GeocoderServiceError, GeocoderTimedOut) as e:
        logging.error(f"OpenCage geocoding error for address '{address}': {e}")
        return (None, None)

def main():
    # Load the dataset
    input_file = 'total.csv'
    output_file = 'final_result_with_coordinates.csv'

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        logging.error(f"Input file '{input_file}' not found.")
        print(f"Error: Input file '{input_file}' not found.")
        return

    # Check if 'address' column exists
    if 'address' not in df.columns:
        logging.error("The dataset does not contain an 'address' column.")
        print("Error: The dataset does not contain an 'address' column.")
        return

    # Initialize Nominatim Geocoder
    user_agent = "connected_parches_datathon"  # Replace with your project name
    nominatim_geolocator = Nominatim(user_agent=user_agent)

    # Initialize OpenCage Geocoder
    opencage_api_key = "YOUR_OPENCAGE_API_KEY"  # Replace with your OpenCage API key
    opencage_geolocator = OpenCage(opencage_api_key)

    # To respect Nominatim's rate limits, use RateLimiter
    nominatim_geocode = RateLimiter(nominatim_geolocator.geocode, min_delay_seconds=1, error_wait_seconds=5.0, max_retries=3, swallow_exceptions=False)

    # Initialize columns for coordinates
    df['latitude'] = None
    df['longitude'] = None

    # Load existing cache
    cache_file = 'geocoding_cache.pkl'
    geocoding_cache = load_cache(cache_file)

    # Iterate over the addresses with progress bar
    for idx, row in tqdm(df.iterrows(), total=df.shape[0], desc="Geocoding Addresses"):
        address = row['address']
        if pd.isnull(address) or address.strip() == "":
            logging.warning(f"Empty address for row index {idx}. Skipping geocoding.")
            continue

        if address in geocoding_cache:
            lat, lon = geocoding_cache[address]
            df.at[idx, 'latitude'] = lat
            df.at[idx, 'longitude'] = lon
            logging.info(f"Cache hit for address '{address}': (lat: {lat}, lon: {lon})")
            continue

        # Attempt geocoding with Nominatim
        lat, lon = geocode_address_nominatim(nominatim_geocode, address)

        # If Nominatim fails, attempt with OpenCage
        if lat is None or lon is None:
            logging.info(f"Falling back to OpenCage for address '{address}'")
            lat, lon = geocode_address_opencage(opencage_geolocator, address)
            print(lat, lon)
        # Update DataFrame and cache
        df.at[idx, 'latitude'] = lat
        df.at[idx, 'longitude'] = lon
        geocoding_cache[address] = (lat, lon)

        if lat is not None and lon is not None:
            logging.info(f"Geocoded address '{address}' to (lat: {lat}, lon: {lon})")
        else:
            logging.warning(f"Geocoding failed for address '{address}'. No location found.")

    save_cache(geocoding_cache, cache_file)

    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Geocoding completed. Enriched dataset saved to '{output_file}'.")
    logging.info(f"Geocoding completed. Enriched dataset saved to '{output_file}' with {len(df)} entries.")

if __name__ == "__main__":
    main()
