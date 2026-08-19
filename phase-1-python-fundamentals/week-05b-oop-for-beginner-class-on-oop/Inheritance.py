#Inheritance is a fundamental concept in object-oriented programming (OOP) 
# that allows a class (called a child or subclass) to inherit attributes and methods from another class (called a parent or superclass). 
# This promotes code reusability and establishes a hierarchical relationship between classes.

# For example a Car is a vehicle and a bike is a vehicle. 
# So we can create a Vehicle class and then create Car and Bike classes that inherit from the Vehicle class.

class Vehicle:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def start_engine(self):
        print(f"{self.brand} {self.model} {self.year}'s engine is starting...")

    def stop_engine(self):
        print(f"{self.brand} {self.model} {self.year}'s engine is stopping...")

class Car(Vehicle):  #we tell class car to inherit from the vehicle class by passing the Vehicle class as an argument to the Car class
    def __init__(self, brand, model, year, num_doors, num_wheels): #we add the num_doors and num_wheels attributes to the Car class
        super().__init__(brand, model, year) #we use the super() function to call the __init__ method of the parent class (Vehicle) and initialize the brand, model, and year attributes.
        self.num_doors = num_doors
        self.num_wheels = num_wheels

class Bike(Vehicle): #we tell class bike to inherit from the vehicle class by passing the Vehicle class as an argument to the Bike class
    def __init__(self, brand, model, year, num_wheels):
        super().__init__(brand, model, year) #we use the super() function to call the __init__ method of the parent class (Vehicle) and initialize the brand, model, and year attributes.
        self.num_wheels = num_wheels

car = Car("Toyota", "Camry", 2020, 4, 4)
bike = Bike("TVS", "Apache-EV", 2025, 2)
print(car.__dict__) #print the car attributes as a dict
print(bike.__dict__) #print the bike attributes as a dict