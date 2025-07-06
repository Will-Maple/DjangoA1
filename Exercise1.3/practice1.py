num1 = int(input("Enter a number: "))
num2 = int(input("Enter a 2nd number: "))
operator = input("Enter either + or -: ")

if operator == "+":
  print(num1 + num2)
elif operator == "-":
  print(num1 - num2)
else:
  print("Either + or - otherwise I ain't gonna do it")