import requests
import json
import os

# List of stores and their corresponding API URLs
stores = {
    "foodbasics": "https://dam.flippenterprise.net/api/flipp/flyers/7469600/flyer_items?locale=en",
    "nofrills": "https://dam.flippenterprise.net/api/flipp/flyers/7465213/flyer_items?locale=en",
    "freshco": "https://dam.flippenterprise.net/api/flipp/flyers/7456719/flyer_items?locale=en",
    "metro": "https://dam.flippenterprise.net/api/flipp/flyers/7471710/flyer_items?locale=en",
    "foodland": "https://dam.flippenterprise.net/api/flipp/flyers/7471042/flyer_items?locale=en",
    "gianttiger": "https://dam.flippenterprise.net/api/flipp/flyers/7465213/flyer_items?locale=en"
}

# Create a directory to store the data if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Define the set of keys to remove from each product entry
keys_to_remove = {
    "video_url", "display_type", "available_to", "page_destination",
    "left", "bottom", "right", "top"
}

# Loop through each store
for store_name, url in stores.items():
    try:
        # Send a GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Get the JSON data from the response
        data = response.json()

        # Process each item in the data list
        for item in data:
            # Remove the unwanted keys
            for key in keys_to_remove:
                # Use .pop() with a default value of None to avoid errors if a key doesn't exist
                item.pop(key, None)

            # Replace the flyer_id with the store name
            item['flyer_id'] = store_name

        # Define the output file path
        file_path = os.path.join('data', f'{store_name}.json')

        # Save the modified data to a JSON file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Successfully scraped and processed data for {store_name}")

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {store_name}: {e}")