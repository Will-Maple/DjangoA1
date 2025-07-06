num = int(input("Enter a number to be divided: "))
start = int(input("Enter a number to start the division from: "))
end = int(input("Enter the end point for the division: "))

for div in range (start, end):
  if div == 0:
    print ("Cannot divide by zero")
    break
  print(num / div)