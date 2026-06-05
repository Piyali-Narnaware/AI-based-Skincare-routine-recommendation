import numpy as np
import pandas as pd

np.random.seed(42)

n = 1000

base_skin_types = np.random.choice(
    ["dry", "normal", "oily", "combination", "sensitive"],
    size=n,
    p=[0.20, 0.22, 0.20, 0.25, 0.13]
)

rows = []


def choose(options, probs):
    return np.random.choice(options, p=probs)


def is_invalid_combination(row):
    if row["breakout_frequency"] >= 3 and row["breakout_location"] == 1:
        return True

    if row["breakout_frequency"] == 1 and row["breakout_location"] == 5:
        return True

    if row["bare_skin_feel_30min"] == 5 and row["midday_shine"] == 1:
        return True

    if (
        row["bare_skin_feel_30min"] == 1
        and row["midday_shine"] == 5
        and row["seasonal_change"] != 4
        and row["pore_visibility"] < 3
    ):
        return True

    if (
        row["pore_visibility"] >= 4
        and row["midday_shine"] == 1
        and row["bare_skin_feel_30min"] <= 2
    ):
        return True

    if (
        row["redness_frequency"] >= 4
        and row["new_product_reaction"] <= 1
        and row["post_cleanse_feel"] <= 1
        and row["seasonal_change"] != 5
    ):
        return True

    return False


while len(rows) < n:
    skin = base_skin_types[len(rows)]
    row = {}

    row["age_group"] = choose(
        [1, 2, 3, 4, 5],
        [0.12, 0.35, 0.25, 0.18, 0.10]
    )

    # -------------------------
    # BASE SKIN PATTERN LOGIC
    # -------------------------

    if skin == "dry":
        dry_pattern = choose(
            ["classic_dry", "dehydrated_dry", "mild_dry"],
            [0.50, 0.30, 0.20]
        )

        if dry_pattern == "classic_dry":
            row["bare_skin_feel_30min"] = choose([1, 2], [0.60, 0.40])
            row["midday_shine"] = choose([1, 2], [0.70, 0.30])
            row["tight_flaky_frequency"] = choose([3, 4], [0.55, 0.45])
            row["pore_visibility"] = choose([1, 2], [0.60, 0.40])

        elif dry_pattern == "dehydrated_dry":
            row["bare_skin_feel_30min"] = choose([1, 2], [0.50, 0.50])
            row["midday_shine"] = choose([2, 3], [0.65, 0.35])
            row["tight_flaky_frequency"] = choose([3, 4], [0.45, 0.55])
            row["pore_visibility"] = choose([2, 3], [0.60, 0.40])

        else:
            row["bare_skin_feel_30min"] = choose([2, 3], [0.65, 0.35])
            row["midday_shine"] = choose([1, 2], [0.45, 0.55])
            row["tight_flaky_frequency"] = choose([2, 3], [0.70, 0.30])
            row["pore_visibility"] = choose([1, 2, 3], [0.40, 0.45, 0.15])

    elif skin == "oily":
        oily_pattern = choose(
            [
                "high_shine_large_pores",
                "high_shine_small_pores",
                "moderate_shine_large_pores",
                "tzone_oily_mixed_pores"
            ],
            [0.35, 0.25, 0.20, 0.20]
        )

        if oily_pattern == "high_shine_large_pores":
            row["bare_skin_feel_30min"] = choose([4, 5], [0.45, 0.55])
            row["midday_shine"] = choose([4, 5], [0.45, 0.55])
            row["pore_visibility"] = choose([4, 5], [0.45, 0.55])
            row["tight_flaky_frequency"] = choose([1, 2], [0.75, 0.25])

        elif oily_pattern == "high_shine_small_pores":
            row["bare_skin_feel_30min"] = choose([4, 5], [0.50, 0.50])
            row["midday_shine"] = choose([4, 5], [0.45, 0.55])
            row["pore_visibility"] = choose([2, 3], [0.55, 0.45])
            row["tight_flaky_frequency"] = choose([1, 2], [0.80, 0.20])

        elif oily_pattern == "moderate_shine_large_pores":
            row["bare_skin_feel_30min"] = choose([3, 4], [0.55, 0.45])
            row["midday_shine"] = choose([3, 4], [0.60, 0.40])
            row["pore_visibility"] = choose([4, 5], [0.60, 0.40])
            row["tight_flaky_frequency"] = choose([1, 2], [0.70, 0.30])

        else:
            row["bare_skin_feel_30min"] = choose([3, 4], [0.45, 0.55])
            row["midday_shine"] = 3
            row["pore_visibility"] = choose([2, 3, 4], [0.25, 0.50, 0.25])
            row["tight_flaky_frequency"] = choose([1, 2, 3], [0.45, 0.40, 0.15])

    elif skin == "combination":
        combo_pattern = choose(
            ["classic_combo", "dehydrated_combo", "oily_tzone_dry_cheeks"],
            [0.45, 0.30, 0.25]
        )

        if combo_pattern == "classic_combo":
            row["bare_skin_feel_30min"] = choose([2, 3, 4], [0.20, 0.50, 0.30])
            row["midday_shine"] = 3
            row["tight_flaky_frequency"] = choose([1, 2, 3], [0.25, 0.55, 0.20])
            row["pore_visibility"] = choose([2, 3, 4], [0.20, 0.55, 0.25])

        elif combo_pattern == "dehydrated_combo":
            row["bare_skin_feel_30min"] = choose([1, 2, 3], [0.25, 0.50, 0.25])
            row["midday_shine"] = choose([3, 4], [0.60, 0.40])
            row["tight_flaky_frequency"] = choose([2, 3], [0.45, 0.55])
            row["pore_visibility"] = choose([2, 3, 4], [0.20, 0.55, 0.25])

        else:
            row["bare_skin_feel_30min"] = choose([2, 3, 4], [0.35, 0.40, 0.25])
            row["midday_shine"] = choose([3, 4], [0.55, 0.45])
            row["tight_flaky_frequency"] = choose([2, 3], [0.55, 0.45])
            row["pore_visibility"] = choose([3, 4], [0.60, 0.40])

    elif skin == "sensitive":
        sensitive_pattern = choose(
            ["dry_sensitive", "normal_sensitive", "oily_sensitive"],
            [0.45, 0.35, 0.20]
        )

        if sensitive_pattern == "dry_sensitive":
            row["bare_skin_feel_30min"] = choose([1, 2, 3], [0.35, 0.45, 0.20])
            row["midday_shine"] = choose([1, 2], [0.45, 0.55])
            row["tight_flaky_frequency"] = choose([3, 4], [0.55, 0.45])
            row["pore_visibility"] = choose([1, 2, 3], [0.45, 0.40, 0.15])

        elif sensitive_pattern == "oily_sensitive":
            row["bare_skin_feel_30min"] = choose([3, 4], [0.45, 0.55])
            row["midday_shine"] = choose([3, 4], [0.55, 0.45])
            row["tight_flaky_frequency"] = choose([1, 2, 3], [0.35, 0.45, 0.20])
            row["pore_visibility"] = choose([2, 3, 4], [0.25, 0.50, 0.25])

        else:
            row["bare_skin_feel_30min"] = choose([2, 3], [0.45, 0.55])
            row["midday_shine"] = choose([1, 2, 3], [0.20, 0.55, 0.25])
            row["tight_flaky_frequency"] = choose([1, 2, 3], [0.25, 0.50, 0.25])
            row["pore_visibility"] = choose([1, 2, 3], [0.30, 0.50, 0.20])

    else:  # normal
        normal_pattern = choose(
            ["balanced_normal", "slightly_oily_normal", "slightly_dry_normal"],
            [0.60, 0.20, 0.20]
        )

        if normal_pattern == "balanced_normal":
            row["bare_skin_feel_30min"] = 3
            row["midday_shine"] = 2
            row["tight_flaky_frequency"] = choose([1, 2], [0.75, 0.25])
            row["pore_visibility"] = choose([1, 2, 3], [0.30, 0.55, 0.15])

        elif normal_pattern == "slightly_oily_normal":
            row["bare_skin_feel_30min"] = choose([3, 4], [0.70, 0.30])
            row["midday_shine"] = choose([2, 3], [0.55, 0.45])
            row["tight_flaky_frequency"] = choose([1, 2], [0.80, 0.20])
            row["pore_visibility"] = choose([2, 3], [0.55, 0.45])

        else:
            row["bare_skin_feel_30min"] = choose([2, 3], [0.45, 0.55])
            row["midday_shine"] = choose([1, 2], [0.35, 0.65])
            row["tight_flaky_frequency"] = choose([1, 2, 3], [0.40, 0.50, 0.10])
            row["pore_visibility"] = choose([1, 2], [0.50, 0.50])

    # -------------------------
    # ACNE TRAIT
    # -------------------------
    is_acne_prone = choose([0, 1], [0.75, 0.25])

    if is_acne_prone:
        row["breakout_frequency"] = choose([3, 4], [0.60, 0.40])
        row["breakout_location"] = choose([2, 3, 4, 5], [0.30, 0.20, 0.30, 0.20])
        row["hormonal_stress_pattern"] = choose([2, 3, 4], [0.25, 0.45, 0.30])
    else:
        row["breakout_frequency"] = choose([1, 2, 3], [0.50, 0.40, 0.10])
        row["breakout_location"] = 1 if row["breakout_frequency"] == 1 else choose([2, 3, 4], [0.35, 0.30, 0.35])
        row["hormonal_stress_pattern"] = choose([1, 2, 3], [0.45, 0.40, 0.15])

    # -------------------------
    # SENSITIVITY SIGNALS
    # -------------------------
    if skin == "sensitive":
        row["new_product_reaction"] = choose([3, 4], [0.55, 0.45])
        row["redness_frequency"] = choose([3, 4], [0.60, 0.40])
        row["post_cleanse_feel"] = choose([3, 4], [0.45, 0.55])
    else:
        row["new_product_reaction"] = choose([1, 2, 3], [0.45, 0.35, 0.20])
        row["redness_frequency"] = choose([1, 2, 3], [0.50, 0.35, 0.15])
        row["post_cleanse_feel"] = choose([1, 2, 3], [0.45, 0.35, 0.20])

    # -------------------------
    # SEASONAL / ENVIRONMENT SIGNAL
    # -------------------------
    if skin == "dry":
        row["seasonal_change"] = choose([1, 3, 4, 5], [0.15, 0.50, 0.20, 0.15])
    elif skin == "oily":
        row["seasonal_change"] = choose([1, 2, 4], [0.25, 0.60, 0.15])
    elif skin == "combination":
        row["seasonal_change"] = choose([2, 3, 4], [0.25, 0.25, 0.50])
    elif skin == "sensitive":
        row["seasonal_change"] = choose([3, 4, 5], [0.25, 0.25, 0.50])
    else:
        row["seasonal_change"] = choose([1, 2, 3], [0.55, 0.25, 0.20])

    row["base_skin_type"] = skin
    row["acne_prone_tag"] = is_acne_prone

    if is_invalid_combination(row):
        continue

    rows.append(row)

df = pd.DataFrame(rows)

df.to_csv("synthetic_skincare_questionnaire_3.csv", index=False)
df.to_csv(r"E:\project\skincare\skincare\scripts\synthetic_skincare_questionnaire_3.csv", index=False)

print(df.head())
print("\nDataset saved successfully.")
print("\nBase skin type distribution:")
print(df["base_skin_type"].value_counts())
print("\nAcne-prone tag distribution:")
print(df["acne_prone_tag"].value_counts())