import pickle

recipe = {
  "Ingredient Name": "Tea",
  "Ingredients": ["Tea leaves", "Water", "Sugar"],
  "Cooking Time": 5,
  "Difficulty": "Easy"
}

my_file = open('recipe_binary.bin', 'wb')
pickle.dump(recipe, my_file)
my_file.close()

with open('recipe_binary.bin', 'rb') as my_file:
    recipe = pickle.load(my_file)

    print("Your Recipe - ")
    print("Name:  " + recipe['Ingredient Name'])
    print("Ingredients:  " + ', '.join(recipe['Ingredients']) + " and " + str(recipe['Cooking Time']) +" minutes")
    print("Difficulty: " + recipe['Difficulty'])