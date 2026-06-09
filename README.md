# AI-Powered Skincare Routine Recommendation

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)

An intelligent skincare recommendation system that predicts **5 skin traits** from a **13-question quiz** using Random Forest regression, scores **151 products** by ingredient match with concentration weighting and brand trust, and builds personalised AM/PM routines with ingredient conflict detection.

---

## How It Works

```
┌──────────────┐     ┌──────────────────┐     ┌───────────────────┐     ┌──────────────────┐
│  User Quiz   │────▶│  Random Forest   │────▶│  Product Scorer   │────▶│  Routine Builder │
│  13 Qs       │     │  Regressor       │     │  (151 products)   │     │  AM/PM +         │
│              │     │  Predicts 5      │     │  Ingredient match │     │  Conflict checks │
│              │     │  skin traits     │     │  + brand trust    │     │  + budget filter │
└──────────────┘     └──────────────────┘     └───────────────────┘     └──────────────────┘
```

### Skin Traits Predicted

1. **Oiliness** — Sebum production level
2. **Dryness** — Moisture retention
3. **Sensitivity** — Reaction tendency
4. **Acne Tendency** — Breakout likelihood
5. **Barrier Health** — Skin barrier strength

### Skin Types Classified

Oily, Dry, Combination, Sensitive, Normal — with sub-types (e.g. *"oily-leaning combination + sensitive + acne-prone"*)

---

## Key Features

- **13-Question Quiz** — Covers skin concerns, diet, lifestyle, environment, and current routine
- **Random Forest Regression** — 5 independent regressors, each predicting one skin trait score (0–10)
- **Ingredient Synonym Engine** — Handles alternative names (e.g. "tocopherol" ↔ "vitamin E") for accurate product matching
- **Concentration-Weighted Scoring** — Products ranked by ingredient match strength, concentration level, and brand trust score
- **AM/PM Routine Generator** — Builds morning and evening routines with product synergy notes and conflict warnings (e.g. retinol + salicylic acid)
- **Budget Tiers** — Budget, Mid-range, Premium for both Indian (INR) and UK (GBP) markets
- **Behaviours to Avoid** — Personalised bad-practice alerts based on skin type
- **Streamlit Web App** — Interactive UI with real-time recommendations

---

## Project Structure

```
├── app.py                           # Streamlit web application
├── src/
│   ├── ingredient_parser.py         # Ingredient synonym resolution
│   ├── main_pipeline.py             # End-to-end pipeline
│   ├── product_database.py          # Product catalogue (151 products)
│   ├── product_matcher.py           # Ingredient matching & scoring
│   ├── recommendation_engine.py     # Product ranking engine
│   ├── routine_engine.py            # AM/PM routine builder
│   ├── skin_classifier.py           # Skin type classification
│   └── validate_all_combinations.py # Exhaustive validation
├── scripts/
│   ├── modeltraining.py             # Random Forest training
│   ├── generate_traits.py           # Synthetic trait generation
│   ├── test_recommendation_system.py# Integration tests
│   └── data validation.py           # Data quality checks
├── data/
│   ├── raw_product_database.csv     # Raw product data
│   ├── model_training_data_3.csv    # Training dataset
│   └── parsed_product_database.csv  # Cleaned product data
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone https://github.com/Piyali-Narnaware/AI-based-Skincare-routine-recommendation.git
cd AI-based-Skincare-routine-recommendation
pip install -r requirements.txt
```

### Run the Streamlit App

```bash
streamlit run app.py
```

### Train the Model

```bash
python scripts/modeltraining.py
```

---

## Dependencies

- Python 3.11+
- scikit-learn (RandomForestRegressor)
- Streamlit
- pandas, numpy
- Git / GitHub
