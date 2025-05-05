from serpapi import GoogleSearch
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')


def send_query(searchTerm, min_price, max_price):
    params = {
        "engine": "google_shopping",
        "q": searchTerm,
        "api_key": api_key,
        "gl": "in",
        "tbm": "shop",
        "hl": "en"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    products = results.get("shopping_results", [])
    filtered = []
    for item in products:
        title = item.get("title", "")
        price_str = item.get("price", "").replace("₹", "").replace(",", "").strip()

        try:
            price = float(price_str)
            if min_price <= price <= max_price:
                filtered.append({
                    "title": title,
                    "price": f"₹{price:,.2f}",
                    "seller": item.get("source", "Unknown"),
                    "link": item.get("product_link", "")
                })
        except ValueError:
            continue
    # Save only the new query results to the JSON
    with open(r'E:\google_shopping\ShopSmart\backend\data\api_results.json', "w") as f:
        json.dump(filtered, f, indent=2)

    return filtered