def derive_condition_tags(row):
    tags = []

    if row["acne_score"] >= 3:
        tags.append("acne_prone")

    if row["barrier_score"] <= 2:
        tags.append("barrier_impaired")

    if row["dryness_score"] >= 3:
        tags.append("dehydration_prone")

    if row["sensitivity_score"] >= 3:
        tags.append("reactive")

    if row["oiliness_score"] >= 3:
        tags.append("high_sebum")

    return tags

def derive_condition_tags(row):
    tags = []

    if row["acne_score"] >= 3:
        tags.append("acne_prone")

    if row["barrier_score"] <= 2:
        tags.append("barrier_impaired")

    if row["dryness_score"] >= 3:
        tags.append("dehydration_prone")

    if row["sensitivity_score"] >= 3:
        tags.append("reactive")

    if row["oiliness_score"] >= 3:
        tags.append("high_sebum")

    return tags


BASE_RECOMMENDATIONS = {
    "oily": {
        "ingredients_to_use": [
            "niacinamide",
            "salicylic acid",
            "zinc pca",
            "green tea"
        ],
        "ingredients_to_avoid": [
            "coconut oil",
            "heavy occlusive oils",
            "isopropyl myristate"
        ],
        "behaviours_to_avoid": [
            "over-cleansing more than twice daily",
            "using harsh scrubs",
            "using overly drying products to control oil"
        ],
        "product_categories": [
            "gel cleanser",
            "lightweight moisturiser",
            "non-comedogenic sunscreen",
            "BHA treatment"
        ]
    },

    "dry": {
        "ingredients_to_use": [
            "ceramides",
            "hyaluronic acid",
            "glycerin",
            "squalane",
            "panthenol"
        ],
        "ingredients_to_avoid": [
            "alcohol denat",
            "strong exfoliating acids",
            "harsh foaming surfactants"
        ],
        "behaviours_to_avoid": [
            "washing with hot water",
            "over-exfoliating",
            "skipping moisturiser after cleansing"
        ],
        "product_categories": [
            "cream cleanser",
            "barrier moisturiser",
            "hydrating serum",
            "gentle sunscreen"
        ]
    },

    "combination": {
        "ingredients_to_use": [
            "niacinamide",
            "hyaluronic acid",
            "ceramides",
            "panthenol"
        ],
        "ingredients_to_avoid": [
            "heavy pore-clogging oils",
            "harsh scrubs",
            "overly drying alcohol-heavy formulas"
        ],
        "behaviours_to_avoid": [
            "using the same heavy product on all areas",
            "over-treating the oily zones",
            "ignoring dry areas because the T-zone is oily"
        ],
        "product_categories": [
            "gentle gel cleanser",
            "lightweight moisturiser",
            "hydrating serum",
            "balanced sunscreen"
        ]
    },

    "sensitive": {
        "ingredients_to_use": [
            "centella asiatica",
            "panthenol",
            "ceramides",
            "allantoin",
            "colloidal oatmeal"
        ],
        "ingredients_to_avoid": [
            "fragrance",
            "essential oils",
            "high-strength retinoids",
            "strong exfoliating acids"
        ],
        "behaviours_to_avoid": [
            "introducing multiple new products at once",
            "using fragranced products",
            "over-exfoliating"
        ],
        "product_categories": [
            "fragrance-free cleanser",
            "barrier repair moisturiser",
            "mineral sunscreen",
            "soothing serum"
        ]
    },

    "normal": {
        "ingredients_to_use": [
            "glycerin",
            "niacinamide",
            "hyaluronic acid",
            "ceramides"
        ],
        "ingredients_to_avoid": [
            "unnecessary high-strength actives",
            "harsh scrubs",
            "fragrance-heavy products"
        ],
        "behaviours_to_avoid": [
            "using too many actives without need",
            "skipping sunscreen",
            "changing products too frequently"
        ],
        "product_categories": [
            "gentle cleanser",
            "daily moisturiser",
            "broad-spectrum sunscreen",
            "optional antioxidant serum"
        ]
    }
}


TAG_RECOMMENDATIONS = {
    "acne_prone": {
        "ingredients_to_use": [
            "salicylic acid",
            "azelaic acid",
            "niacinamide",
            "zinc pca"
        ],
        "ingredients_to_avoid": [
            "coconut oil",
            "isopropyl myristate",
            "heavy comedogenic butters"
        ],
        "behaviours_to_avoid": [
            "picking or squeezing pimples",
            "using comedogenic hair oils near the face",
            "over-drying acne with too many actives"
        ],
        "product_categories": [
            "BHA treatment",
            "non-comedogenic moisturiser",
            "oil-free sunscreen"
        ]
    },

    "barrier_impaired": {
        "ingredients_to_use": [
            "ceramides",
            "panthenol",
            "cholesterol",
            "fatty acids",
            "beta glucan"
        ],
        "ingredients_to_avoid": [
            "strong exfoliating acids",
            "high-strength retinoids",
            "alcohol denat",
            "fragrance"
        ],
        "behaviours_to_avoid": [
            "exfoliating while skin is irritated",
            "using too many active treatments together",
            "washing with very hot water"
        ],
        "product_categories": [
            "barrier repair moisturiser",
            "gentle cleanser",
            "soothing serum"
        ]
    },

    "dehydration_prone": {
        "ingredients_to_use": [
            "hyaluronic acid",
            "glycerin",
            "panthenol",
            "betaine"
        ],
        "ingredients_to_avoid": [
            "harsh foaming cleansers",
            "overuse of clay masks",
            "drying alcohols"
        ],
        "behaviours_to_avoid": [
            "letting skin dry completely before moisturising",
            "using mattifying products all over the face",
            "skipping moisturiser in humid weather"
        ],
        "product_categories": [
            "hydrating serum",
            "lightweight moisturiser",
            "cream or lotion cleanser"
        ]
    },

    "reactive": {
        "ingredients_to_use": [
            "centella asiatica",
            "allantoin",
            "panthenol",
            "colloidal oatmeal"
        ],
        "ingredients_to_avoid": [
            "fragrance",
            "essential oils",
            "strong acids",
            "high-percentage vitamin c"
        ],
        "behaviours_to_avoid": [
            "testing several products at once",
            "using exfoliants during flare-ups",
            "using fragranced skincare"
        ],
        "product_categories": [
            "soothing serum",
            "minimal-ingredient moisturiser",
            "mineral sunscreen"
        ]
    },

    "high_sebum": {
        "ingredients_to_use": [
            "niacinamide",
            "zinc pca",
            "green tea",
            "salicylic acid"
        ],
        "ingredients_to_avoid": [
            "heavy occlusive oils",
            "greasy balms",
            "comedogenic esters"
        ],
        "behaviours_to_avoid": [
            "stripping the skin with harsh cleansers",
            "skipping moisturiser",
            "using overly heavy creams on oily areas"
        ],
        "product_categories": [
            "gel cleanser",
            "lightweight gel moisturiser",
            "oil-control sunscreen"
        ]
    }
}


def merge_unique(items):
    seen = set()
    result = []

    for item in items:
        normalized = item.lower().strip()
        if normalized not in seen:
            seen.add(normalized)
            result.append(item)

    return result


def generate_recommendations(predicted_skin_type, trait_scores):
    tags = derive_condition_tags(trait_scores)

    final = {
        "skin_type": predicted_skin_type,
        "condition_tags": tags,
        "ingredients_to_use": [],
        "ingredients_to_avoid": [],
        "behaviours_to_avoid": [],
        "product_categories": []
    }

    base = BASE_RECOMMENDATIONS[predicted_skin_type]

    for key in [
        "ingredients_to_use",
        "ingredients_to_avoid",
        "behaviours_to_avoid",
        "product_categories"
    ]:
        final[key].extend(base[key])

    for tag in tags:
        tag_rules = TAG_RECOMMENDATIONS[tag]

        for key in [
            "ingredients_to_use",
            "ingredients_to_avoid",
            "behaviours_to_avoid",
            "product_categories"
        ]:
            final[key].extend(tag_rules[key])

    for key in [
        "ingredients_to_use",
        "ingredients_to_avoid",
        "behaviours_to_avoid",
        "product_categories"
    ]:
        final[key] = merge_unique(final[key])

    return final