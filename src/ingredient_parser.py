import re


def normalize_ingredient_name(text):
    text = text.lower().strip()

    # Remove percentages like 10%, 2.5%, etc.
    text = re.sub(r"\d+(\.\d+)?\s*%", "", text)

    # Remove bracketed explanations
    text = re.sub(r"\(.*?\)", "", text)

    # Remove extra symbols
    text = re.sub(r"[^a-z0-9\s\-]", "", text)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def parse_ingredient_string(ingredient_text):
    if not ingredient_text or not isinstance(ingredient_text, str):
        return []

    # Replace common separators with commas
    ingredient_text = ingredient_text.replace(";", ",")
    ingredient_text = ingredient_text.replace("|", ",")
    ingredient_text = ingredient_text.replace("\n", ",")

    raw_ingredients = ingredient_text.split(",")

    ingredients = []

    for item in raw_ingredients:
        cleaned = normalize_ingredient_name(item)

        if cleaned:
            ingredients.append(cleaned)

    return ingredients


def detect_key_actives(ingredients):
    active_keywords = [
        "niacinamide",
        "salicylic acid",
        "zinc pca",
        "azelaic acid",
        "hyaluronic acid",
        "sodium hyaluronate",
        "ceramide",
        "panthenol",
        "centella asiatica",
        "madecassoside",
        "green tea",
        "allantoin",
        "glycerin"
    ]

    key_actives = []

    for ingredient in ingredients:
        for active in active_keywords:
            if active in ingredient:
                key_actives.append(active)

    return list(dict.fromkeys(key_actives))


def parse_product_ingredients(raw_ingredient_text):
    ingredients = parse_ingredient_string(raw_ingredient_text)
    key_actives = detect_key_actives(ingredients)

    return {
        "ingredients": ingredients,
        "key_actives": key_actives
    }


if __name__ == "__main__":
    sample = """
    Aqua, Niacinamide 10%, Zinc PCA, Glycerin, Panthenol,
    Salicylic Acid (BHA), Phenoxyethanol, Fragrance
    """

    parsed = parse_product_ingredients(sample)

    print("Ingredients:")
    print(parsed["ingredients"])

    print("\nKey Actives:")
    print(parsed["key_actives"])