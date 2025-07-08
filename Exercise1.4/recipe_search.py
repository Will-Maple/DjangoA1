import pickle

def display_recipe(recipe = {"name": "error", "time": "n/a", "ingredients": "n/a", "difficulty": "n/a"}):
  print("\n")
  print("Recipe Name: " + recipe["name"])
  print("Cooking time: " + str(recipe["time"]) + "minutes")
  print("Ingredients:") 
  for ingredient in recipe["ingredients"]:
    print(ingredient)
  print("Difficulty: " + recipe["difficulty"])

def search_ingredients(data = {"all_ingredients": ["empty!", ]}, ):
  data_enumerate = enumerate(data["all_ingredients"])
  for tuple in data_enumerate:
    print("Ingredient " + str(tuple[0]) + ": " + str(tuple[1]))
  
  try:
    n = int(input("Enter the number of the ingredient you want to use: "))
    ingredient_searched = data["all_ingredients"][n]
  except:
    print("Error: Please enter a number between 0 and " + len(data_enumerate) - 1)
  else:
    recipes_search = []
    for recipe in data["recipes_list"]:
      if ingredient_searched in recipe["ingredients"]:
        recipes_search.append(recipe)
    return recipes_search

data_location = input("Name of file with recipe data: ")

def fetch_recipes():
   try:
      with open(data_location, 'rb') as location:
         data = pickle.load(location)
   except FileNotFoundError:
      print("File not found")
      print("Starting over...")
      fetch_recipes()
   except:
      print("Unexpected Error")
      print("Starting over...")
      fetch_recipes()
   else:
      print("Data found!")
      recipes = search_ingredients(data)
      for recipe in recipes:
        display_recipe(recipe)
      return(data)
   
fetch_recipes()