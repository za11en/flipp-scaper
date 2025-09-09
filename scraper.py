import requests
import json
import os
import shutil

stores = {
    "foodbasics": "https://dam.flippenterprise.net/api/flipp/flyers/7469600/flyer_items?locale=en",
    "nofrills": "https://dam.flippenterprise.net/api/flipp/flyers/7465213/flyer_items?locale=en",
    "freshco": "https://dam.flippenterprise.net/api/flipp/flyers/7456719/flyer_items?locale=en",
    "metro": "https://dam.flippenterprise.net/api/flipp/flyers/7471710/flyer_items?locale=en",
    "foodland": "https://dam.flippenterprise.net/api/flipp/flyers/7471042/flyer_items?locale=en",
    "gianttiger": "https://dam.flippenterprise.net/api/flipp/flyers/7465213/flyer_items?locale=en",
    "walmart": "https://dam.flippenterprise.net/api/flipp/flyers/7469517/flyer_items?locale=en",
    "loblaws": "https://dam.flippenterprise.net/api/flipp/flyers/7477242/flyer_items?locale=en"
}

# Create base directories if they don't exist
os.makedirs('data/images', exist_ok=True)
os.makedirs('data/json', exist_ok=True)

keys_to_remove = {
    "video_url", "display_type", "available_to", "page_destination",
    "left", "bottom", "right", "top"
}

for store_name, url in stores.items():
    try:
        print(f"Fetching data for {store_name}...")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data:
            print(f"No data found for {store_name}, skipping.\n")
            continue

        # Extract the valid_from date from the first item (assuming all items in a flyer have the same date)
        # The date is in ISO 8601 format, so we can slice the string to get 'YYYY-MM-DD'
        valid_from_date = data[0]['valid_from'][:10]

        # Process JSON data
        for item in data:
            for key in keys_to_remove:
                item.pop(key, None)
            item['flyer_id'] = store_name

        # Create store-specific JSON directory
        store_json_dir = os.path.join('data', 'json', store_name)
        os.makedirs(store_json_dir, exist_ok=True)

        # Define and save the JSON file
        json_filename = f'{store_name}-{valid_from_date}.json'
        json_file_path = os.path.join(store_json_dir, json_filename)

        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully saved JSON to {json_file_path}")

        # Create store- and date-specific image directory
        image_dir = os.path.join('data', 'images', store_name, valid_from_date)
        os.makedirs(image_dir, exist_ok=True)

        print(f"Downloading images for {store_name} for week {valid_from_date}...")
        for item in data:
            image_url = item.get("cutout_image_url")
            item_id = item.get("id")

            if image_url and item_id:
                try:
                    image_filename = f"{item_id}.jpg"
                    image_path = os.path.join(image_dir, image_filename)

                    # Download the image
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