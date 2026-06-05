import pandas as pd

df = pd.read_csv("synthetic_skincare_questionnaire_3.csv")


def compute_oiliness(row):
    score = 0

    # Shine is the strongest oiliness signal
    if row["midday_shine"] == 5:
        score += 3
    elif row["midday_shine"] == 4:
        score += 2
    elif row["midday_shine"] == 3:
        score += 1

    # Pores support oiliness but are not mandatory
    if row["pore_visibility"] >= 4:
        score += 1.5
    elif row["pore_visibility"] == 3:
        score += 0.5

    # 30-min bare skin feel adds supporting evidence
    if row["bare_skin_feel_30min"] == 5:
        score += 1.5
    elif row["bare_skin_feel_30min"] == 4:
        score += 0.5

    return min(round(score), 5)


def compute_dryness(row):
    score = 0

    # Tightness/flaking is the strongest dryness signal
    if row["tight_flaky_frequency"] == 4:
        score += 3
    elif row["tight_flaky_frequency"] == 3:
        score += 2
    elif row["tight_flaky_frequency"] == 2:
        score += 1

    # Bare skin tightness supports dryness
    if row["bare_skin_feel_30min"] == 1:
        score += 1.5
    elif row["bare_skin_feel_30min"] == 2:
        score += 1

    # Post-cleanse discomfort supports dryness/barrier weakness
    if row["post_cleanse_feel"] >= 3:
        score += 1

    # Seasonal dryness / mixed dryness signal
    if row["seasonal_change"] in [3, 4]:
        score += 1

    return min(round(score), 5)


def compute_sensitivity(row):
    score = 0

    # Product reaction (main driver)
    if row["new_product_reaction"] == 4:
        score += 2.5
    elif row["new_product_reaction"] == 3:
        score += 2
    elif row["new_product_reaction"] == 2:
        score += 1

    # Redness (strong signal)
    if row["redness_frequency"] == 4:
        score += 2
    elif row["redness_frequency"] == 3:
        score += 1

    # Post-cleanse irritation
    if row["post_cleanse_feel"] == 4:
        score += 1.5
    elif row["post_cleanse_feel"] == 3:
        score += 1

    # Seasonal reactivity
    if row["seasonal_change"] == 5:
        score += 1
    elif row["seasonal_change"] == 4:
        score += 0.5

    return max(min(round(score), 5), 0)

def compute_acne(row):
    score = 0

    # Breakout frequency is the strongest acne signal
    if row["breakout_frequency"] == 4:
        score += 3
    elif row["breakout_frequency"] == 3:
        score += 2
    elif row["breakout_frequency"] == 2:
        score += 0.5

    # Location supports acne pattern
    if row["breakout_location"] == 5:
        score += 1.5
    elif row["breakout_location"] in [2, 4]:
        score += 1
    elif row["breakout_location"] == 3:
        score += 0.5

    # Hormonal/stress pattern supports acne tendency
    if row["hormonal_stress_pattern"] == 4:
        score += 1
    elif row["hormonal_stress_pattern"] == 3:
        score += 0.5

    return min(round(score), 5)


def compute_barrier(row):
    score = 5

    # Cleanser discomfort weakens barrier confidence
    if row["post_cleanse_feel"] >= 3:
        score -= 2

    # Product reaction weakens barrier confidence
    if row["new_product_reaction"] >= 3:
        score -= 2

    # Flaking/tightness suggests barrier stress
    if row["tight_flaky_frequency"] == 4:
        score -= 1.5
    elif row["tight_flaky_frequency"] == 3:
        score -= 1

    # Frequent redness suggests barrier/inflammation issue
    if row["redness_frequency"] == 4:
        score -= 1
    elif row["redness_frequency"] == 3:
        score -= 0.5

    # Weather reactivity suggests weaker resilience
    if row["seasonal_change"] == 5:
        score -= 1

    return max(round(score), 0)


df["oiliness_score"] = df.apply(compute_oiliness, axis=1)
df["dryness_score"] = df.apply(compute_dryness, axis=1)
df["sensitivity_score"] = df.apply(compute_sensitivity, axis=1)
df["acne_score"] = df.apply(compute_acne, axis=1)
df["barrier_score"] = df.apply(compute_barrier, axis=1)

df.to_csv("model_training_data_3.csv", index=False)
df.to_csv(r"E:\project\skincare\skincare\scripts\model_training_data_3.csv", index=False)

print("Dataset transformed and saved as model_training_data.csv")
print(df.head())

print("\nTrait score ranges:")
print(df[
    [
        "oiliness_score",
        "dryness_score",
        "sensitivity_score",
        "acne_score",
        "barrier_score",
    ]
].agg(["min", "max"]))

print("\nTrait score distribution:")
for col in [
    "oiliness_score",
    "dryness_score",
    "sensitivity_score",
    "acne_score",
    "barrier_score",
]:
    print(f"\n{col}")
    print(df[col].value_counts().sort_index())