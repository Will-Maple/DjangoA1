from sqlalchemy import create_engine, Table, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer, String

# Creates a base for creating table objects, and an engine and session for  acce
Base = declarative_base()
engine = create_engine("mysql://cf-python:password@localhost/my_database")
Session = sessionmaker(bind=engine)
session = Session()

class UserQuit(Exception):
  pass

def get_input(prompt):
  user_input = input(prompt)
  if user_input.strip().lower() in ['q', 'quit', 'exit']:
    raise UserQuit()
  return user_input

# Defining an object class for recipes
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    
    def calculate_difficulty(self):
      ingredients_list = self.get_ingredient_list()
      if not ingredients_list:
        if self.cooking_time < 10:
          return "easy"
        elif self.cooking_time >= 10:
          return "intermediate"
        else:
          return "error"
      elif self.cooking_time < 10 and len(ingredients_list) < 4:
        return "easy"
      elif self.cooking_time < 10 and len(ingredients_list) >= 4:
        return "medium"
      elif self.cooking_time >= 10 and len(ingredients_list) < 4:
        return "intermediate"
      elif self.cooking_time >= 10 and len(ingredients_list) >= 4:
        return "hard"
      else:
        return "error"
      
    def get_difficulty(self):
      self.difficulty = self.calculate_difficulty()
      return self.difficulty
    
    def get_ingredient_list(self):
      ingredient_list = []
      for i in self.ingredients.split(", "):
        ingredient = i.strip()
        ingredient_list.append(ingredient)
      return ingredient_list

    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + "-" + self.difficulty + ">"
    def __str__(self):
      output = "\nTasty " + str(self.name) + "\nCooking Time: " + str(self.cooking_time) + " minutes\nDifficulty: " + str(self.difficulty) + "\nIngredients: \n"
      for ingredient in self.get_ingredient_list(): output += str(ingredient) + "\n"
      return output
    
# Creates the Recipe table in the MYSQL db
Base.metadata.create_all(engine)

def create_recipe():
  while True:
    try:
      while True:
        input_name = get_input("Name of Recipe: ")
        if not (3 <= len(input_name) <= 50):
          print("Name must be between 3 and 50 characters")
        else:
          break
      while True:
        input_cooking_time = get_input("Cooking time in minutes: ")
        if not input_cooking_time.isnumeric():
          print("Please input a number")
        else:
          input_cooking_time = int(input_cooking_time)
          break
      ingredients_list = []
      ingredients_str = ""
      while True:
        number_ingredients = get_input("How many ingredients would you like to enter?: ")
        if not number_ingredients.isnumeric() or int(number_ingredients) > 26:
          print("Please input a number less than 26")
        else:
          break
      for i in range(int(number_ingredients)):
        while True:
          input_ingredients = get_input("Enter an ingredient: ")
          if not input_ingredients.isalnum():
            print("Please only use alphanumerics")
          elif (len(ingredients_str) + len(input_ingredients)) > 253:
            characters_left = 253 - len(ingredients_str)
            print("Ingredient is too long, in ingredient list you have " + str(characters_left) + "characters left")
          else:
            ingredient = input_ingredients.strip()
            if ingredient not in ingredients_list:
              ingredients_list.append(ingredient)
              ingredients_str = ", ".join(ingredients_list)
          break

      recipe = Recipe(
        name = input_name,
        cooking_time = input_cooking_time,
        ingredients = ingredients_str
      )
      calculate_difficulty = recipe.calculate_difficulty()
      recipe.difficulty = calculate_difficulty
      session.add(recipe)
      break
    except UserQuit:
      raise
    except Exception as e:
      print(e)
      break

def search_recipe():
   recipes = all_recipes()
   if len(recipes) != 0:  
    display_recipes(recipes)
   else:
     print("No recipes in the database! Please create one or stop complaining!")
     return None
   all_ingredients = []
   for recipe in recipes:
      ingredient_list = recipe.get_ingredient_list()
      for ingredient in ingredient_list:
        ingredient = ingredient.strip()
        if ingredient not in all_ingredients:
          all_ingredients.append(ingredient)
   for index, i in enumerate(all_ingredients):
     print(f"{index}: {i}")
   while True:
     try:
      search_int = int(get_input("Number of ingredient to search: "))
      search_ingredient = all_ingredients[search_int]
      recipes = session.query(Recipe).filter(Recipe.ingredients.contains(search_ingredient)).all()
      return recipes
     except UserQuit:
      raise
     except Exception as e:
      print(e)
      break

def update_recipe():
   while True:
     try:
      recipes = all_recipes()
      if len(recipes) != 0:
        for result in recipes:
          results = (result.id, result.name)
          print(str(results[0]) + ": for recipe - " + results[1])
      else:
        print("No recipes in the database! Please create one or stop complaining!")
        return None
      choice1 = int(get_input("Select recipe by Id: "))
      recipe = session.query(Recipe).filter(Recipe.id == str(choice1)).one()
      print("1: Name: " + recipe.name)
      print("2: Cooking_time: " + str(recipe.cooking_time))
      print("3: Ingredients: " + recipe.ingredients)
      choice2 = int(get_input("Select column by number: "))
      if choice2 == 1:
        choice3 = get_input("Input new recipe name: ")
        if not (3<= len(choice3) <= 50):
          print("Name must be between 3 and 50 characters")
        else:
          recipe.name = choice3
        break  
      elif choice2 == 2:
        choice3 = get_input("Input new cooking time: ")
        if not choice3.isnumeric():
          print("Please input a number")
        else:
          choice3 = int(choice3)
          recipe.cooking_time = choice3
        break
      elif choice2 == 3:
        while True:
         recipe.ingredients = ""
         ingredients_list = []
         ingredients_str = ""
         print("Ingredients cleared, please add all ingredients")
         number_ingredients = get_input("How many ingredients would you like to enter?: ")
         if not number_ingredients.isnumeric() or int(number_ingredients) > 26:
           print("Please input a number less than 26")
         else:
           break
        for i in range(int(number_ingredients)):
         while True:
          choice3 = get_input("Input ingredient " + str(i + 1) + ": ")
          if not choice3.isalnum():
            print("Please only use alphanumerics")
          elif(len(ingredients_str) + len(choice3)) > 253:
            characters_left = 253 - len(ingredients_str)
            print("Ingredient is too long, in ingredient list you have " + str(characters_left) + "characters left")
          else:
            ingredient = choice3.strip()
            if ingredient not in ingredients_list:
              ingredients_list.append(ingredient)
              ingredients_str = ", ".join(ingredients_list)
            break
        recipe.ingredients = ingredients_str
        break
      else:
        print("Sorry that was not a correct input")
     except UserQuit:
      raise
     except Exception as e:
      print(e)
      break
     else:
       recipe.get_difficulty()
       break

def delete_recipe():
   while True:
    try:
      recipes = all_recipes()
      if len(recipes) != 0:
        for result in recipes:
          results = (result.id, result.name)
          print(str(results[0]) + ": for recipe - " + results[1])
      else:
        print("No recipes in the database! Please create one or stop complaining!")
        return None
      choice = int(get_input("Select recipe to delete by id: "))
      item_for_deletion = session.query(Recipe).filter(Recipe.id == str(choice)).one()
      while True:
        try:
          option = "0"
          confirmation = get_input("Would you like to delete " + item_for_deletion.name + "? Enter 'Yes' to confirm: ")
          if confirmation.lower() == "yes":
            session.delete(item_for_deletion)
            print("Item deleted")
            break
          else:
            print("Action canceled")
            option = get_input("Enter 1 for main menu, 2 to delete a recipe: ")
            if option == '1':
              break
            if option == '2':
              break
        except UserQuit:
          raise UserQuit()
        except:
          print("Something went wrong")
    except UserQuit:
      raise
    except Exception as e:
      print(e)
      break
    else:
      if option == '2':
        option = '0'
        print("-")
      else:
        return
     

def all_recipes():
   recipes = session.query(Recipe).all()
   return recipes
   

def display_recipes(recipes):
  for recipe in recipes:
    print(recipe)

def main_loop():
  while True:
    try:
      choice = "Initial Value"
      while(choice.strip().lower() not in ['quit', 'exit', 'q']):
        print('What would you like to do?')
        print('1. Create a new recipe?')
        print('2. Search for a recipe by ingredient?')
        print('3. Update an existing recipe?')
        print('4. Delete a recipe?')
        print('5. View all recipes?')
        print("Type 'quit' to exit the program.")
        choice = input("Your choice: ")
        if choice == '1':
          create_recipe()
          session.commit()
        elif choice == '2':
          recipes = search_recipe()
          if recipes == None:
            return
          else:
            display_recipes(recipes)
        elif choice == '3':
          update_recipe()
          session.commit()
        elif choice == '4':
          delete_recipe()
          session.commit()
        elif choice == '5':
          recipes = all_recipes()
          if recipes:
            display_recipes(recipes)
          else:
            print("No recipes in the database! Please create one or stop complaining!")
        elif choice == 'quit' or choice == 'Quit':
          break
        else:
          print('Whatcha trying to do? Input 1-5 or quit...')
      break
    except UserQuit:
      print("Returned to main menu: input 'quit' again to close program")
    except Exception as e:
      print(e)

main_loop()
session.close()
engine.dispose()