import pandas as pd
import requests
from tqdm import tqdm
import time
import logging

N = 10

logging.basicConfig(
    filename='places_api.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_place_details(api_key, lat, lng, place_name):
    """Fetch place details including rating and reviews using Google Places API."""
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f"{lat},{lng}",
        'radius': 50,  # Adjust radius as needed
        'name': place_name,
        'key': api_key
    }
    try:
        res = requests.get(endpoint_url, params=params)
        res.raise_for_status()
        results = res.json().get('results')
        if not results:
            logging.warning(f"No results found for {place_name} at ({lat}, {lng})")
            return None, None
        place_id = results[0].get('place_id')
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            'place_id': place_id,
            'fields': 'rating,reviews',
            'key': api_key
        }
        details_res = requests.get(details_url, params=details_params)
        details_res.raise_for_status()
        details = details_res.json().get('result', {})
        rating = details.get('rating')
        reviews = details.get('reviews', [])
        # Concatenate the latest N reviews
        latest_reviews = [review.get('text') for review in reviews[:N]]
        concatenated_reviews = " | ".join(latest_reviews)
        return rating, concatenated_reviews
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred for {place_name}: {http_err}")
    except Exception as err:
        logging.error(f"Error occurred for {place_name}: {err}")
    return None, None

def main():
    # Load the dataset with coordinates
    input_file = 'final_result_with_coordinates.csv'
    output_file = 'final_result_with_reviews.csv'

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        logging.error(f"Input file '{input_file}' not found.")
        print(f"Error: Input file '{input_file}' not found.")
        return

    required_columns = {'latitude', 'longitude', 'name'}
    if not required_columns.issubset(df.columns):
        logging.error(f"Dataset missing required columns: {required_columns - set(df.columns)}")
        print(f"Error: Dataset missing required columns: {required_columns - set(df.columns)}")
        return

    api_key = "YOUR_GOOGLE_PLACES_API_KEY"  # Replace with your actual API key

    df['rating'] = None
    df['reviews'] = None

    # Iterate over each row to fetch ratings and reviews
    for idx, row in tqdm(df.iterrows(), total=df.shape[0], desc="Fetching Ratings and Reviews"):
        lat = row['latitude']
        lng = row['longitude']
        place_name = row['name']

        if pd.isnull(lat) or pd.isnull(lng) or pd.isnull(place_name):
            logging.warning(f"Missing data for row {idx}. Skipping.")
            continue

        rating, reviews = get_place_details(api_key, lat, lng, place_name)
        df.at[idx, 'rating'] = rating
        df.at[idx, 'reviews'] = reviews

        # Respect rate limits: Google Places API allows 50 requests per second
        # But to be safe, add a small delay
        time.sleep(0.05)

    # Save the enriched dataset
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    logging.info(f"Enriched dataset saved to '{output_file}'")
    print(f"Ratings and reviews fetched. Enriched dataset saved to '{output_file}'.")

if __name__ == "__main__":
    main()
