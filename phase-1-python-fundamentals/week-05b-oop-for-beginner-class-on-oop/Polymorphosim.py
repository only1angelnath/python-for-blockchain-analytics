"""
Polymorphism 
Polymorphism is a greek word that means "many forms." 
In programming, polymorphism allows methods to do different things based on the object it is acting upon. 
It allows for flexibility and the ability to define methods in a way that can work with different data types or classes.
It enables a single interface to be used for different underlying data types.
"""

"""""
# Example with no polymorphism

class Car:
    def __init__(self, brand, model, year, number_of_doors):
        self.brand = brand
        self.model = model
        self.year = year
        self.number_of_doors = number_of_doors

    def start(self):
        print("Car is starting.")

    def stop(self):
        print("Car is stopping.")

class Motorcycle:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def start_bike(self):
        print("Motorcycle is starting.")

    def stop_bike(self):
        print("Motorcycle is stopping.")

# creating a list of vehicle that we can loop through
vehicles = [
    Car("Toyota", "Corrolla", 2020, 4),
    Motorcycle("Spiro", "Agenda2", 2025),
    Car("Ford", "Focus", 2020, 4),
    Motorcycle("Honda", "Scoopy", 2025),
]

#loop through the list of vehicles and ispect each vehicle
for vehicle in vehicles:
    if isinstance(vehicle, Car):
        print(f"Inspecting {vehicle.brand} {vehicle.model} ({type(vehicle).__name__})")
        vehicle.start()
        vehicle.stop()
    elif isinstance(vehicle, Motorcycle):
        print(f"Inspecting {vehicle.brand} {vehicle.model} ({type(vehicle).__name__})")
        vehicle.start_bike()
        vehicle.stop_bike()
    else:
        raise Exception("Object is not a valid vehicle")
"""""
    

## Good example with polymorphism

class Vehicle:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def start(self):
        print(f"{self.brand} {self.model} {self.year} ({type(self).__name__})'s engine is starting...")

    def stop(self):
        print(f"{self.brand} {self.model} {self.year} ({type(self).__name__})'s engine is stopping...")

class Car(Vehicle):
    def __init__(self, brand, model, year, num_doors):
        super().__init__(brand, model, year) #we use the super() function to call the __init__ method of the parent class (Vehicle) and initialize the brand, model, and year attributes.
        self.num_doors = num_doors

class Motorcycle(Vehicle):
    def __init__(self, brand, model, year):
        super().__init__(brand, model, year) #we use the super() function to call the __init__ method of the parent class (Vehicle) and initialize the brand, model, and year attributes.

class Plane(Vehicle):
    def __init__(self, brand, model, year):
        super().__init__(brand, model, year) #we use the super() function to call the __init__ method of the parent class (Vehicle) and initialize the brand, model, and year attributes.

#creating a list of vehicle that we can loop through
vehicles: list[Vehicle] = [
    Car("Toyota", "Corrolla", 2020, 4),
    Motorcycle("Spiro", "Agenda2", 2025),
    Plane("Boeing", "737", 2020),
    Car("Ford", "Focus", 2020, 4),
    Motorcycle("Honda", "Scoopy", 2025),
    Plane("Airbus", "A380", 2020),
]

#loop through the list of vehicles and ispect each vehicle
for vehicle in vehicles:
    print(f"Inspecting {vehicle.brand} {vehicle.model} ({type(vehicle).__name__})")
    vehicle.start()
    vehicle.stop()

    # if isinstance(vehicle, Vehicle):
    #     print(f"Inspecting {vehicle.brand} {vehicle.model} ({type(vehicle).__name__})")
    #     vehicle.start()
    #     vehicle.stop()
    # else:
    #     raise Exception("Object is not a valid vehicle")

