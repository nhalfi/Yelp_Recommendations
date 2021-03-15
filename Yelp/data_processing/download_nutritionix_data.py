import json
import requests

NUTRITIONIX_URL = "https://api.nutritionix.com/v1_1/search"
DEFAULT_ITERATION_COUNT = 60


def fetch_data_from_nutritionix(iteration_count=1):
    results = []
    query = {
        "appId": "91e4a07d",
        "appKey": "03d1f9a480f0ee71eb064d5d6fa7264e",
        "fields": [
            "item_name",
            "brand_name",
            "upc",
            "nt_ingredient_statement",
            "nf_calories",
            "nf_calories_from_fat",
            "nf_total_fat",
            "nf_saturated_fat",
            "nf_trans_fatty_acid",
            "nf_cholesterol",
            "nf_sodium",
            "nf_sugars",
            "nf_protein",
            "nf_serving_per_container"
            ],
        "limit": 50,
        "filters": {"item_type": 1}
    }
    for i in range(iteration_count):
        try:
            query["offset"] = (i*50),
            response = requests.post(NUTRITIONIX_URL, json=query)
            print(response.status_code)
            if response.ok:
                results.extend(response.json()['hits'])
        except Exception as e:
            # This is generally considered bad.
            # We want to get as much data as we can.
            print(e)

    return results


def persist_data_as_json(data, filename="../data/restaurants_items.json"):

    with open(filename, 'w') as json_file:
        json.dump(data, json_file)


if __name__ == "__main__":
    data = fetch_data_from_nutritionix(iteration_count=DEFAULT_ITERATION_COUNT)
    persist_data_as_json(data)
