USAGE_RULES = {
    "niacinamide": "morning",
    "zinc pca": "morning",
    "green tea": "morning",
    "salicylic acid": "night",
    "azelaic acid": "night",
    "vitamin c": "morning",
    "retinol": "night",
}

CONFLICTS = [
    ("retinol", "salicylic acid"),
    ("retinol", "glycolic acid"),
    ("vitamin c", "salicylic acid"),
]

PAIRINGS = [
    ("niacinamide", "zinc pca"),
    ("ceramides", "cholesterol"),
]

FREQUENCY_RULES = {
    "salicylic acid": "2-3 times/week",
    "retinol": "2 times/week",
    "azelaic acid": "daily",
}


def generate_routine(recommendations):
    ingredients = recommendations["ingredients_to_use"]

    morning = []
    night = []
    warnings = []
    pairings = []

    # Assign AM / PM
    for ing in ingredients:
        rule = USAGE_RULES.get(ing, "both")

        if rule in ["morning", "both"]:
            morning.append(ing)

        if rule in ["night", "both"]:
            night.append(ing)

    # Detect conflicts
    for a, b in CONFLICTS:
        if a in ingredients and b in ingredients:
            warnings.append(f"Avoid using {a} with {b}")

    # Detect pairings
    for a, b in PAIRINGS:
        if a in ingredients and b in ingredients:
            pairings.append(
                  f"{a.title()} and {b.upper()} work well together for oil control and acne-prone skin."
)

    return {
        "morning_routine": morning,
        "night_routine": night,
        "conflicts": warnings,
        "pairings": pairings
    }


