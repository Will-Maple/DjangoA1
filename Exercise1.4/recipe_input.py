import pickle

def take_recipe():
  name = input("Name of Recipe: ")
  cooking_time = int(input("Cooking time in minutes: "))
  ingredients_input = input("Enter the ingredients (comma-seperated): ")
  ingredients = []

  for i in ingredients_input.split(","):
    ingredient = i.strip()
    if ingredient not in ingredients:
      ingredients.append(ingredient)

  if cooking_time < 10 and len(ingredients) < 4:
      difficulty = "easy"
  elif cooking_time < 10 and len(ingredients) >= 4:
      difficulty = "medium"
  elif cooking_time >= 10 and len(ingredients) < 4:
      difficulty = "medium"
  elif cooking_time >= 10 and len(ingredients) >= 4:
      difficulty = "hard"
  else:
      difficulty = "error"

  recipe = {"name": name, "time": cooking_time, "ingredients": ingredients, "difficulty": difficulty}
  return recipe

data_location = input("Name of file with recipe data: ")

def fetch_recipes():
   try:
      with open(data_location, 'rb') as location:
         data = pickle.load(location)
   except FileNotFoundError:
      data = {"recipes_list": [], "all_ingredients": []}
      print("File not found")
      print("Creating empty data set...")
   except:
      data = {"recipes_list": [], "all_ingredients": []}
      print("Unexpected Error")
      print("Creating empty data set...")
   else:
      print("Data found!")
   finally:
      recipes_list = data["recipes_list"]
      all_ingredients = data["all_ingredients"]
      return recipes_list, all_ingredients

recipes_list, all_ingredients = fetch_recipes()
n = int(input("How many recipes would you like to enter?: "))
for i in range(n):
   recipe_iteration = take_recipe()
   recipes_list.append(recipe_iteration)
   for ingredient in recipe_iteration["ingredients"]:
       if ingredient not in all_ingredients:
        all_ingredients.append(ingredient)

data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}
with open(data_location, "wb") as file:
   pickle.dump(data, file)
