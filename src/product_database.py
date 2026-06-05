import os
import pandas as pd
from src.ingredient_parser import parse_product_ingredients


def load_products_from_csv(csv_path=None):
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw_product_database.csv")
    df = pd.read_csv(csv_path)

    products = []

    for _, row in df.iterrows():
        parsed = parse_product_ingredients(row["raw_ingredients"])

        products.append({
            "product_name": row["product_name"],
            "brand": row["brand"],
            "category": row["category"],
            "price_inr": row["price_inr"],
            "region": [r.strip() for r in row.get("region", "India").split(";")],
            "raw_ingredients": row["raw_ingredients"],
            "ingredients": parsed["ingredients"],
            "key_actives": parsed["key_actives"]
        })

    return products


PRODUCTS = load_products_from_csv()