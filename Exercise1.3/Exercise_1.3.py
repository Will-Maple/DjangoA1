recipes_list = []
ingredients_list = []

def take_recipe(name="default name", cooking_time=0, ingredients=[]):
  recipe = {
      "name": name,
      "cooking_time": cooking_time,
      "ingredients": ingredients
  }
  return recipe

n = int(input("Enter the number of recipes: "))

for i in range(n):
    name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = input("Enter the ingredients (comma-separated): ")
    recipe_ingredients = []


    for i in ingredients.split(","):
        ingredient = i.strip()
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
            recipe_ingredients.append(ingredient)

    recipes_list.append(take_recipe(name, cooking_time, recipe_ingredients))

for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        difficulty = "easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        difficulty = "medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        difficulty = "medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        difficulty = "hard"
    else:
        difficulty = "error"
    print("Recipe: " + recipe["name"])
    print("Cooking time: " + str(recipe["cooking_time"]) + " minutes")
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty level: " + difficulty)

print("Ingredients Available Across All Recipes")
print("---------------------------")
for ingredient in ingredients_list.sort():
    print(ingredient)