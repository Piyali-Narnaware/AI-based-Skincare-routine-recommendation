import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from src.recommendation_engine import generate_recommendations
from src.product_matcher import recommend_products
from src.routine_engine import generate_routine


# -----------------------------
# 1. Load dataset
# -----------------------------

import os
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "scripts", "model_training_data_3.csv"))


# -----------------------------
# 2. Define features and targets
# -----------------------------

feature_cols = [
    "age_group",
    "bare_skin_feel_30min",
    "midday_shine",
    "tight_flaky_frequency",
    "pore_visibility",
    "breakout_frequency",
    "breakout_location",
    "hormonal_stress_pattern",
    "new_product_reaction",
    "redness_frequency",
    "post_cleanse_feel",
    "seasonal_change",
    "acne_prone_tag"
]

target_cols = [
    "oiliness_score",
    "dryness_score",
    "sensitivity_score",
    "acne_score",
    "barrier_score"
]

X = df[feature_cols]
y = df[target_cols]


# -----------------------------
# 3. Train model
# -----------------------------

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


# -----------------------------
# 4. Skin type classifier
# -----------------------------

def classify_skin_type(row):
    oil = row["oiliness_score"]
    dry = row["dryness_score"]
    sens = row["sensitivity_score"]

    if sens >= 4:
        return "sensitive"

    if abs(oil - dry) <= 1 and oil >= 2:
        return "combination"

    if oil >= 2.7:
        return "oily"

    if dry >= 3:
        return "dry"

    return "normal"


# -----------------------------
# 5. Example user input
# -----------------------------

sample_user = pd.DataFrame([{
    "age_group": 2,
    "bare_skin_feel_30min": 4,
    "midday_shine": 4,
    "tight_flaky_frequency": 2,
    "pore_visibility": 3,
    "breakout_frequency": 3,
    "breakout_location": 4,
    "hormonal_stress_pattern": 3,
    "new_product_reaction": 2,
    "redness_frequency": 2,
    "post_cleanse_feel": 2,
    "seasonal_change": 4,
    "acne_prone_tag": 1
}])


# -----------------------------
# 6. Predict trait scores
# -----------------------------

prediction = model.predict(sample_user)[0]

trait_scores = pd.Series(
    prediction,
    index=target_cols
)

predicted_skin_type = classify_skin_type(trait_scores)


# -----------------------------
# 7. Generate recommendations
# -----------------------------

recommendations = generate_recommendations(
    predicted_skin_type,
    trait_scores
)

REGION = "India"
product_results = recommend_products(recommendations, region=REGION)

routine = generate_routine(recommendations)
# -----------------------------
# 8. Print final output
# -----------------------------

print("\n==============================")
print("FINAL SKIN ANALYSIS")
print("==============================")

print("\nPredicted Trait Scores:")
for trait, score in trait_scores.items():
    print(f"{trait}: {round(score, 2)}")

print("\nPredicted Skin Type:")
print(predicted_skin_type)

print("\nCondition Tags:")
print(recommendations["condition_tags"])

print("\nIngredients to Use:")
for item in recommendations["ingredients_to_use"][:8]:
    print("-", item)

print("\nIngredients to Avoid:")
for item in recommendations["ingredients_to_avoid"][:8]:
    print("-", item)

print("\nBehaviours to Avoid:")
for item in recommendations["behaviours_to_avoid"][:6]:
    print("-", item)

print("\nProduct Categories:")
for item in recommendations["product_categories"][:6]:
    print("-", item)


# -----------------------------
# 9. Product recommendations
# -----------------------------

print("\n==============================")
print("PRODUCT RECOMMENDATIONS")
print("==============================")

ROUTINE_ORDER = ["cleanser", "serum", "treatment", "moisturiser", "sunscreen"]

print("\nRecommended Routine (Category-wise):")

category_map = {
    item["category"].lower(): item
    for item in product_results["category_recommendations"]
}

for category in ROUTINE_ORDER:
    if category in category_map:
        product = category_map[category]

        print(f"\n{category.upper()}:")
        print(f"- {product['product_name']} ({product['brand']})")
        print(f"  Score: {product['score']}")
        print(f"  Why: {product['why_recommended']}")

print("\nProducts to Avoid:")
for product in product_results["avoid_products"][:5]:
    print(f"- {product['product_name']} ({product['brand']})")
    print(f"  Category: {product['category']}")
    print(f"  Score: {product['score']}")
    print(f"  Problem ingredients: {product['matched_bad']}")

print("\n==============================")
print("USAGE ROUTINE (SMART)")
print("==============================")

print("\nMorning:")
for item in routine["morning_routine"]:
    print("-", item)

print("\nNight:")
for item in routine["night_routine"]:
    print("-", item)

if routine["conflicts"]:
    print("\nWarnings:")
    for w in routine["conflicts"]:
        print("-", w)

if routine["pairings"]:
    print("\nGood Pairings:")
    for p in routine["pairings"]:
        print("-", p)