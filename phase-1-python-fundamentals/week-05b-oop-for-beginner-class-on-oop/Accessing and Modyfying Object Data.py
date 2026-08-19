# class User:
#     def __init__(self, username , email, password):
#         self.username = username
#         self.email = email
#         self.password = password

#     def say_hi_to_user(self, user):
#         print(f"Sending message to {user.username}: Hi {user.username}, How are you doing today?. Its {self.username}")

# user1= User("Mide", "mide@gmail.com", "123456")
# user2= User("Badmus", "badthemus@gmail.com", "A2#dtk")

# print(user1.email)

# user1.email = "midethegreat@hotmail.com"
# print(user1.email)

##There are two main ways to access and modify object data in Python. These two approaches are:

# 1. The traditional "Java"-style, and 2. the more modern "Python" (and C#) style.

# 1. **The traditional way: make the data private and use getters and setters:**

# from datetime import datetime
# class User:
#     def __init__(self, username , email, password):
#         self.username = username
#         self._email = email #the underscore is used to make the attribute private/protected
#         self.password = password

#     def get_email(self):
#         print(f"Email accessed at {datetime.now()}")
#         return self._email

#     def set_email(self, new_email): #we create a setter method to modify the private attribute
#         if "@" in new_email:
#             self._email = new_email
#             print(f"Email modified at {datetime.now()}")
#         else:
#             print("Invalid email")

# user1= User("Mide", "MidE@gmail.com", "123456")
# print(user1.get_email())


# user1.set_email("midethegreathotmail.com")
# print(user1.get_email())


# 2. **The more modern way: make the data public and use property decorators:**

from datetime import datetime
class User:
    def __init__(self, username , email, password):
        self.username = username
        self._email = email
        self.password = password

    @property #using a prpoerty decorator to create a getter method for the email attribute
    def email(self):
        print(f"Email accessed at {datetime.now()}")
        return self._email

    @email.setter #using a property decorator to create a setter method for the email attribute
    def email(self, new_email):
        if "@" in new_email:
            self._email = new_email
            print(f"Email modified at {datetime.now()}")
        else:
            print("Invalid email")


user1= User("Luku", "Lukudbomber@gmail.com", "123456")
user1.email = "this is not an email"
print(user1.email)