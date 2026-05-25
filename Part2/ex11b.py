# TODO:
# Create a function called calculate that takes three arguments:
# - A number
# - An operator ("+", "-", "*", or "/")
# - Another number
# The function should return the result of the calculation

num1 = float(input("Enter a number: "))
num2 = float(input("Enter another number: "))

def calculate(num1, operator, num2):
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "*":
        return num1 * num2
    elif operator == "/":
        return num1 / num2
    else:
        return "Invalid operator"
    
# Test the function with different operations
print(calculate(num1, "+", num2))  
print(calculate(num1, "-", num2))  
print(calculate(num1, "*", num2)) 
print(calculate(num1, "/", num2)) 