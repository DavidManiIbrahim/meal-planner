from django.core.management.base import BaseCommand
from nutrition.models import Ingredient, Dish, DishIngredient


class Command(BaseCommand):
    help = "Seeds the database with a starter Nigerian food dataset"

    def handle(self, *args, **kwargs):

        # ---------- INGREDIENTS ----------
        ingredients_data = [
            ("Rice", "moderate", 800, True, False, ""),
            ("Beans", "budget", 500, True, False, ""),
            ("Garri", "budget", 400, True, False, ""),
            ("Yam", "moderate", 700, True, True, "all year"),
            ("Palm oil", "moderate", 1000, True, False, ""),
            ("Groundnut oil", "moderate", 1200, True, False, ""),
            ("Egusi (melon seeds)", "moderate", 900, True, False, ""),
            ("Ugu (fluted pumpkin leaves)", "budget", 300, True, True, "rainy"),
            ("Bitter leaf", "budget", 300, True, True, "rainy"),
            ("Okro", "budget", 300, True, True, "rainy"),
            ("Chicken", "premium", 2500, True, False, ""),
            ("Fish (Titus/Mackerel)", "moderate", 1800, True, False, ""),
            ("Beef", "premium", 2200, True, False, ""),
            ("Turkey", "premium", 3000, True, False, ""),
            ("Onions", "budget", 200, True, False, ""),
            ("Tomatoes", "budget", 300, True, True, "all year"),
            ("Pepper (Tatashe/Scotch bonnet)", "budget", 300, True, False, ""),
            ("Crayfish", "moderate", 800, True, False, ""),
            ("Maize (corn)", "budget", 400, True, True, "harmattan"),
            ("Plantain", "budget", 400, True, True, "all year"),
            ("Eggs", "moderate", 900, True, False, ""),
            ("Bread", "budget", 700, True, False, ""),
            ("Akara beans mix", "budget", 500, True, False, ""),
            ("Ogbono seeds", "moderate", 1000, True, False, ""),
            ("Locust beans (iru)", "budget", 400, True, False, ""),
            ("Wheat flour", "moderate", 800, True, False, ""),
            ("Cassava flour (fufu)", "budget", 600, True, False, ""),
            ("Vegetable oil", "moderate", 1100, True, False, ""),
            ("Groundnut (peanuts)", "budget", 500, True, False, ""),
            ("Sweet potato", "budget", 500, True, True, "all year"),
        ]

        ingredient_objs = {}
        for name, cost_level, cost, nationwide, seasonal, season in ingredients_data:
            obj, _ = Ingredient.objects.get_or_create(
                name=name,
                defaults={
                    "cost_level": cost_level,
                    "approximate_cost_naira": cost,
                    "is_available_nationwide": nationwide,
                    "is_seasonal": seasonal,
                    "season": season,
                }
            )
            ingredient_objs[name] = obj

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(ingredient_objs)} ingredients"))

        # ---------- DISHES ----------
        # Each dish: (name, meal_type, region, cost_level, spice, calories, protein, carb, fat,
        #             is_veg, gluten, nuts, fish, eggs, dairy, soy, seasonal, season,
        #             [(ingredient_name, quantity), ...])
        dishes_data = [
            ("Jollof Rice with Chicken", "lunch", "general", "moderate", "medium",
             650, 35, 70, 20, False, False, False, False, False, False, False, False, "",
             [("Rice", "2 cups"), ("Chicken", "1 piece"), ("Tomatoes", "3 medium"),
              ("Onions", "1 medium"), ("Pepper (Tatashe/Scotch bonnet)", "2 pieces"),
              ("Vegetable oil", "3 tbsp")]),

            ("Egusi Soup with Pounded Yam", "dinner", "general", "moderate", "medium",
             700, 30, 45, 40, False, False, True, True, False, False, False, False, "",
             [("Egusi (melon seeds)", "1 cup"), ("Yam", "4 medium pieces"),
              ("Ugu (fluted pumpkin leaves)", "1 bunch"), ("Palm oil", "4 tbsp"),
              ("Fish (Titus/Mackerel)", "2 pieces"), ("Crayfish", "2 tbsp")]),
              ("Amala with Ewedu and Gbegiri", "dinner", "yoruba", "moderate", "mild",
             600, 25, 60, 25, False, False, False, True, False, False, False, False, "",
             [("Cassava flour (fufu)", "2 cups"), ("Beans", "1 cup"),
              ("Fish (Titus/Mackerel)", "1 piece"), ("Palm oil", "3 tbsp"),
              ("Locust beans (iru)", "1 tbsp")]),

            ("Ofe Onugbu (Bitterleaf Soup) with Fufu", "dinner", "igbo", "moderate", "medium",
             650, 28, 55, 30, False, False, False, True, False, False, False, False, "",
             [("Bitter leaf", "1 bunch"), ("Cassava flour (fufu)", "2 cups"),
              ("Beef", "3 pieces"), ("Crayfish", "2 tbsp"), ("Palm oil", "3 tbsp")]),

            ("Tuwo Shinkafa with Miyan Kuka", "dinner", "hausa", "moderate", "mild",
             620, 22, 65, 20, False, False, False, False, False, False, False, False, "",
             [("Rice", "2 cups"), ("Beef", "2 pieces"), ("Onions", "1 medium"),
              ("Groundnut oil", "2 tbsp")]),

            ("Beans and Plantain Porridge", "lunch", "general", "budget", "mild",
             550, 18, 75, 15, True, False, False, False, False, False, False, False, "",
             [("Beans", "2 cups"), ("Plantain", "2 medium"), ("Palm oil", "2 tbsp"),
              ("Onions", "1 medium"), ("Pepper (Tatashe/Scotch bonnet)", "1 piece")]),

            ("Akara with Pap", "breakfast", "general", "budget", "mild",
             400, 15, 45, 15, True, False, False, False, False, False, False, False, "",
             [("Akara beans mix", "1 cup"), ("Maize (corn)", "1 cup"),
              ("Vegetable oil", "3 tbsp"), ("Pepper (Tatashe/Scotch bonnet)", "1 piece")]),

            ("Bread and Egg with Tea", "breakfast", "general", "budget", "mild",
             450, 18, 50, 18, False, True, False, False, True, True, False, False, "",
             [("Bread", "4 slices"), ("Eggs", "2 pieces"), ("Onions", "1 small"),
              ("Vegetable oil", "1 tbsp")]),

            ("Yam and Egg Sauce", "breakfast", "general", "moderate", "mild",
             500, 20, 55, 18, False, False, False, False, True, False, False, False, "",
             [("Yam", "3 medium pieces"), ("Eggs", "3 pieces"), ("Tomatoes", "2 medium"),
              ("Onions", "1 medium"), ("Vegetable oil", "2 tbsp")]),

            ("Moi Moi", "breakfast", "general", "moderate", "mild",
             350, 20, 25, 18, False, False, False, True, True, False, False, False, "",
             [("Akara beans mix", "2 cups"), ("Fish (Titus/Mackerel)", "1 piece"),
              ("Eggs", "1 piece"), ("Vegetable oil", "2 tbsp"),
              ("Pepper (Tatashe/Scotch bonnet)", "1 piece")]),

            ("Fried Rice with Turkey", "lunch", "general", "premium", "mild",
             680, 32, 68, 22, False, False, False, False, False, False, False, False, "",
             [("Rice", "2 cups"), ("Turkey", "1 piece"), ("Onions", "1 medium"),
              ("Vegetable oil", "3 tbsp")]),

            ("Ogbono Soup with Semovita", "dinner", "general", "moderate", "medium",
             630, 27, 50, 32, False, True, False, True, False, False, False, False, "",
             [("Ogbono seeds", "1 cup"), ("Wheat flour", "2 cups"),
              ("Beef", "2 pieces"), ("Palm oil", "3 tbsp"), ("Crayfish", "1 tbsp")]),

            ("Okro Soup with Semovita", "dinner", "general", "moderate", "medium",
             600, 26, 48, 28, False, True, False, True, False, False, False, False, "",
             [("Okro", "1 cup"), ("Wheat flour", "2 cups"), ("Fish (Titus/Mackerel)", "2 pieces"),
              ("Palm oil", "3 tbsp"), ("Crayfish", "1 tbsp")]),

            ("Masa with Miyan Kuka", "breakfast", "hausa", "moderate", "mild",
             480, 15, 60, 15, True, False, False, False, False, False, False, False, "",
             [("Rice", "2 cups"), ("Maize (corn)", "1 cup"), ("Vegetable oil", "2 tbsp")]),
             ("Boiled Sweet Potato with Egg Sauce", "breakfast", "general", "budget", "mild",
             420, 16, 55, 14, False, False, False, False, True, False, False, False, "",
             [("Sweet potato", "3 medium pieces"), ("Eggs", "2 pieces"),
              ("Tomatoes", "2 medium"), ("Vegetable oil", "2 tbsp")]),

            ("Groundnut Snack Mix", "snack", "general", "budget", "mild",
             250, 10, 15, 18, True, False, True, False, False, False, False, False, "",
             [("Groundnut (peanuts)", "1 cup"), ("Maize (corn)", "1 cup")]),

            ("Roasted Plantain (Boli)", "snack", "general", "budget", "mild",
             220, 3, 50, 2, True, False, False, False, False, False, False, True, "all year",
             [("Plantain", "2 medium")]),

            ("Fresh Fruit Mix (Banana, Orange, Pawpaw)", "snack", "general", "budget", "mild",
             150, 2, 35, 1, True, False, False, False, False, False, False, True, "all year",
             []),

            ("Chicken Pepper Soup", "dinner", "general", "premium", "very_spicy",
             400, 35, 15, 18, False, False, False, False, False, False, False, False, "",
             [("Chicken", "1 piece"), ("Pepper (Tatashe/Scotch bonnet)", "2 pieces"),
              ("Onions", "1 medium")]),

            ("Beans Porridge with Fish", "lunch", "general", "budget", "medium",
             580, 24, 70, 16, False, False, False, True, False, False, False, False, "",
             [("Beans", "2 cups"), ("Fish (Titus/Mackerel)", "1 piece"),
              ("Palm oil", "2 tbsp"), ("Pepper (Tatashe/Scotch bonnet)", "1 piece")]),
              ("Ofada Rice with Ayamase Sauce", "lunch", "yoruba", "moderate", "very_spicy",
             680, 28, 65, 30, False, False, False, False, False, False, False, False, "",
             [("Rice", "2 cups"), ("Pepper (Tatashe/Scotch bonnet)", "4 pieces"),
              ("Palm oil", "4 tbsp"), ("Beef", "2 pieces"), ("Onions", "1 medium")]),

            ("Nkwobi", "dinner", "igbo", "premium", "very_spicy",
             520, 24, 15, 40, False, False, False, False, False, False, False, False, "",
             [("Beef", "3 pieces"), ("Palm oil", "3 tbsp"), ("Pepper (Tatashe/Scotch bonnet)", "2 pieces"),
              ("Onions", "1 medium")]),

            ("Suya Skewers", "dinner", "hausa", "moderate", "very_spicy",
             450, 38, 10, 28, False, False, True, False, False, False, False, False, "",
             [("Beef", "3 pieces"), ("Groundnut (peanuts)", "1 cup"), ("Pepper (Tatashe/Scotch bonnet)", "2 pieces"),
              ("Onions", "1 medium")]),

            ("Efo Riro with Rice", "dinner", "yoruba", "moderate", "medium",
             600, 26, 55, 28, False, False, False, True, False, False, False, False, "",
             [("Ugu (fluted pumpkin leaves)", "1 bunch"), ("Rice", "2 cups"), ("Fish (Titus/Mackerel)", "2 pieces"),
              ("Palm oil", "3 tbsp"), ("Crayfish", "1 tbsp")]),

            ("Oha Soup with Fufu", "dinner", "igbo", "moderate", "medium",
             630, 27, 50, 32, False, False, False, False, False, False, False, False, "",
             [("Bitter leaf", "1 bunch"), ("Cassava flour (fufu)", "2 cups"), ("Beef", "2 pieces"),
              ("Palm oil", "3 tbsp"), ("Crayfish", "1 tbsp")]),

            ("Dambu Nama with Tuwo", "lunch", "hausa", "moderate", "medium",
             580, 30, 60, 20, False, False, False, False, False, False, False, False, "",
             [("Beef", "3 pieces"), ("Rice", "2 cups"), ("Groundnut oil", "2 tbsp"),
              ("Onions", "1 medium")]),

            ("Vegetable Fried Rice", "lunch", "general", "moderate", "mild",
             560, 16, 70, 18, True, False, False, False, False, False, False, False, "",
             [("Rice", "2 cups"), ("Ugu (fluted pumpkin leaves)", "1 cup"), ("Onions", "1 medium"),
              ("Vegetable oil", "3 tbsp")]),

            ("Ewa Agoyin with Bread", "breakfast", "yoruba", "budget", "medium",
             480, 20, 55, 16, True, True, False, False, False, False, False, False, "",
             [("Beans", "2 cups"), ("Bread", "2 slices"), ("Palm oil", "3 tbsp"),
              ("Pepper (Tatashe/Scotch bonnet)", "2 pieces")]),

            ("Yam Porridge (Asaro)", "dinner", "general", "budget", "medium",
             550, 14, 75, 18, True, False, False, False, False, False, False, False, "",
             [("Yam", "4 medium pieces"), ("Palm oil", "3 tbsp"), ("Tomatoes", "2 medium"),
              ("Pepper (Tatashe/Scotch bonnet)", "1 piece"), ("Crayfish", "1 tbsp")]),

            ("Coconut Rice", "lunch", "general", "moderate", "mild",
             620, 14, 78, 22, True, False, False, False, False, False, False, False, "",
             [("Rice", "2 cups"), ("Palm oil", "2 tbsp"), ("Onions", "1 medium")]),

            ("Chin Chin", "snack", "general", "budget", "mild",
             300, 5, 40, 14, True, True, False, False, True, False, False, False, "",
             [("Wheat flour", "2 cups"), ("Vegetable oil", "3 tbsp"), ("Eggs", "1 piece")]),

            ("Puff Puff", "snack", "general", "budget", "mild",
             280, 5, 38, 12, True, True, False, False, False, False, False, False, "",
             [("Wheat flour", "2 cups"), ("Vegetable oil", "3 tbsp")]),

            ("Zobo Drink with Fruit Snack", "snack", "general", "budget", "mild",
             120, 1, 28, 0, True, False, False, False, False, False, False, True, "all year",
             []),
             ("Kilishi with Salad", "snack", "hausa", "premium", "very_spicy",
             350, 32, 8, 20, False, False, True, False, False, False, False, False, "",
             [("Beef", "2 pieces"), ("Groundnut (peanuts)", "1 cup"), ("Pepper (Tatashe/Scotch bonnet)", "1 piece")]),

            ("Akara and Custard", "breakfast", "general", "budget", "mild",
             420, 17, 48, 16, True, False, False, False, True, False, False, False, "",
             [("Akara beans mix", "1 cup"), ("Maize (corn)", "1 cup"), ("Vegetable oil", "2 tbsp"),
              ("Eggs", "1 piece")]),

            ("Custard with Bread", "breakfast", "general", "budget", "mild",
             380, 10, 55, 12, True, True, False, False, True, True, False, False, "",
             [("Maize (corn)", "1 cup"), ("Bread", "2 slices")]),

            ("Fisherman Soup", "dinner", "general", "premium", "medium",
             500, 34, 20, 24, False, False, False, True, False, False, False, False, "",
             [("Fish (Titus/Mackerel)", "2 pieces"), ("Crayfish", "2 tbsp"), ("Pepper (Tatashe/Scotch bonnet)", "2 pieces"),
              ("Onions", "1 medium"), ("Palm oil", "2 tbsp")]),

            ("Turkey Stew with Rice", "lunch", "general", "premium", "medium",
             700, 36, 68, 24, False, False, False, False, False, False, False, False, "",
             [("Turkey", "1 piece"), ("Rice", "2 cups"), ("Tomatoes", "3 medium"),
              ("Onions", "1 medium"), ("Vegetable oil", "3 tbsp")]),

            ("Vegetable Salad with Egg", "lunch", "general", "budget", "mild",
             350, 15, 25, 20, True, False, False, False, True, False, False, False, "",
             [("Eggs", "2 pieces"), ("Tomatoes", "2 medium"), ("Onions", "1 small"),
              ("Sweet potato", "1 medium")]),

            ("Ofada Beans (Gbegiri Beans)", "lunch", "yoruba", "budget", "medium",
             540, 22, 68, 16, True, False, False, False, False, False, False, False, "",
             [("Beans", "2 cups"), ("Palm oil", "2 tbsp"), ("Pepper (Tatashe/Scotch bonnet)", "1 piece")]),

            ("Miyan Taushe with Tuwo", "dinner", "hausa", "moderate", "mild",
             580, 20, 62, 22, True, False, False, False, False, False, False, False, "",
             [("Rice", "2 cups"), ("Sweet potato", "2 medium"), ("Groundnut (peanuts)", "1 cup"),
              ("Onions", "1 medium")]),
        ]

        created_count = 0
        for entry in dishes_data:
            (name, meal_type, region, cost_level, spice, calories, protein, carb, fat,
             is_veg, gluten, nuts, fish, eggs, dairy, soy, seasonal, season, dish_ingredients) = entry

            dish, created = Dish.objects.get_or_create(
                name=name,
                defaults={
                    "meal_type": meal_type,
                    "region": region,
                    "cost_level": cost_level,
                    "spice_level": spice,
                    "calories": calories,
                    "protein_grams": protein,
                    "carb_grams": carb,
                    "fat_grams": fat,
                    "is_vegetarian": is_veg,
                    "contains_gluten": gluten,
                    "contains_nuts": nuts,
                    "contains_fish": fish,
                    "contains_eggs": eggs,
                    "contains_dairy": dairy,
                    "contains_soy": soy,
                    "is_seasonal": seasonal,
                    "season": season,
                }
            )

            if created:
                created_count += 1
                for ing_name, quantity in dish_ingredients:
                    DishIngredient.objects.create(
                        dish=dish,
                        ingredient=ingredient_objs[ing_name],
                        quantity=quantity,
                    )

        self.stdout.write(self.style.SUCCESS(f"Seeded {created_count} new dishes"))
        self.stdout.write(self.style.SUCCESS("Food database seeding complete!"))