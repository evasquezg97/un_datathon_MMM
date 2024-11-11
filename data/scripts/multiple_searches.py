import argparse
import pandas as pd
import sys
sys.path.append('.')
import os
import logging
from src.scrapper import main as scrape_main

# Configure logging
logging.basicConfig(
    filename='data_collection.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define diversified categories with focused search terms for a balanced dataset
categories = {
    "parks": ["Parks in Medellin", "Local parks in Medellin"],
    "nature_reserves": ["Nature reserves in Medellin", "Protected natural areas in Medellin"],
    "eco_cafes": ["Eco-friendly cafes in Medellin", "Organic cafes Medellin", "Sustainable cafes in Medellin"],
    "local_restaurants": ["Local restaurants in Medellin", "Family-owned restaurants Medellin", "Farm-to-table restaurants Medellin"],
    "organic_markets": ["Organic markets in Medellin", "Farmers markets Medellin", "Eco markets Medellin"],
    "museums": ["Museums in Medellin", "Cultural museums Medellin"],
    "art_galleries": ["Art galleries in Medellin", "Local art spaces Medellin"],
    "theaters": ["Theaters in Medellin", "Local theater groups Medellin"],
    "community_centers": ["Community centers in Medellin", "Local community hubs Medellin"],
    "plazas": ["Public plazas in Medellin", "Local plazas Medellin"],
    "sports_complexes": ["Sports complexes in Medellin", "Outdoor sports Medellin"],
    # New categories
    "zero_waste_stores": ["Zero waste stores in Medellin", "Plastic-free shops Medellin"],
    "eco_furniture_stores": ["Eco-friendly furniture stores Medellin", "Sustainable furniture Medellin"],
    "organic_beauty_stores": ["Organic beauty stores Medellin", "Natural cosmetics Medellin"],
    "recycled_products_shops": ["Recycled products shops Medellin", "Upcycled goods Medellin"],
    "vegan_restaurants": ["Vegan restaurants Medellin", "Plant-based eateries Medellin"],
    "health_food_stores": ["Health food stores Medellin", "Organic groceries Medellin"],
    "juice_bars": ["Organic juice bars Medellin", "Cold-pressed juice Medellin"],
    "wellness_centers": ["Wellness centers in Medellin", "Holistic health Medellin"],
    "yoga_studios": ["Yoga studios Medellin", "Eco-friendly yoga classes Medellin"],
    "meditation_centers": ["Meditation centers Medellin", "Mindfulness centers Medellin"],
    "bike_shops": ["Bicycle shops Medellin", "Sustainable bike shops Medellin"],
    "ev_charging_stations": ["Electric vehicle charging stations Medellin", "EV charging Medellin"],
    "recycling_centers": ["Recycling centers in Medellin", "Waste management Medellin"],
    "renewable_energy_companies": ["Renewable energy companies Medellin", "Solar energy Medellin"],
    "green_tech_companies": ["Green tech companies Medellin", "Eco-friendly tech startups Medellin"],
    "eco_cleaning_services": ["Eco-friendly cleaning services Medellin", "Green cleaning Medellin"],
    "community_gardens": ["Community gardens Medellin", "Urban farming Medellin"],
    "eco_hotels": ["Eco-friendly hotels Medellin", "Sustainable accommodations Medellin"],
    "local_breweries": ["Local breweries Medellin", "Craft beer Medellin"],
    "art_workshops": ["Art workshops Medellin", "Sustainable art studios Medellin"],
    "cultural_centers": ["Cultural centers Medellin", "Environmental cultural centers Medellin"],
    "health_clinics": ["Health clinics in Medellin", "Organic health clinics Medellin"],
    "mental_health_centers": ["Mental health centers Medellin", "Eco-friendly mental health services Medellin"],
    "environmental_ngos": ["Environmental NGOs Medellin", "Sustainability advocacy groups Medellin"],
    "eco_tours": ["Eco-tours Medellin", "Sustainable tourism Medellin"],
    "artisan_shops": ["Artisan shops Medellin", "Handmade crafts Medellin"],
    "sustainable_event_venues": ["Sustainable event venues Medellin", "Eco-friendly event spaces Medellin"],
    "organic_pet_stores": ["Organic pet stores Medellin", "Natural pet supplies Medellin"],
    "green_building_firms": ["Green construction firms Medellin", "Eco-friendly architecture Medellin"],
    "local_sports_clubs": ["Local sports clubs Medellin", "Sustainable sports facilities Medellin"],
    "green_coworking_spaces": ["Green coworking spaces Medellin", "Eco-friendly coworking Medellin"],
    "environmental_learning_centers": ["Environmental learning centers Medellin", "Sustainability training institutes Medellin"],
    # Add more categories as needed
}

def collect_data_for_category(category_name, search_terms, total, output_dir='categories_data'):
    """Collect data for a specific category with diversified search terms and save individually."""
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Initialize empty DataFrame for the category
    category_df = pd.DataFrame()

    # Calculate entries per search term
    entries_per_term = total // len(search_terms)

    for term in search_terms:
        try:
            logging.info(f"Collecting data for category '{category_name}' with search term '{term}'")
            scrape_main(output_path='temp_result.csv', search_for=term, total=entries_per_term)

            # Load the scraped data
            temp_df = pd.read_csv('temp_result.csv')
            logging.info(f"Collected {len(temp_df)} entries for search term '{term}' in category '{category_name}'")

            # Append to category DataFrame
            category_df = pd.concat([category_df, temp_df], ignore_index=True)

            # Remove temporary file
            os.remove('temp_result.csv')

        except Exception as e:
            logging.error(f"Error collecting data for category '{category_name}' with search term '{term}': {e}")
            continue  # Skip to the next search term

    if not category_df.empty:
        # Tag with category name
        category_df["Category"] = category_name

        # Save the category data
        category_output_path = os.path.join(output_dir, f"{category_name}.csv")
        category_df.to_csv(category_output_path, index=False, encoding='utf-8-sig')
        logging.info(f"Saved data for category '{category_name}' to '{category_output_path}'")
    else:
        logging.warning(f"No data collected for category '{category_name}'")

    return category_df

def normalize_and_rename_columns(df):
    """Normalize column names to lowercase and rename specific columns."""
    # Normalize column names to lowercase
    df.columns = df.columns.str.lower()

    # Rename 'names' to 'name' if it exists
    if 'names' in df.columns:
        df = df.rename(columns={'names': 'name'})

    # Rename other columns if necessary (example: 'phone number' to 'phone')
    rename_mapping = {
        'phone number': 'phone'
        # Add other mappings if needed
    }
    df = df.rename(columns=rename_mapping)

    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connected Parches Data Collection Script")
    parser.add_argument("-t", "--total", type=int, default=1000, help="Total entries across all categories")
    parser.add_argument("-o", "--output", type=str, default='final_result.csv', help="Final output CSV path")
    parser.add_argument("-d", "--output_dir", type=str, default='categories_data', help="Directory to save individual category CSVs")
    args = parser.parse_args()

    total_entries = args.total
    final_output_path = args.output
    output_dir = args.output_dir

    all_data = pd.DataFrame()

    # Calculate entries per category to ensure balanced dataset
    entries_per_category = total_entries // len(categories)
    logging.info(f"Starting data collection for {len(categories)} categories with {entries_per_category} entries each.")

    # Loop through each category and collect data
    for category, search_terms in categories.items():
        logging.info(f"Processing category: {category}")
        category_data = collect_data_for_category(category, search_terms, entries_per_category, output_dir=output_dir)

        if not category_data.empty:
            all_data = pd.concat([all_data, category_data], ignore_index=True)
        else:
            logging.warning(f"No data to append for category '{category}'")

    # Normalize and rename columns
    all_data = normalize_and_rename_columns(all_data)

    # Define required columns
    required_columns = {"name", "address", "description"}

    # Check for required columns (case-insensitive and after renaming)
    lower_columns = set(all_data.columns)
    missing_columns = required_columns - lower_columns

    if missing_columns:
        logging.error(f"The following required columns are missing: {missing_columns}")
        print(f"Error: The following required columns are missing: {missing_columns}")
        print("Please check the scraper implementation to ensure these fields are being populated correctly.")
    else:
        # Clean the compiled dataset
        initial_count = len(all_data)
        all_data.drop_duplicates(subset=["name", "address", "description"], inplace=True)
        final_count = len(all_data)
        logging.info(f"Dropped {initial_count - final_count} duplicate entries.")

        # Ensure descriptions are not truncated
        all_data["description"] = all_data["description"].apply(lambda x: x if isinstance(x, str) else "")

        # Save the final cleaned dataset with complete descriptions
        all_data.to_csv(final_output_path, index=False, encoding='utf-8-sig')
        logging.info(f"Final dataset saved to '{final_output_path}' with {len(all_data)} entries.")
        print(f"Final dataset saved to {final_output_path} with {len(all_data)} entries.")
