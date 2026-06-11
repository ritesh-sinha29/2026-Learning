# ==========================================
# PYTHON CLASSES & OOP (FOR BEGINNERS)
# ==========================================

# --- WHAT IS A CLASS? ---
# A class is like a BLUEPRINT or TEMPLATE for creating objects.
# Example: A "Car" blueprint defines: color, brand, speed.
#          From that blueprint, you can create many actual cars.

# --- REAL-WORLD USE CASES ---
# * FastAPI + Pydantic: You define a `class User` as a model,
#   and FastAPI uses it to validate request and response data.
# * LangGraph: State objects that hold data as an agent runs are classes.
# * Everywhere: Grouping related data and behavior together.

print("==========================================")
print("1. CREATING A SIMPLE CLASS")
print("==========================================")

# `class` keyword creates a new class
# `__init__` is a special method called automatically when you create an object
# `self` refers to the specific object being created (like "this" in other languages)

class Dog:
    # __init__ runs automatically when you create a Dog
    def __init__(self, name, breed):
        # Store the values on `self` so we can use them later
        self.name = name
        self.breed = breed

    # This is a method (a function inside a class)
    def bark(self):
        print(f"{self.name} says: Woof!")

# Creating OBJECTS (instances) from the Dog blueprint:
dog1 = Dog("Bruno", "Labrador")
dog2 = Dog("Max", "Pug")

print("Dog 1 name:", dog1.name)
print("Dog 2 breed:", dog2.breed)
dog1.bark()
dog2.bark()

print()

# ==========================================
print("2. CLASS WITH MULTIPLE METHODS")
print("==========================================")

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance   # starting balance

    def deposit(self, amount):
        self.balance = self.balance + amount
        print(f"Deposited ₹{amount}. New balance: ₹{self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Not enough money!")
        else:
            self.balance = self.balance - amount
            print(f"Withdrew ₹{amount}. New balance: ₹{self.balance}")

    def show_balance(self):
        print(f"Account owner: {self.owner} | Balance: ₹{self.balance}")

account = BankAccount("Ritesh", 5000)
account.show_balance()
account.deposit(2000)
account.withdraw(1000)
account.withdraw(10000)  # Should show "Not enough money!"

print()

# ==========================================
print("3. INHERITANCE — One class inherits from another")
print("==========================================")

# Inheritance means a NEW class gets all the features of an EXISTING class.
# Then you can add more features on top.

class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating.")

# Cat INHERITS from Animal — it gets `name` and `eat()` for free!
class Cat(Animal):
    def meow(self):
        print(f"{self.name} says: Meow!")

my_cat = Cat("Whiskers")
my_cat.eat()    # Inherited from Animal
my_cat.meow()  # Defined in Cat

print()

# ==========================================
print("4. FASTAPI USE CASE — Pydantic Model (class)")
print("==========================================")

# In FastAPI, you define what data your API expects using a class.
# This is called a Pydantic model. It looks exactly like a normal class.

# (In real FastAPI: from pydantic import BaseModel)
# Here we simulate it without installing FastAPI:

class UserRequest:
    # This class represents the data a user sends when registering
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email

    def to_dict(self):
        # FastAPI converts this to a JSON response automatically
        return {"name": self.name, "age": self.age, "email": self.email}

new_user = UserRequest("Ritesh", 20, "ritesh@example.com")
print("New user data:", new_user.to_dict())
