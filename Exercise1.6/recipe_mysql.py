import mysql.connector

conn = mysql.connector.connect( host='localhost', user='cf-python', passwd='password')

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
   item_id INT PRIMARY KEY AUTO_INCREMENT,
   item_name VARCHAR(50),
   ingredients VARCHAR(255),
   cooking_time INT,
   difficulty VARCHAR(20))''')

def calculate_difficulty(ct, ing):
  if ct < 10 and len(ing) < 4:
      difficulty = "easy"
  elif ct < 10 and len(ing) >= 4:
      difficulty = "medium"
  elif ct >= 10 and len(ing) < 4:
      difficulty = "medium"
  elif ct >= 10 and len(ing) >= 4:
      difficulty = "hard"
  else:
      difficulty = "error"
  return difficulty

def display_recipes(conn, cursor):
   cursor.execute("SELECT item_id, item_name, ingredients, cooking_time, difficulty FROM Recipes")
   results = cursor.fetchall()
   for recipe in results:
     print("Id: ", recipe[0])
     print("Name: ", recipe[1])
     print("Ingredients: ", recipe[2])
     print("Cooking_time: ", recipe[3])
     print("Difficulty: ", recipe[4])
     print()

def create_recipe(conn, cursor):
  name = input("Name of Recipe: ")
  cooking_time = int(input("Cooking time in minutes: "))
  ingredients_input = input("Enter the ingredients (comma-seperated): ")
  ingredients = []

  for i in ingredients_input.split(","):
    ingredient = i.strip()
    if ingredient not in ingredients:
      ingredients.append(ingredient)

  difficulty = calculate_difficulty(cooking_time, ingredients)

  ingredients_str = ", ".join(ingredients)
  recipe = {"name": name, "time": cooking_time, "ingredients": ingredients_str, "difficulty": difficulty}
  return recipe

def search_recipe(conn, cursor):
   cursor.execute("SELECT ingredients FROM Recipes")
   results = cursor.fetchall()
   all_ingredients = []
   for tuple in results:
      ingredient_str = tuple[0]
      ingredient_list = ingredient_str.split(",")
      for ingredient in ingredient_list:
        ingredient = ingredient.strip()
        if ingredient not in all_ingredients:
          all_ingredients.append(ingredient)
   for index, i in enumerate(all_ingredients):
     print(f"{index}: {i}")
   search_int = int(input("Number of ingredient to search: "))
   search_ingredient = all_ingredients[search_int]
   search_term = f"%{search_ingredient}%"
   sql = ("SELECT item_name, ingredients, cooking_time, difficulty FROM Recipes WHERE ingredients LIKE %s")
   cursor.execute(sql, (search_term,))
   recipes = cursor.fetchall()
   return recipes


def update_recipe(conn, cursor):
   display_recipes(conn, cursor)
   choice1 = int(input("Select recipe by Id: "))
   print("1: Name")
   print("2: Ingredients")
   print("3: Cooking_time")
   choice2 = int(input("Select column by number: "))
   if choice2 == 1:
      choice3 = input("Input new recipe name: ")
      sql = "UPDATE Recipes SET item_name = %s WHERE item_id = %s"
      value = (choice3, choice1)
      cursor.execute(sql, value)
   elif choice2 == 2:
      choice3 = input("Input ingredients seperated by a comma: ")
      sql = "UPDATE Recipes SET ingredients = %s WHERE item_id = %s"
      value = (choice3, choice1)
      cursor.execute(sql, value)
   elif choice2 == 3:
      choice3 = int(input("Input new cooking time: "))
      sql = "UPDATE Recipes SET cooking_time = %s WHERE item_id = %s"
      value = (choice3, choice1)
      cursor.execute(sql, value)
   else:
      print("Sorry that was not a correct input")


def delete_recipe(conn, cursor):
   display_recipes(conn, cursor)
   choice = int(input("Select recipe to delete by id: "))
   sql = "DELETE FROM Recipes WHERE item_id = %s"
   value = (choice,)
   cursor.execute(sql, value)

choice = "Initial Value"
while(choice != 'quit'):
  print('What would you like to do?')
  print('1. Create a new recipe?')
  print('2. Search for a recipe by ingredient?')
  print('3. Update an existing recipe?')
  print('4. Delete a recipe?')
  print("Type 'quit' to exit the program.")
  choice = input("Your choice: ")

  if choice == '1':
    recipe = create_recipe(conn, cursor)
    sql = ('''INSERT INTO Recipes(item_name, ingredients, cooking_time, difficulty)
      VALUES (%s, %s, %s, %s)''')
    values = (recipe["name"], recipe["ingredients"], recipe["time"], recipe["difficulty"])
    cursor.execute(sql, values)
    conn.commit()
  elif choice == '2':
    recipes = search_recipe(conn, cursor)
    for recipe in recipes:
       print("Name: ", recipe[0])
       print("Ingredients: ", recipe[1])
       print("Cooking_time: ", recipe[2])
       print("Difficulty: ", recipe[3])
       print()
  elif choice == '3':
    update_recipe(conn, cursor)
    conn.commit()
  elif choice == '4':
    delete_recipe(conn, cursor)
    conn.commit()

conn.close()