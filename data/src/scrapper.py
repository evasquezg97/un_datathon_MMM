from playwright.sync_api import sync_playwright, TimeoutError
import pandas as pd
import argparse
import time
import re

names_list = []
address_list = []
website_list = []
phones_list = []
reviews_c_list = []
reviews_a_list = []
store_s_list = []
in_store_list = []
store_del_list = []
place_t_list = []
open_list = []
intro_list = []
reviews_text_list = []
descriptions_list = []

def clean_description(text):
    """Clean and validate description text"""
    if not isinstance(text, str):
        return ""

    # Remove unwanted characters and patterns
    cleaned = re.sub(r'[\n\r\t]+', ' ', text)  # Remove newlines, tabs
    cleaned = re.sub(r'\s+', ' ', cleaned)  # Normalize spaces
    cleaned = re.sub(r'[^\w\s.,!?-]', '', cleaned)  # Keep only alphanumeric and basic punctuation
    cleaned = cleaned.strip()

    # Basic validation
    if len(cleaned) < 10:  # Too short, likely garbage
        return ""
    if len(cleaned) > 1000:  # Too long, truncate
        cleaned = cleaned[:997] + "..."

    # Check for repetitive patterns that might indicate garbage
    if re.search(r'(.{20,}?)\1{2,}', cleaned):  # Same pattern repeating 3+ times
        return ""

    # Check for high percentage of non-alphabetic characters
    alpha_ratio = sum(c.isalpha() for c in cleaned) / len(cleaned) if cleaned else 0
    if alpha_ratio < 0.5:  # Less than 50% letters
        return ""

    return cleaned

def safe_extract(page, selector, timeout=5000):
    """Safely extract text from an element with error handling"""
    try:
        if page.locator(selector).count() > 0:
            return page.locator(selector).first.inner_text(timeout=timeout)
        return ""
    except Exception as e:
        print(f"Error extracting {selector}: {str(e)}")
        return ""

def extract_reviews_and_description(page):
    """Extract reviews and description with enhanced error handling"""
    reviews = []
    description = ""

    try:
        # Try to click "More reviews" button if it exists
        more_reviews_button = '//button[@aria-label="More reviews"]'
        if page.locator(more_reviews_button).count() > 0:
            page.locator(more_reviews_button).click()
            page.wait_for_timeout(2000)  # Wait for reviews to load

            # Scroll through reviews
            last_review_count = 0
            scroll_attempts = 0
            max_scroll_attempts = 10

            while scroll_attempts < max_scroll_attempts:
                page.mouse.wheel(0, 2000)
                page.wait_for_timeout(1000)

                # Get all review elements
                review_elements = page.locator('//div[@class="MyEned"]').all()

                if len(review_elements) <= last_review_count:
                    scroll_attempts += 1
                else:
                    last_review_count = len(review_elements)
                    scroll_attempts = 0

            # Extract reviews
            for review in review_elements[:10]:  # Limit to first 10 reviews
                try:
                    review_text = review.locator('.//span[@class="wiI7pd"]').inner_text()
                    reviews.append(review_text.strip())
                except Exception:
                    continue

    except Exception as e:
        print(f"Error extracting reviews: {str(e)}")

    try:
        # Try different selectors for description
        description_selectors = [
            '//div[@class="PYvSYb"]//div[@class="WeS02d fontBodyMedium"]',
            '//div[@class="WeS02d fontBodyMedium"]',
            '//div[contains(@class, "PYvSYb")]'
        ]

        for selector in description_selectors:
            if page.locator(selector).count() > 0:
                raw_description = page.locator(selector).first.inner_text(timeout=5000)
                description = clean_description(raw_description)
                if description:  # If we got a valid cleaned description
                    break

    except Exception as e:
        print(f"Error extracting description: {str(e)}")

    return " | ".join(reviews) if reviews else "No reviews available", description

def get_rating(page):
    """Extract rating with enhanced error handling"""
    try:
        rating_selector = '//div[contains(@class, "fontDisplayLarge")]'
        if page.locator(rating_selector).count() > 0:
            rating_text = page.locator(rating_selector).first.inner_text()
            return re.search(r'(\d+\.?\d*)', rating_text).group(1)
    except Exception as e:
        print(f"Error extracting rating: {str(e)}")
    return ""

def main(output_path='result.csv', search_for="Parks in Medellin", total=10):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            headless=False
        )

        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )

        page = context.new_page()
        page.set_default_timeout(30000)  # 30 seconds default timeout

        try:
            page.goto("https://www.google.com/maps", timeout=60000)
            page.wait_for_timeout(2000)

            # Search and wait for results
            page.locator('//input[@id="searchboxinput"]').fill(search_for)
            page.keyboard.press("Enter")
            page.wait_for_selector('//a[contains(@href, "https://www.google.com/maps/place")]')

            previously_counted = 0
            while True:
                page.mouse.wheel(0, 10000)
                page.wait_for_timeout(2000)

                current_count = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()

                if current_count >= total or current_count == previously_counted:
                    listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()[:total]
                    listings = [listing.locator("xpath=..") for listing in listings]
                    print(f"Total Found: {len(listings)}")
                    break

                previously_counted = current_count
                print(f"Currently Found: {current_count}")

            # Scraping each listing
            for listing in listings:
                try:
                    listing.click()
                    page.wait_for_timeout(2000)

                    # Extract basic information
                    names_list.append(safe_extract(page, '//h1[contains(@class, "DUwDvf")]'))
                    address_list.append(safe_extract(page, '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'))
                    website_list.append(safe_extract(page, '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'))
                    phones_list.append(safe_extract(page, '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'))

                    # Extract reviews and description
                    reviews_text, description = extract_reviews_and_description(page)
                    reviews_text_list.append(reviews_text)
                    descriptions_list.append(description)

                    # Extract rating
                    rating = get_rating(page)
                    reviews_a_list.append(rating)

                    # Additional information
                    place_t_list.append(safe_extract(page, '//div[@class="LBgpqf"]//button[@class="DkEaL "]'))
                    open_list.append(safe_extract(page, '//button[contains(@data-item-id, "oh")]//div[contains(@class, "fontBodyMedium")]'))

                    # Store features
                    store_s_list.append("Yes" if page.locator('//div[contains(text(), "In-store shopping")]').count() > 0 else "No")
                    in_store_list.append("Yes" if page.locator('//div[contains(text(), "In-store pickup")]').count() > 0 else "No")
                    store_del_list.append("Yes" if page.locator('//div[contains(text(), "Delivery")]').count() > 0 else "No")

                except Exception as e:
                    print(f"Error processing listing: {str(e)}")
                    # Append empty values for failed extractions
                    for lst in [names_list, address_list, website_list, phones_list,
                              reviews_text_list, descriptions_list, reviews_a_list,
                              place_t_list, open_list, store_s_list, in_store_list,
                              store_del_list]:
                        if len(lst) < len(names_list):
                            lst.append("")

            # Create DataFrame and save
            df = pd.DataFrame({
                'Names': names_list,
                'Website': website_list,
                'Description': descriptions_list,
                'Phone Number': phones_list,
                'Address': address_list,
                'Average Rating': reviews_a_list,
                'Store Shopping': store_s_list,
                'In Store Pickup': in_store_list,
                'Delivery': store_del_list,
                'Type': place_t_list,
                'Opens At': open_list,
                'Reviews': reviews_text_list
            })

            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(df.head())

        except Exception as e:
            print(f"Major error occurred: {str(e)}")
        finally:
            browser.close()