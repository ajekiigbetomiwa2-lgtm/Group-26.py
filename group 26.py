"""
Complete Recipe Nutrition Calculator with Built-in Database and Sample Recipes
"""

import os
from collections import defaultdict

# ==================== BUILT-IN DATABASES ====================
NUTRITION_DB = {
    "chicken breast": {
        "calories": 165, "protein": 31, "fat": 3.6, "carbs": 0,
        "vitamin_a": 20, "vitamin_b": 0.6, "vitamin_d": 0.1,
        "price_per_unit": 0.03
    },
    "brown rice": {
        "calories": 111, "protein": 2.6, "fat": 0.9, "carbs": 23,
        "vitamin_b": 0.1, "vitamin_e": 0.4, "price_per_unit": 0.02
    },
    "salmon": {
        "calories": 208, "protein": 20, "fat": 13, "carbs": 0,
        "vitamin_d": 11, "vitamin_b": 0.8, "price_per_unit": 0.05
    },
    "broccoli": {
        "calories": 34, "protein": 2.8, "fat": 0.4, "carbs": 6.6,
        "vitamin_a": 31, "vitamin_c": 89, "vitamin_k": 102,
        "price_per_unit": 0.01
    },
    "olive oil": {
        "calories": 884, "protein": 0, "fat": 100, "carbs": 0,
        "vitamin_e": 14, "vitamin_k": 60, "price_per_unit": 0.10
    },
    "egg": {
        "calories": 143, "protein": 13, "fat": 10, "carbs": 1.1,
        "vitamin_a": 160, "vitamin_d": 2, "vitamin_b": 0.9,
        "price_per_unit": 0.04
    },
    "whole wheat bread": {
        "calories": 247, "protein": 13, "fat": 3.4, "carbs": 41,
        "vitamin_b": 0.5, "price_per_unit": 0.03
    },
    "banana": {
        "calories": 89, "protein": 1.1, "fat": 0.3, "carbs": 23,
        "vitamin_c": 8.7, "vitamin_b": 0.4, "price_per_unit": 0.02
    },
    "milk": {
        "calories": 42, "protein": 3.4, "fat": 1, "carbs": 5,
        "vitamin_a": 14, "vitamin_d": 1.2, "vitamin_b": 0.4,
        "price_per_unit": 0.01
    },
    "potato": {
        "calories": 77, "protein": 2, "fat": 0.1, "carbs": 17,
        "vitamin_c": 19.7, "vitamin_b": 0.3, "price_per_unit": 0.01
    },
    "tomato": {
        "calories": 18, "protein": 0.9, "fat": 0.2, "carbs": 3.9,
        "vitamin_a": 42, "vitamin_c": 13.7, "price_per_unit": 0.02
    },
    "spinach": {
        "calories": 23, "protein": 2.9, "fat": 0.4, "carbs": 3.6,
        "vitamin_a": 188, "vitamin_c": 28, "vitamin_k": 483,
        "price_per_unit": 0.02
    },
    "ground beef": {
        "calories": 250, "protein": 26, "fat": 15, "carbs": 0,
        "vitamin_b": 0.8, "price_per_unit": 0.04
    },
    "cheese": {
        "calories": 402, "protein": 25, "fat": 33, "carbs": 1.3,
        "vitamin_a": 100, "vitamin_b": 0.4, "price_per_unit": 0.08
    },
    "apple": {
        "calories": 52, "protein": 0.3, "fat": 0.2, "carbs": 14,
        "vitamin_c": 4.6, "price_per_unit": 0.02
    }
}

DIETARY_REQUIREMENTS = {
    "child": {"calories": 1600, "protein": 34, "fat": 50, "carbs": 130},
    "teen": {"calories": 2200, "protein": 52, "fat": 65, "carbs": 180},
    "adult": {"calories": 2000, "protein": 50, "fat": 65, "carbs": 130},
    "senior": {"calories": 1800, "protein": 46, "fat": 60, "carbs": 130},
    "diabetic": {"calories": 1800, "protein": 50, "fat": 60, "carbs": 100},
    "athlete": {"calories": 2800, "protein": 140, "fat": 80, "carbs": 350}
}

VITAMINS = ["A", "B", "C", "D", "E", "K"]

# Built-in recipe files
BUILTIN_RECIPES = {
    "chicken_rice.txt": """Chicken with Rice
chicken breast: 200
brown rice: 150
olive oil: 10
broccoli: 100""",
    
    "salmon_salad.txt": """Salmon Salad
salmon: 150
spinach: 80
tomato: 100
olive oil: 15""",
    
    "breakfast.txt": """Healthy Breakfast
egg: 100
whole wheat bread: 60
milk: 200
apple: 100"""
}

# ==================== CORE CLASSES ====================
class NutritionDatabase:
    def __init__(self):
        self.db = NUTRITION_DB
            
    def get_nutrition(self, ingredient):
        return self.db.get(ingredient.lower())

class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients
        self.nutrition = self._calculate_nutrition()
        
    def _calculate_nutrition(self):
        nutrition_db = NutritionDatabase()
        total = defaultdict(float)
        
        for ingredient, amount in self.ingredients.items():
            data = nutrition_db.get_nutrition(ingredient)
            if not data:
                print(f"\nWarning: No nutrition data for '{ingredient}'")
                continue
                
            for nutrient, value in data.items():
                if nutrient == "price_per_unit":
                    continue
                total[nutrient] += value * amount / 100
                
        return dict(total)
        
    def get_cost(self):
        nutrition_db = NutritionDatabase()
        total = 0.0
        
        for ingredient, amount in self.ingredients.items():
            data = nutrition_db.get_nutrition(ingredient)
            if not data or "price_per_unit" not in data:
                continue
            total += data["price_per_unit"] * amount
            
        return round(total, 2)

class MealPlan:
    def __init__(self, name, recipes):
        self.name = name
        self.recipes = recipes
        self.nutrition = self._calculate_total_nutrition()
        
    def _calculate_total_nutrition(self):
        total = defaultdict(float)
        for recipe in self.recipes:
            for nutrient, value in recipe.nutrition.items():
                total[nutrient] += value
        return dict(total)
        
    def meets_requirements(self, dietary_type):
        requirements = DIETARY_REQUIREMENTS.get(dietary_type.lower())
        if not requirements:
            return False, "Invalid dietary type"
            
        for nutrient, required in requirements.items():
            if self.nutrition.get(nutrient, 0) < required * 0.9:
                return False, f"Insufficient {nutrient}"
                
        return True, "Meets requirements"

class RecipeManager:
    def __init__(self):
        self.recipe_dir = "recipes"
        self._setup_recipe_dir()
        
    def _setup_recipe_dir(self):
        if not os.path.exists(self.recipe_dir):
            os.makedirs(self.recipe_dir)
            self._create_builtin_recipes()
    
    def _create_builtin_recipes(self):
        for filename, content in BUILTIN_RECIPES.items():
            with open(os.path.join(self.recipe_dir, filename), "w") as f:
                f.write(content)
    
    def get_recipe_files(self):
        return [f for f in os.listdir(self.recipe_dir) if f.endswith('.txt')]
    
    def parse_recipe_file(self, filename):
        try:
            with open(os.path.join(self.recipe_dir, filename), "r") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                
            if not lines:
                print(f"\nError: Recipe file '{filename}' is empty.")
                return None
                
            name = lines[0]
            ingredients = {}
            
            for line in lines[1:]:
                if ":" not in line:
                    continue
                parts = line.split(":")
                if len(parts) != 2:
                    continue
                ingredient, amount = parts[0].strip(), parts[1].strip()
                try:
                    ingredients[ingredient] = float(amount)
                except ValueError:
                    print(f"\nWarning: Invalid amount '{amount}' for ingredient '{ingredient}'")
                    continue
                
            return Recipe(name, ingredients)
        except FileNotFoundError:
            print(f"\nError: Recipe file '{filename}' not found.")
            return None

# ==================== USER INTERFACE ====================
class MenuInterface:
    def __init__(self):
        self.meal_plans = {}
        self.nutrition_db = NutritionDatabase()
        self.recipe_manager = RecipeManager()
        
    def display_menu(self):
        while True:
            print("\n" + "=" * 40)
            print("Recipe Nutrition Calculator")
            print("=" * 40)
            print("1. Analyze a recipe")
            print("2. Create a meal plan")
            print("3. Generate shopping list")
            print("4. View dietary requirements")
            print("5. View built-in recipes")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == "1":
                self.analyze_recipe()
            elif choice == "2":
                self.create_meal_plan()
            elif choice == "3":
                self.generate_shopping_list()
            elif choice == "4":
                self.view_dietary_requirements()
            elif choice == "5":
                self.view_builtin_recipes()
            elif choice == "6":
                print("\nExiting program. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 6.")
    
    def analyze_recipe(self):
        print("\n" + "=" * 40)
        print("Recipe Analysis")
        print("=" * 40)
        
        recipes = self.recipe_manager.get_recipe_files()
        if not recipes:
            print("\nNo recipe files found.")
            return
            
        print("\nAvailable recipes:")
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe}")
            
        try:
            selection = int(input("\nEnter recipe number to analyze: "))
            if selection < 1 or selection > len(recipes):
                print("\nInvalid selection.")
                return
                
            recipe = self.recipe_manager.parse_recipe_file(recipes[selection-1])
            
            if recipe:
                self.display_recipe_nutrition(recipe)
        except ValueError:
            print("\nPlease enter a valid number.")
    
    def display_recipe_nutrition(self, recipe):
        print("\n" + "=" * 40)
        print(f"Nutrition Analysis: {recipe.name}")
        print("=" * 40)
        print(f"\nCalories: {recipe.nutrition.get('calories', 0):.1f} kcal")
        print(f"Protein: {recipe.nutrition.get('protein', 0):.1f} g")
        print(f"Fat: {recipe.nutrition.get('fat', 0):.1f} g")
        print(f"Carbohydrates: {recipe.nutrition.get('carbs', 0):.1f} g")
        
        print("\nVitamins:")
        for vitamin in VITAMINS:
            key = f"vitamin_{vitamin.lower()}"
            if key in recipe.nutrition:
                print(f"  Vitamin {vitamin}: {recipe.nutrition[key]:.1f} mcg")
        
        print(f"\nEstimated Cost: ${recipe.get_cost():.2f}")
    
    def create_meal_plan(self):
        print("\n" + "=" * 40)
        print("Create Meal Plan")
        print("=" * 40)
        
        recipes = self.recipe_manager.get_recipe_files()
        if not recipes:
            print("\nNo recipe files found.")
            return
            
        print("\nAvailable recipes:")
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe}")
            
        print("\nEnter the numbers of recipes to include (comma separated)")
        print("Example: 1,3,5")
        
        try:
            selections = input("Your selection: ").split(',')
            selected_indices = [int(s.strip()) for s in selections if s.strip().isdigit()]
            
            if not selected_indices:
                print("\nNo valid selections made.")
                return
                
            valid_selections = []
            for idx in selected_indices:
                if 1 <= idx <= len(recipes):
                    valid_selections.append(idx)
                else:
                    print(f"\nWarning: Ignoring invalid selection {idx}")
            
            if not valid_selections:
                print("\nNo valid recipes selected.")
                return
                
            plan_name = input("\nEnter a name for this meal plan: ").strip()
            if not plan_name:
                print("\nMeal plan name cannot be empty.")
                return
                
            recipe_objects = []
            for idx in valid_selections:
                recipe = self.recipe_manager.parse_recipe_file(recipes[idx-1])
                if recipe:
                    recipe_objects.append(recipe)
            
            if not recipe_objects:
                print("\nNo valid recipes could be loaded.")
                return
                
            meal_plan = MealPlan(plan_name, recipe_objects)
            self.meal_plans[plan_name] = meal_plan
            
            print(f"\nSuccessfully created meal plan: {plan_name}")
            print("\nTotal Nutrition:")
            print(f"Calories: {meal_plan.nutrition.get('calories', 0):.1f} kcal")
            print(f"Protein: {meal_plan.nutrition.get('protein', 0):.1f} g")
            print(f"Fat: {meal_plan.nutrition.get('fat', 0):.1f} g")
            print(f"Carbohydrates: {meal_plan.nutrition.get('carbs', 0):.1f} g")
            
            print("\nDietary Requirements Check:")
            for diet in DIETARY_REQUIREMENTS:
                meets, message = meal_plan.meets_requirements(diet)
                print(f"{diet.title()}: {'✓' if meets else '✗'} {message}")
                
        except ValueError:
            print("\nPlease enter valid numbers separated by commas.")
    
    def generate_shopping_list(self):
        print("\n" + "=" * 40)
        print("Generate Shopping List")
        print("=" * 40)
        
        if not self.meal_plans:
            print("\nNo meal plans have been created yet.")
            return
            
        print("\nAvailable Meal Plans:")
        for i, plan_name in enumerate(self.meal_plans.keys(), 1):
            print(f"{i}. {plan_name}")
            
        try:
            selection = int(input("\nEnter meal plan number: "))
            if selection < 1 or selection > len(self.meal_plans):
                print("\nInvalid selection.")
                return
                
            plan_name = list(self.meal_plans.keys())[selection-1]
            meal_plan = self.meal_plans[plan_name]
            
            print(f"\nShopping List for: {plan_name}")
            print("=" * 40)
            
            combined = defaultdict(float)
            for recipe in meal_plan.recipes:
                for ingredient, amount in recipe.ingredients.items():
                    combined[ingredient] += amount
            
            print("\nIngredient\t\tAmount (g)")
            print("-" * 30)
            for ingredient, amount in combined.items():
                print(f"{ingredient.ljust(20)}\t{amount:.1f}")
                
            total_cost = sum(recipe.get_cost() for recipe in meal_plan.recipes)
            print(f"\nEstimated Total Cost: ${total_cost:.2f}")
            
        except ValueError:
            print("\nPlease enter a valid number.")
    
    def view_dietary_requirements(self):
        print("\n" + "=" * 40)
        print("Dietary Requirements Reference")
        print("=" * 40)
        
        for diet, requirements in DIETARY_REQUIREMENTS.items():
            print(f"\n{diet.title()}:")
            for nutrient, amount in requirements.items():
                print(f"  {nutrient.title()}: {amount} {'g' if nutrient != 'calories' else 'kcal'}")
    
    def view_builtin_recipes(self):
        print("\n" + "=" * 40)
        print("Built-in Recipes")
        print("=" * 40)
        
        for filename, content in BUILTIN_RECIPES.items():
            print(f"\n{filename}:")
            print("-" * 30)
            print(content)

# ==================== MAIN PROGRAM ====================
def main():
    print("\nLoading Recipe Nutrition Calculator with built-in recipes...")
    menu = MenuInterface()
    menu.display_menu()

if __name__ == "__main__":
    main()