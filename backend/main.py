from serpapi import GoogleSearch
import json
import re
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage


load_dotenv()
api_key = os.getenv('API_KEY')

email_user = "gutkarsh9838@gmail.com"
email_pass = "qtkg qkkv cdgk cuxa"


def send_email(user_email):
    msg = EmailMessage()
    msg["Subject"] = "ShopSmart - Products Available in Your Price Range!"
    msg["From"] = email_user
    msg["To"] = user_email

    content = "Hello,\n\nProducts are  available in your price range....!!!\n\n"
    
    msg.set_content(content)

    # Send the email using Gmail's SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)
        print("Mail Sent!!!")



def send_query(searchTerm, min_price, max_price,user_email=None):
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

        if filtered and  user_email:
            send_email(user_email)

    return filtered