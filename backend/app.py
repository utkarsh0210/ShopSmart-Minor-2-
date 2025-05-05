from flask import Flask , request , jsonify
from flask_cors import CORS
import json
from main import send_query


app = Flask(__name__)
CORS(app)

prod_data = r"E:\google_shopping\ShopSmart\backend\data\api_results.json"

@app.route("/")
def index():
    return "Welcome to Shopsmart"

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    search_term = data.get("searchTerm", "").lower()
    min_price = float(data.get("minPrice", 0))
    max_price = float(data.get("maxPrice", float("inf")))

    print("Received:", search_term, min_price, max_price)

    # Step 1: Query Google Shopping using SerpAPI
    filtered = send_query(search_term,min_price , max_price)

    return jsonify(filtered)

@app.route("/show_result", methods=["GET"])
def show_result():
    search_term = request.args.get("searchTerm", "").lower().split()
    with open(prod_data,'r') as f:
        data = json.load(f)
    # def matches_search(title, tokens):
    #     title_lower = title.lower()
    #     return all(token in title_lower for token in tokens)

    # filtered_data = [
    #     item for item in data
    #     if matches_search(item["title"], search_term)
    # ]

    print(f"Sending {len(data)} items matching tokens: {search_term}")
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)