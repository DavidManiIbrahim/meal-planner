from django.contrib import admin
from .models import Ingredient, Dish, DishIngredient, MealPlan, MealPlanEntry, Rating

admin.site.register(Ingredient)
admin.site.register(Dish)
admin.site.register(DishIngredient)
admin.site.register(MealPlan)
admin.site.register(MealPlanEntry)
admin.site.register(Rating)
# Register your models here.
