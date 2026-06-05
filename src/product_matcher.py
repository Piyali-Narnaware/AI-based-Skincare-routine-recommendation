from src.product_database import PRODUCTS


INGREDIENT_SYNONYMS = {
    "niacinamide": ["niacinamide", "vitamin b3", "nicotinamide"],
    "salicylic acid": ["salicylic acid", "bha", "beta hydroxy acid"],
    "zinc pca": ["zinc pca"],
    "hyaluronic acid": ["hyaluronic acid", "sodium hyaluronate"],
    "ceramides": ["ceramide", "ceramide np", "ceramide ap", "ceramide eop"],
    "panthenol": ["panthenol", "pro vitamin b5", "pro-vitamin b5"],
    "glycerin": ["glycerin", "glycerine"],
    "centella asiatica": ["centella asiatica", "cica", "madecassoside"],
    "fragrance": ["fragrance", "parfum", "perfume"],
    "alcohol denat": ["alcohol denat", "denatured alcohol", "sd alcohol"],
    "coconut oil": ["coconut oil", "cocos nucifera oil"],
    "essential oils": ["essential oils", "lavender oil", "tea tree oil", "peppermint oil"],
    "isopropyl myristate": ["isopropyl myristate"],
    "heavy occlusive oils": ["mineral oil", "heavy occlusive oils"],
}


def normalize(text):
    return text.lower().strip()


def expand_terms(terms):
    expanded = set()

    for term in terms:
        term = normalize(term)
        expanded.add(term)

        if term in INGREDIENT_SYNONYMS:
            for synonym in INGREDIENT_SYNONYMS[term]:
                expanded.add(normalize(synonym))

    return expanded


def score_product(product, recommendations):
    product_ingredients = set(normalize(i) for i in product["ingredients"])

    use_terms = expand_terms(recommendations["ingredients_to_use"])
    avoid_terms = expand_terms(recommendations["ingredients_to_avoid"])

    matched_good = sorted(product_ingredients.intersection(use_terms))
    matched_bad = sorted(product_ingredients.intersection(avoid_terms))

    score = 0

    # Strong reward for key actives
    key_actives = [normalize(i) for i in product.get("key_actives", [])]

    for active in key_actives:
        if active in use_terms:
            score += 20

    # Normal reward for other useful ingredients
    for ingredient in product_ingredients:
        if ingredient in use_terms:
            score += 10

    # Heavy penalty for avoid ingredients
    for ingredient in product_ingredients:
        if ingredient in avoid_terms:
            score -= 40

    status = (
        "recommended"
        if score > 0 and not matched_bad
        else "avoid"
        if matched_bad
        else "neutral"
    )

    return {
        "product_name": product["product_name"],
        "brand": product["brand"],
        "category": product["category"],
        "price_inr": product["price_inr"],
        "price_gbp": product["price_gbp"],
        "score": score,
        "status": status,
        "matched_good": matched_good,
        "matched_bad": matched_bad,
        "why_recommended": f"Matches helpful ingredients: {', '.join(matched_good)}"
        if matched_good
        else "",
        "why_avoided": f"Contains avoid ingredients: {', '.join(matched_bad)}"
        if matched_bad
        else "",
    }

BUDGET_RANGES = {
    "India": {"Budget": (0, 500), "Mid-range": (500, 1000), "Premium": (1000, float("inf"))},
    "UK": {"Budget": (0, 8), "Mid-range": (8, 15), "Premium": (15, float("inf"))},
}


def in_budget(product, region, budget):
    if budget == "All":
        return True
    ranges = BUDGET_RANGES.get(region)
    if not ranges or budget not in ranges:
        return True
    lo, hi = ranges[budget]
    price = product["price_gbp"] if region == "UK" else product["price_inr"]
    return lo <= price < hi


def recommend_products(recommendations, region="India", budget="All"):
    recommended = []
    avoid = []
    neutral = []

    for product in PRODUCTS:
        if region not in product.get("region", ["India"]):
            continue
        if not in_budget(product, region, budget):
            continue
        scored = score_product(product, recommendations)

        if scored["status"] == "recommended":
            recommended.append(scored)
        elif scored["status"] == "avoid":
            avoid.append(scored)
        else:
            neutral.append(scored)

    # Sort lists
    recommended = sorted(recommended, key=lambda x: x["score"], reverse=True)
    avoid = sorted(avoid, key=lambda x: x["score"])

    # -----------------------------
    # Group by category (FIXED INDENTATION)
    # -----------------------------
    category_best = {}

    for product in recommended:
        cat = product["category"].strip().lower()

        if cat not in category_best:
            category_best[cat] = product

    # Convert to list
    category_recommendations = list(category_best.values())

    # -----------------------------
    # Final return
    # -----------------------------
    return {
        "recommended_products": recommended,
        "category_recommendations": category_recommendations,
        "avoid_products": avoid,
        "neutral_products": neutral
    }