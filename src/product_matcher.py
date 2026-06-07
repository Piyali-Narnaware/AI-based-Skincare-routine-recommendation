from src.product_database import PRODUCTS


INGREDIENT_BENEFITS = {
    "niacinamide": "regulates oil production, reduces pore appearance, and strengthens skin barrier",
    "salicylic acid": "deeply cleanses pores, reduces blackheads, and controls acne breakouts",
    "zinc pca": "controls sebum production and soothes inflammation",
    "hyaluronic acid": "provides intense hydration and plumps the skin",
    "ceramides": "repairs and strengthens the skin barrier, locking in moisture",
    "panthenol": "soothes irritation and supports skin healing",
    "glycerin": "hydrates and maintains skin moisture balance",
    "centella asiatica": "calms inflammation, boosts collagen, and accelerates healing",
    "green tea": "provides antioxidant protection and soothes inflammation",
    "azelaic acid": "reduces redness, unclogs pores, and brightens skin tone",
    "retinol": "stimulates collagen production, reduces fine lines and acne",
    "vitamin c": "brightens skin, reduces dark spots, and protects from environmental damage",
    "squalane": "hydrates without clogging pores and mimics skin's natural oils",
}

SYNERGY_NOTES = {
    ("niacinamide", "zinc pca"): "Together they provide excellent oil control and acne management.",
    ("salicylic acid", "niacinamide"): "Salicylic acid clears pores while niacinamide soothes and repairs.",
    ("hyaluronic acid", "ceramides"): "Hyaluronic acid hydrates while ceramides lock in moisture.",
    ("centella asiatica", "panthenol"): "A powerful soothing duo that calms irritation and supports healing.",
    ("retinol", "ceramides"): "Retinol renews skin while ceramides protect the barrier from irritation.",
}


def describe_benefits(matched_good):
    if not matched_good:
        return ""
    parts = []
    for ing in matched_good:
        ing_lower = ing.lower().strip()
        benefit = INGREDIENT_BENEFITS.get(ing_lower, "supports healthy skin function")
        parts.append(f"- **{ing}**: {benefit}")
    synergy = ""
    for ing1, ing2 in [("niacinamide", "zinc pca"), ("salicylic acid", "niacinamide"), ("hyaluronic acid", "ceramides"), ("centella asiatica", "panthenol"), ("retinol", "ceramides")]:
        if ing1 in [i.lower() for i in matched_good] and ing2 in [i.lower() for i in matched_good]:
            synergy = "\n\n" + SYNERGY_NOTES.get((ing1, ing2), "")
            break
    body = "\n".join(parts)
    return body + synergy


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
        "why_recommended": describe_benefits(matched_good)
        if matched_good
        else "",
        "highlights": product.get("highlights", ""),
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