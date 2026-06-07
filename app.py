import os
import json
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor

from src.recommendation_engine import generate_recommendations
from src.product_matcher import recommend_products
from src.routine_engine import generate_routine
from src.skin_classifier import classify_skin_type, get_base_skin_type


st.set_page_config(
    page_title="Skincare Recommendation System",
    page_icon="🧴",
    layout="wide"
)

COUNTER_FILE = os.path.join(os.path.dirname(__file__), "data", "visit_count.json")


def get_visit_count():
    try:
        count = 0
        if os.path.exists(COUNTER_FILE):
            with open(COUNTER_FILE, "r") as f:
                data = json.load(f)
                count = data.get("count", 0)
        count += 1
        with open(COUNTER_FILE, "w") as f:
            json.dump({"count": count}, f)
        return count
    except Exception:
        return None


@st.cache_resource
def train_model():
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
        "acne_prone_tag",
    ]

    target_cols = [
        "oiliness_score",
        "dryness_score",
        "sensitivity_score",
        "acne_score",
        "barrier_score",
    ]

    X = df[feature_cols]
    y = df[target_cols]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model, target_cols


model, target_cols = train_model()


def get_match_label(score):
    if score >= 70:
        return "Strong match"
    elif score >= 40:
        return "Good match"
    elif score > 0:
        return "Possible match"
    return "Not recommended"


age_map = {
    "13–19": 1,
    "20–29": 2,
    "30–39": 3,
    "40–49": 4,
    "50+": 5,
}

bare_skin_map = {
    "Very tight or uncomfortable": 1,
    "Slightly tight": 2,
    "Comfortable / balanced": 3,
    "Slightly oily": 4,
    "Very oily or greasy": 5,
}

midday_shine_map = {
    "Dry or dull": 1,
    "Balanced / normal": 2,
    "Shiny only on T-zone": 3,
    "Shiny all over": 4,
    "Very greasy all over": 5,
}

tight_flaky_map = {
    "Rarely or never": 1,
    "Sometimes": 2,
    "Often": 3,
    "Very often": 4,
}

breakout_frequency_map = {
    "Rarely or never": 1,
    "Occasionally, around once a month": 2,
    "Frequently, around weekly": 3,
    "Very frequently, multiple times a week": 4,
}

breakout_location_map = {
    "I rarely get breakouts": 1,
    "Forehead / nose / T-zone": 2,
    "Cheeks": 3,
    "Jawline / chin": 4,
    "All over the face": 5,
}

pore_visibility_map = {
    "Barely visible": 1,
    "Slightly visible": 2,
    "Visible mainly on nose / T-zone": 3,
    "Visible across cheeks and T-zone": 4,
    "Very enlarged across most of the face": 5,
}

new_product_reaction_map = {
    "Usually no reaction": 1,
    "Mild tingling only": 2,
    "Sometimes redness, stinging, or bumps": 3,
    "Often burning, itching, redness, or irritation": 4,
}

redness_map = {
    "Rarely or never": 1,
    "Sometimes": 2,
    "Often": 3,
    "Very often": 4,
}

post_cleanse_map = {
    "Soft and comfortable": 1,
    "Slightly tight but okay": 2,
    "Tight, dry, or squeaky clean": 3,
    "Stinging, burning, or irritated": 4,
}

seasonal_change_map = {
    "Stays mostly the same": 1,
    "Gets oilier in heat or humidity": 2,
    "Gets drier in cold or AC environments": 3,
    "Gets both oily and dry depending on area/season": 4,
    "Gets red, irritated, or reactive with weather changes": 5,
}

hormonal_map = {
    "Rarely or never": 1,
    "Sometimes": 2,
    "Often during stress or lifestyle changes": 3,
    "Very often / clear monthly or hormonal pattern": 4,
}


col_title, col_counter = st.columns([10, 1])
with col_title:
    st.title("🧴 Skincare Recommendation System")
with col_counter:
    visit_count = get_visit_count()
    if visit_count is not None:
        st.caption(f"👁️ {visit_count}")

st.write(
    "Answer the questions below to get your skin analysis, ingredient guidance, "
    "routine suggestions, and product recommendations."
)

st.divider()

st.header("Skin Questionnaire")

col1, col2 = st.columns(2)

with col1:
    age_group_label = st.selectbox("Age group", list(age_map.keys()))

    bare_skin_label = st.selectbox(
        "How does your skin feel 30 minutes after washing, with no product?",
        list(bare_skin_map.keys())
    )

    midday_shine_label = st.selectbox(
        "How does your skin usually look by midday?",
        list(midday_shine_map.keys())
    )

    tight_flaky_label = st.selectbox(
        "How often does your skin feel tight, flaky, or rough?",
        list(tight_flaky_map.keys())
    )

    pore_visibility_label = st.selectbox(
        "How visible are your pores?",
        list(pore_visibility_map.keys())
    )

    breakout_frequency_label = st.selectbox(
        "How often do you get breakouts?",
        list(breakout_frequency_map.keys())
    )

with col2:
    breakout_location_label = st.selectbox(
        "Where do you usually get breakouts?",
        list(breakout_location_map.keys())
    )

    new_product_reaction_label = st.selectbox(
        "How does your skin react when trying a new product?",
        list(new_product_reaction_map.keys())
    )

    redness_label = st.selectbox(
        "How often do you experience unexplained redness or flushing?",
        list(redness_map.keys())
    )

    post_cleanse_label = st.selectbox(
        "How does your skin feel after using a cleanser?",
        list(post_cleanse_map.keys())
    )

    seasonal_change_label = st.selectbox(
        "How does your skin change with weather or seasons?",
        list(seasonal_change_map.keys())
    )

    hormonal_label = st.selectbox(
        "Do breakouts or skin changes happen around hormones, stress, or lifestyle changes?",
        list(hormonal_map.keys())
    )

region_label = st.selectbox(
    "Which region's products would you like recommendations for?",
    ["India", "UK"]
)

budget_label = st.selectbox(
    "Budget preference",
    ["All", "Budget", "Mid-range", "Premium"]
)

acne_prone_label = st.radio(
    "Do you consider your skin acne-prone?",
    ["No", "Yes"],
    horizontal=True
)

st.divider()


if st.button("Analyze My Skin", type="primary"):

    user_answers = {
        "age_group": age_map[age_group_label],
        "bare_skin_feel_30min": bare_skin_map[bare_skin_label],
        "midday_shine": midday_shine_map[midday_shine_label],
        "tight_flaky_frequency": tight_flaky_map[tight_flaky_label],
        "pore_visibility": pore_visibility_map[pore_visibility_label],
        "breakout_frequency": breakout_frequency_map[breakout_frequency_label],
        "breakout_location": breakout_location_map[breakout_location_label],
        "hormonal_stress_pattern": hormonal_map[hormonal_label],
        "new_product_reaction": new_product_reaction_map[new_product_reaction_label],
        "redness_frequency": redness_map[redness_label],
        "post_cleanse_feel": post_cleanse_map[post_cleanse_label],
        "seasonal_change": seasonal_change_map[seasonal_change_label],
        "acne_prone_tag": 1 if acne_prone_label == "Yes" else 0,
    }

    user_input = pd.DataFrame([user_answers])

    prediction = model.predict(user_input)[0]

    trait_scores = pd.Series(
        prediction,
        index=target_cols
    )

    predicted_skin_profile = classify_skin_type(
        trait_scores,
        user_answers
    )

    base_skin_type = get_base_skin_type(predicted_skin_profile)

    recommendations = generate_recommendations(
        base_skin_type,
        trait_scores
    )

    product_results = recommend_products(recommendations, region=region_label, budget=budget_label)
    routine = generate_routine(recommendations)

    st.header("Your Skin Analysis")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Skin profile", predicted_skin_profile.title())

    with c2:
        st.metric("Acne tendency", round(trait_scores["acne_score"], 2))

    with c3:
        st.metric("Barrier health", round(trait_scores["barrier_score"], 2))

    st.subheader("Model Trait Scores")

    trait_display = pd.DataFrame({
        "Trait": [
            "Oiliness",
            "Dryness",
            "Sensitivity",
            "Acne tendency",
            "Barrier health",
        ],
        "Score": [
            round(trait_scores["oiliness_score"], 2),
            round(trait_scores["dryness_score"], 2),
            round(trait_scores["sensitivity_score"], 2),
            round(trait_scores["acne_score"], 2),
            round(trait_scores["barrier_score"], 2),
        ],
    })

    st.dataframe(trait_display, width="stretch")

    st.subheader("Condition Tags")

    if recommendations["condition_tags"]:
        readable_tags = [
            tag.replace("_", " ").title()
            for tag in recommendations["condition_tags"]
        ]
        st.write(", ".join(readable_tags))
    else:
        st.write("No major condition tags detected.")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Ingredients to Use")
        for item in recommendations["ingredients_to_use"]:
            st.write(f"✅ {item}")

    with right:
        st.subheader("Ingredients to Avoid")
        for item in recommendations["ingredients_to_avoid"]:
            st.write(f"⚠️ {item}")

    st.subheader("Behaviours to Avoid")
    for item in recommendations["behaviours_to_avoid"]:
        st.write(f"• {item}")

    st.divider()

    st.header("Smart Usage Routine")

    r1, r2 = st.columns(2)

    with r1:
        st.subheader("Morning")
        if routine["morning_routine"]:
            for item in routine["morning_routine"]:
                st.write(f"☀️ {item}")
        else:
            st.write("No specific morning actives detected.")

    with r2:
        st.subheader("Night")
        if routine["night_routine"]:
            for item in routine["night_routine"]:
                st.write(f"🌙 {item}")
        else:
            st.write("No specific night actives detected.")

    if routine["conflicts"]:
        st.warning("Ingredient warnings:")
        for warning in routine["conflicts"]:
            st.write(f"⚠️ {warning}")

    if routine["pairings"]:
        st.success("Why this works well:")
        for pair in routine["pairings"]:
            st.write(f"✅ {pair}")

    st.divider()

    st.header("Recommended Product Routine")

    routine_order = [
        "cleanser",
        "serum",
        "treatment",
        "moisturiser",
        "sunscreen",
    ]

    category_map = {
        product["category"].strip().lower(): product
        for product in product_results["category_recommendations"]
    }

    for category in routine_order:
        if category in category_map:
            product = category_map[category]

            with st.container(border=True):
                st.subheader(category.title())
                st.write(f"**{product['product_name']}**")
                st.write(f"Brand: {product['brand']}")
                price = product['price_gbp'] if region_label == "UK" else product['price_inr']
                sym = "£" if region_label == "UK" else "₹"
                st.write(f"Price: {sym}{price}")
                st.write(f"Match: {get_match_label(product['score'])}")
                st.markdown(product["why_recommended"])

    currency = "£" if region_label == "UK" else "₹"
    st.caption(f"Showing products available in **{region_label}** | Budget: **{budget_label}**")

    st.header("Products to Avoid")

    if product_results["avoid_products"]:
        for product in product_results["avoid_products"]:
            with st.container(border=True):
                st.write(f"**{product['product_name']}**")
                st.write(f"Brand: {product['brand']}")
                st.write(f"Category: {product['category']}")
                st.write("Recommendation: Avoid for this profile")
                st.write(f"Problem ingredients: {', '.join(product['matched_bad'])}")
    else:
        st.write("No avoid products detected.")

    st.divider()
    st.caption(
        "⚠️ **Disclaimer:** This is an AI-generated recommendation based on your questionnaire responses. "
        "It is not a substitute for professional dermatological advice. "
        "Always patch-test new products and consult a dermatologist for persistent skin concerns."
    )