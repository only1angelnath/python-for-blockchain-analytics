#A static attribute is a variable that is shared among all instances of a class. 
# It is defined within the class but outside of any instance methods. 
# Static attributes are accessed using the class name rather than an instance of the class.

class User:
    user_count = 0 #this is a static attribute that keeps track of the number of instances of the User class created


    def __init__(self, username , email, password):
        self.username = username
        self.email = email
        self.password = password
        User.user_count += 1 #incrementing the static attribute user_count by 1 each time a new instance of the class is created

    def display_user(self):
        print(f"Username: {self.username}, Email: {self.email}")

user1= User("Luku", "Lukudbomber@gmail.com", "123456")
user2= User("Bengu", "drbengualairojinle@gmail.com", "34567")

print(User.user_count)
print(user1.user_count)
print(user2.user_count)

