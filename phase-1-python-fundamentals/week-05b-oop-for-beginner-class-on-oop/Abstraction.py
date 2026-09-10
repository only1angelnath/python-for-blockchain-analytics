#Abstraction is a fundamental concept in object-oriented programming (OOP) that allows us to hide the complex implementation details of a class and expose only the necessary functionalities to the user.
#It helps in reducing complexity and increasing efficiency by hiding unnessary details from the user. 
# In Python, abstraction can be achieved using abstract classes and methods.

#bad example
class BadEmailService:
    # def send_email(self):
    #     self.connect()
    #     self.authenticate()
    #     print("Sending email...")
    #     self.disconnect()

    def connect(self):
        print("Connecting to email server...")

    def authenticate(self):
        print("Authenticating...")

    # We could also force clients to call connect, authenticate, send_email, and disconnect to send an email. That wouldn't be very nice tho! No abstraction means more effort for client/dev.
    def send_email(self):
        print("Sending email...")

    def disconnect(self):
        print("Disconnecting from email server...")

email = BadEmailService()

email.connect()
email.authenticate()
email.send_email()
email.disconnect()

# LOGS:
# Connecting to email server...
# Authenticating...
# Sending email...
# Disconnecting from email server...

# Oh no, I don't have such a simple API to just send an email (this thing I actually want to do). Much easier to make mistakes -- I might forget to disconnect after sending.
# What happens if implementation details change? Client code has to change.

#good example
class EmailService:
    def _connect(self):   #this is a protetcted method
        print("Connecting to email server...")

    def _authenticate(self):
        print("Authenticating user...")

    def send_email(self): #this is a public method
        self._connect()
        self._authenticate()
        print("Sending email...")
        self._disconnect()

    def _disconnect(self):
        print("Disconnecting from email server...")

email = EmailService()
email.send_email()


## Encapsulation and Abstraction are two fundamental concepts in object-oriented programming (OOP) that help in organizing and structuring code. 
# While they are related, they serve different purposes.

# Encapsulation is a fundamental concept in object-oriented programming (OOP) that restricts access to certain components of an object, such as its attributes and methods. 
# This is done to protect the internal state of the object and to prevent unintended interference from outside code. 
# In Python, encapsulation is typically achieved using private and protected attributes, as well as getter and setter methods.

# Abstraction, on the other hand, is a fundamental concept in object-oriented programming (OOP) that allows us to hide the complex implementation details of a class and expose only the necessary functionalities to the user.
# It helps in reducing complexity and increasing efficiency by hiding unnessary details from the user. 
# In Python, abstraction can be achieved using abstract classes and methods.