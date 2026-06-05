import pandas as pd

df = pd.read_csv("model_training_data_3.csv")

trait_cols = [
    "oiliness_score",
    "dryness_score",
    "sensitivity_score",
    "acne_score",
    "barrier_score"
]

print("\nDataset shape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nTrait score ranges:")
print(df[trait_cols].agg(["min", "max", "mean"]))

print("\nTrait score distributions:")
for col in trait_cols:
    print(f"\n{col}")
    print(df[col].value_counts().sort_index())

print("\nAverage trait scores by base skin type:")
print(df.groupby("base_skin_type")[trait_cols].mean().round(2))

print("\nAverage trait scores by acne-prone tag:")
print(df.groupby("acne_prone_tag")[trait_cols].mean().round(2))

print("\nPossible combination-skin style rows:")
combo_like = df[
    (df["oiliness_score"] >= 2) &
    (df["dryness_score"] >= 3)
]
print(combo_like.shape)
print(combo_like.head(10))

print("\nSuspicious rows: high oiliness but low oil signals")
suspicious_oily = df[
    (df["oiliness_score"] >= 4) &
    (df["midday_shine"] <= 2) &
    (df["bare_skin_feel_30min"] <= 3)
]
print(suspicious_oily.shape)
print(suspicious_oily.head())

print("\nSuspicious rows: high dryness but low dryness signals")
suspicious_dry = df[
    (df["dryness_score"] >= 4) &
    (df["tight_flaky_frequency"] <= 1) &
    (df["bare_skin_feel_30min"] >= 3)
]
print(suspicious_dry.shape)
print(suspicious_dry.head())

print("\nSuspicious rows: high sensitivity but low sensitivity signals")
suspicious_sensitive = df[
    (df["sensitivity_score"] >= 4) &
    (df["new_product_reaction"] <= 2) &
    (df["redness_frequency"] <= 2)
]
print(suspicious_sensitive.shape)
print(suspicious_sensitive.head())

print("\nSuspicious rows: strong barrier but high irritation")
suspicious_barrier = df[
    (df["barrier_score"] >= 4) &
    (
        (df["post_cleanse_feel"] >= 3) |
        (df["new_product_reaction"] >= 3) |
        (df["redness_frequency"] >= 3)
    )
]
print(suspicious_barrier.shape)
print(suspicious_barrier.head())

print("\nValidation complete.")