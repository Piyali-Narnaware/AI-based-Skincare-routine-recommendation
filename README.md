# AI-based Skincare Routine Recommendation

## Purpose

This project is an **AI-powered skincare recommendation system** that analyzes a user's skin through a 13-question questionnaire and provides personalized skincare guidance. It predicts five key skin trait scores (oiliness, dryness, sensitivity, acne tendency, barrier health) using a Random Forest regression model, then classifies the skin type and generates tailored recommendations for ingredients, products, routines, and behaviours.

The goal is to make skincare science-backed and personalized — replacing guesswork with data-driven suggestions.

---

## Tools Used

| Tool | Purpose |
|------|---------|
| **Python 3.11** | Core programming language |
| **Streamlit** | Web UI framework for the interactive questionnaire |
| **scikit-learn** | Random Forest Regressor model for trait prediction |
| **pandas / numpy** | Data handling and manipulation |
| **Git & GitHub** | Version control and remote hosting |

### Project Structure

```
src/
├── recommendation_engine.py   # Ingredient & behaviour rules engine
├── product_matcher.py         # Scores products against ingredient rules
├── routine_engine.py          # Builds AM/PM routines with conflict detection
├── skin_classifier.py         # Skin type classification logic
├── product_database.py        # Loads product data from CSV
├── ingredient_parser.py       # Parses raw INCI ingredient strings
├── main_pipeline.py           # CLI demo pipeline
└── validate_all_combinations.py  # Brute-force validation tool
```

---

## Output

The system produces a complete skincare analysis including:

1. **Trait Scores** — 5 numerical scores (oiliness, dryness, sensitivity, acne, barrier)
2. **Skin Profile** — e.g. "Oily-leaning combination + sensitive + acne-prone"
3. **Condition Tags** — e.g. acne_prone, barrier_impaired, dehydration_prone
4. **Ingredients to Use / Avoid** — personalized ingredient guidance
5. **Product Recommendations** — specific products scored by ingredient match
6. **Smart Routine** — morning/night routine with conflict warnings and pairing suggestions

### Sample Output

```
Trait Scores:        Oiliness 2.9 | Dryness 1.55 | Sensitivity 1.53
                     Acne 3.89 | Barrier 4.81

Skin Profile:        Oily + acne-prone

Top Products:        The Derma Co Salicylic Acid Serum (Score: 90)
                     Minimalist 2% SA Face Wash (Score: 60)

Routine:             AM — niacinamide, zinc pca, green tea
                     PM — salicylic acid, azelaic acid
```

---

## How the System Can Be Useful

- **Consumers** — Get personalized skincare advice without expensive dermatologist visits
- **Skincare brands** — Integrate recommendation logic into e-commerce for customer guidance
- **Educators** — Demonstrate how ML + rule-based systems can solve real-world problems
- **Developers** — Use as a template for building domain-specific recommendation engines

---

## Future Scope

- **Deep learning model** — Replace Random Forest with a neural network for higher accuracy
- **Larger product database** — Scrape or API-integrate thousands of products with real-time pricing
- **User feedback loop** — Let users rate recommendations and retrain the model over time
- **Image-based analysis** — Add computer vision to assess skin from photos
- **Mobile app** — Wrap the engine in a React Native / Flutter frontend
- **Multi-language support** — Expand questionnaire and recommendations to regional languages
- **REST API** — Serve predictions via FastAPI for third-party integrations
