# class Dog:
#     def __init__(self, name, breed, owner):
#         self.name = name
#         self.breed = breed
#         self.owner = owner

#     def bark(self):
#         print(f"{self.name} - a {self.breed} barks Woof Woof Agressively!")

# class Owner:
#     def __init__(self, name, address, contact_number):
#         self.name = name
#         self.address = address
#         self.phone_number = contact_number
        
# owner1= Owner("Danny", "122, Afoni Adegbayi", "814-822-92")
# dog1= Dog("Bruce", "Labrador", owner1)
# print(dog1.owner.name)
# dog1.bark()


# owner2= Owner("Mike", "395, Akobo", "853-857-67")
# dog2= Dog("Freya", "Greyhoound", owner2)
# print(dog2.owner.name)
# dog2.bark()



## Example

class Person:
    def __init__ (self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")


person1 = Person("Alice", 25)
person1.greet()

person2 = Person("Mide", 17)
person2.greet()