import requests
import json
import os
import shutil

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
        # --- 1. Fetch and Process JSON Data ---
        print(f"Fetching data for {store_name}...")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Process each item in the data list
        for item in data:
            for key in keys_to_remove:
                item.pop(key, None)
            item['flyer_id'] = store_name

        # --- 2. Save the Processed JSON File ---
        json_file_path = os.path.join('data', f'{store_name}.json')
        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully saved JSON for {store_name}")

        # --- 3. Download Images ---
        # Create a dedicated folder for the store's images
        image_dir = os.path.join('data', f'{store_name}_images')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        print(f"Downloading images for {store_name}...")
        for item in data:
            image_url = item.get("cutout_image_url")
            item_id = item.get("id")

            # Proceed only if the URL and ID exist
            if image_url and item_id:
                try:
                    # Define the image filename using the item's ID
                    image_filename = f"{item_id}.jpg"
                    image_path = os.path.join(image_dir, image_filename)

                    # Stream the download to handle images efficiently
                    img_response = requests.get(image_url, stream=True)
                    img_response.raise_for_status()

                    # Save the image to the file
                    with open(image_path, 'wb') as img_file:
                        shutil.copyfileobj(img_response.raw, img_file)

                except requests.exceptions.RequestException as e:
                    print(f"  - Could not download image for item {item_id}: {e}")

        print(f"Finished downloading images for {store_name}\n")

    except requests.exceptions.RequestException as e:
        print(f"Error scraping {store_name}: {e}\n")