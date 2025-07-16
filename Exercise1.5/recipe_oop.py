class Recipe(object):
  all_ingredients = []
  def __init__(self, name, ingredients, cooking_time):
    self.name = name 
    self.ingredients = []
    self.add_ingredients(ingredients)
    self.cooking_time= cooking_time
    self.difficulty = None
    self.calculate_difficulty()

  def calculate_difficulty(self):
    if self.cooking_time < 10 and len(self.ingredients) < 4:
      return "easy"
    elif self.cooking_time < 10 and len(self.ingredients) >= 4:
      return "medium"
    elif self.cooking_time >= 10 and len(self.ingredients) < 4:
      return "intermediate"
    elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
      return "hard"
    else:
      return "error"

  def get_name(self):
    return self.name
    
  def set_name(self, name):
    self.name = name

  def get_cooking_time(self):
    return self.cooking_time
    
  def set_cooking_time(self, cooking_time):
    self.cooking_time = cooking_time

  def get_ingredients(self):
    return self.ingredients
  
  def update_all_ingredients(self):
    for ingredient in self.ingredients:
      if ingredient not in Recipe.all_ingredients:
        Recipe.all_ingredients.append(ingredient)
      
  def add_ingredients(self, ingredients_input):
    for i in ingredients_input:
      ingredient = i.strip()
      if ingredient not in self.ingredients:
        self.ingredients.append(ingredient)
    self.update_all_ingredients()

  def search_ingredient(self, ingredient):
    if ingredient in self.ingredients:
      return True
    else:
      return False

  def get_difficulty(self):
    if not self.difficulty:
      self.calculate_difficulty()
    return self.difficulty
  
  def __str__(self):
    output = "\nTasty " + str(self.name) + "\n\nCooking Time:" + str(self.cooking_time) + "minutes\nIngredients: \n"
    for ingredient in self.ingredients: output += str(ingredient) + "\n"
    return output
  
  def recipe_search(data, search_term):
    for recipe in data:
      if recipe.search_ingredient(search_term):
        print("\nFound! " + search_term + ": \n" + str(recipe))

tea = Recipe("Tea", ("Tea Leaves", "Sugar", "Water"), 5)
print(tea)
coffee = Recipe("Coffee", ("Coffee Powder", "Sugar", "Water"), 5)
print(coffee)
cake = Recipe("Cake", ("Butter", "Sugar", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"), 50)
print(cake)
banana_smoothie = Recipe("Banana Smoothie", ("Bananas", "Sugar", "Milk", "Peanut Butter", "Ice Cubes"), 5)
print(banana_smoothie)
recipes_list = [tea, coffee, cake, banana_smoothie]
Recipe.recipe_search(recipes_list, "Water")
Recipe.recipe_search(recipes_list, "Sugar")
Recipe.recipe_search(recipes_list, "Bananas")
print(Recipe.all_ingredients)