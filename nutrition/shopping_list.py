"""
Shopping List Generator
Aggregates ingredients across all dishes in a MealPlan,
grouped by cost tier, with a total estimated cost.
"""

from collections import defaultdict
from nutrition.models import DishIngredient


def generate_shopping_list(meal_plan):
    dish_ids = meal_plan.entries.values_list('dish_id', flat=True).distinct()

    dish_ingredients = DishIngredient.objects.filter(
        dish_id__in=dish_ids
    ).select_related('ingredient', 'dish')

    grouped = defaultdict(list)
    total_cost = 0
    seen_costs = set()

    for di in dish_ingredients:
        ing = di.ingredient
        grouped[ing.cost_level].append({
            'ingredient': ing.name,
            'quantity': di.quantity,
            'for_dish': di.dish.name,
            'cost_naira': ing.approximate_cost_naira,
            'flagged': not ing.is_available_nationwide,
        })
        if ing.id not in seen_costs:
            total_cost += ing.approximate_cost_naira
            seen_costs.add(ing.id)

    return {
        'grouped': dict(grouped),
        'total_estimated_cost': total_cost,
    }