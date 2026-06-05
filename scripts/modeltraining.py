import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load dataset
df = pd.read_csv("model_training_data_3.csv")

# Features (inputs)
X = df.drop(columns=[
    "oiliness_score",
    "dryness_score",
    "sensitivity_score",
    "acne_score",
    "barrier_score",
    "base_skin_type"  # not needed for training
])

# Targets (outputs)
y = df[[
    "oiliness_score",
    "dryness_score",
    "sensitivity_score",
    "acne_score",
    "barrier_score"
]]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, y_pred)

print("Mean Absolute Error:", mae)

from sklearn.metrics import mean_absolute_error

trait_names = [
    "oiliness_score",
    "dryness_score",
    "sensitivity_score",
    "acne_score",
    "barrier_score"
]

print("\nTrait-wise MAE:")

for i, trait in enumerate(trait_names):
    mae_trait = mean_absolute_error(y_test.iloc[:, i], y_pred[:, i])
    print(f"{trait}: {round(mae_trait, 3)}")


feature_names = X.columns

print("\nFeature Importance (averaged across all traits):")

importances = model.feature_importances_

# Sort features
indices = np.argsort(importances)[::-1]

for i in indices:
    print(f"{feature_names[i]}: {round(importances[i], 4)}")


pred_df = pd.DataFrame(
    y_pred,
    columns=[
        "oiliness_score",
        "dryness_score",
        "sensitivity_score",
        "acne_score",
        "barrier_score"
    ],
    index=X_test.index
)

def classify_skin_type(row):
    oil = row["oiliness_score"]
    dry = row["dryness_score"]
    sens = row["sensitivity_score"]

    # Sensitive override
    if sens >= 4:
        return "sensitive"

    # Combination (relaxed condition)
    if abs(oil - dry) <= 1 and oil >= 2:
        return "combination"

    # Oily
    if oil >= 3:
        return "oily"

    # Dry
    if dry >= 3:
        return "dry"

    return "normal"

pred_df["predicted_skin_type"] = pred_df.apply(classify_skin_type, axis=1)

print("\nPredicted skin types:")
print(pred_df["predicted_skin_type"].value_counts())

print("\nPrediction preview:")
print(pred_df.head())