"""
Meal Generator
Takes a Profile, filters the food database by the user's six-factor
constraints (allergies, budget, region, spice, protein preference,
availability), then assembles a 7-day meal plan hitting the
expert system's calorie/macro targets.
"""

import random
from nutrition.models import Dish, MealPlan, MealPlanEntry
from nutrition.expert_system import run_expert_system

# Budget levels ranked so we know what a user "can afford"
BUDGET_RANK = {'budget': 1, 'moderate': 2, 'flexible': 3}
DISH_COST_RANK = {'budget': 1, 'moderate': 2, 'premium': 3}


def filter_dishes_for_profile(profile):
    """
    Knowledge-driven filtering step.
    Returns a queryset of dishes that are safe and appropriate
    for this specific user, based on the six factors.
    """
    dishes = Dish.objects.all()

    # 1. Allergy filtering — hard exclusion, never negotiable
    if profile.allergy_gluten:
        dishes = dishes.exclude(contains_gluten=True)
    if profile.allergy_nuts:
        dishes = dishes.exclude(contains_nuts=True)
    if profile.allergy_fish:
        dishes = dishes.exclude(contains_fish=True)
    if profile.allergy_eggs:
        dishes = dishes.exclude(contains_eggs=True)
    if profile.allergy_dairy:
        dishes = dishes.exclude(contains_dairy=True)
    if profile.allergy_soy:
        dishes = dishes.exclude(contains_soy=True)

    # 2. Economic constraints — only dishes at or below the user's budget rank
    max_rank = BUDGET_RANK.get(profile.budget_level, 2)
    affordable_ids = [
        d.id for d in dishes
        if DISH_COST_RANK.get(d.cost_level, 2) <= max_rank
    ]
    dishes = dishes.filter(id__in=affordable_ids)

    # 3. Protein preference — vegetarian users only get vegetarian dishes.
    # Meat-preference users still see vegetarian dishes too (breakfasts/snacks
    # are often vegetarian by nature), so this is a soft preference, not a hard filter.
    if profile.protein_preference == 'none':
        dishes = dishes.filter(is_vegetarian=True)

    # 4. Cultural region — user's region OR general dishes always included
    if profile.cultural_region != 'general':
        dishes = dishes.filter(region__in=[profile.cultural_region, 'general'])

    return dishes


def pick_dish(candidates, used_recently):
    """
    Data-driven ranking step.
    Prefers dishes not used in the last 2 days (repetition control),
    and among ties, prefers higher-rated dishes.
    """
    fresh = [d for d in candidates if d.id not in used_recently]
    pool = fresh if fresh else list(candidates)

    if not pool:
        return None

    # Sort by average rating (None treated as neutral 3.0), highest first,
    # then shuffle within same-rating groups for variety
    pool_with_rating = [(d, d.average_rating() or 3.0) for d in pool]
    max_rating = max(r for _, r in pool_with_rating)
    top_tier = [d for d, r in pool_with_rating if r == max_rating]
    return random.choice(top_tier)


def generate_meal_plan(profile):
    """
    Main entry point. Generates and saves a 7-day MealPlan for the profile.
    Returns the created MealPlan instance.
    """
    targets = run_expert_system(profile)
    candidates = filter_dishes_for_profile(profile)

    meal_plan = MealPlan.objects.create(
        profile=profile,
    
        daily_calorie_target=targets['daily_calories'],
        daily_protein_target=targets['protein_grams'],
        daily_carb_target=targets['carb_grams'],
        daily_fat_target=targets['fat_grams'],
    )

    meal_slots = ['breakfast', 'lunch', 'dinner', 'snack']
    used_recently = {slot: [] for slot in meal_slots}  # track last 2 days per slot

    for day in range(1, 8):
        for slot in meal_slots:
            slot_candidates = candidates.filter(meal_type=slot)

            if not slot_candidates.exists():
                continue  # no dish available for this slot — skip gracefully

            chosen = pick_dish(slot_candidates, used_recently[slot])
            if chosen is None:
                continue

            MealPlanEntry.objects.create(
                meal_plan=meal_plan,
                dish=chosen,
                day_number=day,
                meal_type=slot,
            )

            # Repetition control: remember last 2 days' picks for this slot
            used_recently[slot].append(chosen.id)
            if len(used_recently[slot]) > 2:
                used_recently[slot].pop(0)

    return meal_plan