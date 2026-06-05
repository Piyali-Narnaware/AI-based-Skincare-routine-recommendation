def classify_skin_type(trait_scores, user_answers):
    oil = trait_scores["oiliness_score"]
    dry = trait_scores["dryness_score"]
    sens_score = trait_scores["sensitivity_score"]
    acne = trait_scores["acne_score"]
    barrier = trait_scores["barrier_score"]

    redness = user_answers["redness_frequency"]
    seasonal = user_answers["seasonal_change"]
    reaction = user_answers["new_product_reaction"]
    pores = user_answers["pore_visibility"]

    sensitive_signals = 0

    if redness >= 3:
        sensitive_signals += 1

    if reaction >= 3:
        sensitive_signals += 1

    if seasonal == 5:
        sensitive_signals += 1

    if barrier <= 3:
        sensitive_signals += 1

    if sens_score >= 3:
        sensitive_signals += 1

    is_sensitive = sensitive_signals >= 2
    is_acne_prone = acne >= 3

    if seasonal == 4 and pores >= 3:
        if dry > oil:
            base_type = "dry-leaning combination"
        elif oil > dry:
            base_type = "oily-leaning combination"
        else:
            base_type = "combination"

    elif dry >= 2.2 and seasonal == 4:
        base_type = "dry-leaning combination"

    elif abs(oil - dry) <= 1 and (oil >= 2 or dry >= 2):
        if dry > oil:
            base_type = "dry-leaning combination"
        elif oil > dry:
            base_type = "oily-leaning combination"
        else:
            base_type = "combination"

    elif oil >= 2.7:
        base_type = "oily"

    elif dry >= 2.3:
        base_type = "dry"

    else:
        base_type = "normal"

    profile_parts = [base_type]

    if is_sensitive and "sensitive" not in base_type:
        profile_parts.append("sensitive")

    if is_acne_prone:
        profile_parts.append("acne-prone")

    return " + ".join(profile_parts)


def get_base_skin_type(profile):
    profile = profile.lower()

    if "sensitive" in profile:
        return "sensitive"
    if "combination" in profile:
        return "combination"
    if "oily" in profile:
        return "oily"
    if "dry" in profile:
        return "dry"

    return "normal"