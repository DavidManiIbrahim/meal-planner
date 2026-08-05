"""
Expert System — Knowledge Base and Inference Engine
Calculates BMI, daily calorie targets, and macronutrient distribution
based on a user's Profile using rule-based (IF-THEN) logic.
"""

# ---------- KNOWLEDGE BASE ----------

BMI_RULES = {
    'underweight': {
        'range': (0, 18.5),
        'calorie_adjustment': 500,
        'advice': "You are underweight. Increasing your calorie intake is recommended.",
    },
    'normal': {
        'range': (18.5, 25),
        'calorie_adjustment': 0,
        'advice': "Your weight is within a healthy range. Maintain your current balance.",
    },
    'overweight': {
        'range': (25, 30),
        'calorie_adjustment': -300,
        'advice': "You are overweight. Reducing calorie intake and increasing protein is recommended.",
    },
    'obese': {
        'range': (30, 999),
        'calorie_adjustment': -500,
        'advice': "A significant calorie reduction is recommended, alongside regular activity.",
    },
}

GOAL_RULES = {
    'lose': {
        'protein_pct': 40,
        'carb_pct': 30,
        'fat_pct': 30,
        'meal_frequency': 5,
        'advice': "Higher protein helps preserve muscle while losing fat.",
    },
    'maintain': {
        'protein_pct': 30,
        'carb_pct': 40,
        'fat_pct': 30,
        'meal_frequency': 3,
        'advice': "Balanced macronutrients support weight maintenance.",
    },
    'gain': {
        'protein_pct': 30,
        'carb_pct': 50,
        'fat_pct': 20,
        'meal_frequency': 6,
        'advice': "Higher carbohydrates provide energy to support weight gain.",
    },
}

AGE_RULES = {
    'teen': {
        'range': (0, 17),
        'advice': "Growing teens need extra calcium and iron in their diet.",
    },
    'young_adult': {
        'range': (18, 35),
        'advice': "Focus on balanced nutrition to support energy and activity levels.",
    },
    'middle_aged': {
        'range': (36, 55),
        'advice': "Reducing sodium and increasing fibre intake is recommended at this age.",
    },
    'senior': {
        'range': (56, 999),
        'advice': "Focus on calcium-rich, easily digestible foods.",
    },
}


# ---------- INFERENCE ENGINE ----------

def get_bmi_category(bmi):
    for category, rule in BMI_RULES.items():
        low, high = rule['range']
        if low <= bmi < high:
            return category
    return 'normal'


def get_age_group(age):
    for group, rule in AGE_RULES.items():
        low, high = rule['range']
        if low <= age <= high:
            return group
    return 'young_adult'


def run_expert_system(profile):
    """
    Takes a Profile instance and returns a dict of calculated targets and advice.
    This is the main inference function — it applies all the IF-THEN rules
    in sequence to produce a personalised nutrition recommendation.
    """

    advice_list = []

    # Step 1 — BMI
    bmi = profile.bmi()
    bmi_category = get_bmi_category(bmi)
    bmi_rule = BMI_RULES[bmi_category]
    advice_list.append(bmi_rule['advice'])

    # Step 2 — Age group
    age_group = get_age_group(profile.age)
    age_rule = AGE_RULES[age_group]
    advice_list.append(age_rule['advice'])

    # Step 3 — Goal (macronutrient split + meal frequency)
    goal_rule = GOAL_RULES[profile.goal]
    advice_list.append(goal_rule['advice'])

    # Step 4 — BMR (already a method on Profile)
    bmr = profile.bmr()

    # Step 5 — Final daily calorie target = BMR adjusted by BMI category
    daily_calories = bmr + bmi_rule['calorie_adjustment']
    daily_calories = max(daily_calories, 1200)  # safety floor, never go below 1200 kcal

    # Step 6 — Macronutrient grams from percentages
    protein_grams = round((daily_calories * goal_rule['protein_pct'] / 100) / 4)
    carb_grams = round((daily_calories * goal_rule['carb_pct'] / 100) / 4)
    fat_grams = round((daily_calories * goal_rule['fat_pct'] / 100) / 9)
    return {
        'bmi': bmi,
        'bmi_category': bmi_category,
        'age_group': age_group,
        'daily_calories': round(daily_calories),
        'protein_grams': protein_grams,
        'carb_grams': carb_grams,
        'fat_grams': fat_grams,
        'meal_frequency': goal_rule['meal_frequency'],
        'advice': advice_list,
    }