import pandas as pd
from recommendation_engine import generate_recommendations

sample_trait_scores = pd.Series({
    "oiliness_score": 3.4,
    "dryness_score": 2.7,
    "sensitivity_score": 2.1,
    "acne_score": 4.2,
    "barrier_score": 1.8
})

predicted_skin_type = "combination"

recommendations = generate_recommendations(
    predicted_skin_type,
    sample_trait_scores
)

print("\nSkin Type:")
print(recommendations["skin_type"])

print("\nCondition Tags:")
print(recommendations["condition_tags"])

print("\nIngredients to Use:")
for item in recommendations["ingredients_to_use"]:
    print("-", item)

print("\nIngredients to Avoid:")
for item in recommendations["ingredients_to_avoid"]:
    print("-", item)

print("\nBehaviours to Avoid:")
for item in recommendations["behaviours_to_avoid"]:
    print("-", item)

print("\nProduct Categories:")
for item in recommendations["product_categories"]:
    print("-", item)