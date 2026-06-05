import itertools
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from recommendation_engine import generate_recommendations
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import classify_skin_type, get_base_skin_type


df = pd.read_csv("data/model_training_data_3.csv")

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

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


option_space = {
    "age_group": [1, 2, 3, 4, 5],
    "bare_skin_feel_30min": [1, 2, 3, 4, 5],
    "midday_shine": [1, 2, 3, 4, 5],
    "tight_flaky_frequency": [1, 2, 3, 4],
    "pore_visibility": [1, 2, 3, 4, 5],
    "breakout_frequency": [1, 2, 3, 4],
    "breakout_location": [1, 2, 3, 4, 5],
    "hormonal_stress_pattern": [1, 2, 3, 4],
    "new_product_reaction": [1, 2, 3, 4],
    "redness_frequency": [1, 2, 3, 4],
    "post_cleanse_feel": [1, 2, 3, 4],
    "seasonal_change": [1, 2, 3, 4, 5],
    "acne_prone_tag": [0, 1],
}


def flag_suspicious(row):
    flags = []

    profile = row["skin_profile"].lower()

    # Strong dryness signals but normal output
    if (
        row["bare_skin_feel_30min"] <= 2
        and row["midday_shine"] <= 2
        and row["tight_flaky_frequency"] >= 3
        and "normal" in profile
    ):
        flags.append("Strong dry signals but classified normal")

    # Strong oil signals but normal/dry output
    if (
        row["midday_shine"] >= 4
        and row["pore_visibility"] >= 4
        and row["bare_skin_feel_30min"] >= 4
        and ("normal" in profile or profile.startswith("dry"))
    ):
        flags.append("Strong oily signals but classified normal/dry")

    # Strong sensitivity signals but not sensitive
    if (
        row["new_product_reaction"] >= 3
        and row["redness_frequency"] >= 3
        and row["seasonal_change"] == 5
        and "sensitive" not in profile
    ):
        flags.append("Strong sensitivity signals but not sensitive")

    # Strong acne signals but no acne-prone profile/tag
    if (
        row["breakout_frequency"] >= 3
        and row["acne_prone_tag"] == 1
        and "acne-prone" not in profile
    ):
        flags.append("Strong acne signals but not acne-prone")

    # Seasonal mixed + visible pores should not usually be plain normal
    if (
        row["seasonal_change"] == 4
        and row["pore_visibility"] >= 3
        and profile == "normal"
    ):
        flags.append("Mixed seasonal skin + pores but classified normal")

    # Barrier impaired but not sensitive/barrier impaired recommendations
    if (
        row["post_cleanse_feel"] >= 3
        and row["new_product_reaction"] >= 3
        and "sensitive" not in profile
    ):
        flags.append("Barrier/reactivity signals but not sensitive")

    return flags


records = []

keys = list(option_space.keys())
values = list(option_space.values())

total = 0

for combo in itertools.product(*values):
    user_answers = dict(zip(keys, combo))

    user_input = pd.DataFrame([user_answers])
    prediction = model.predict(user_input)[0]

    trait_scores = pd.Series(prediction, index=target_cols)

    skin_profile = classify_skin_type(trait_scores, user_answers)
    base_skin_type = get_base_skin_type(skin_profile)

    recommendations = generate_recommendations(base_skin_type, trait_scores)

    record = {
        **user_answers,
        "oiliness_score": round(trait_scores["oiliness_score"], 2),
        "dryness_score": round(trait_scores["dryness_score"], 2),
        "sensitivity_score": round(trait_scores["sensitivity_score"], 2),
        "acne_score": round(trait_scores["acne_score"], 2),
        "barrier_score": round(trait_scores["barrier_score"], 2),
        "skin_profile": skin_profile,
        "base_skin_type": base_skin_type,
        "condition_tags": ", ".join(recommendations["condition_tags"]),
    }

    flags = flag_suspicious(record)
    record["flags"] = " | ".join(flags)

    records.append(record)
    total += 1


results = pd.DataFrame(records)

results.to_csv("all_combination_validation_results.csv", index=False)

flagged = results[results["flags"] != ""]
flagged.to_csv("flagged_suspicious_results.csv", index=False)

print("Validation complete.")
print("Total combinations checked:", len(results))
print("Flagged suspicious rows:", len(flagged))

print("\nSkin profile distribution:")
print(results["skin_profile"].value_counts())

print("\nBase skin type distribution:")
print(results["base_skin_type"].value_counts())

print("\nFlag examples:")
print(flagged[[
    "skin_profile",
    "oiliness_score",
    "dryness_score",
    "sensitivity_score",
    "acne_score",
    "barrier_score",
    "flags"
]].head(20))