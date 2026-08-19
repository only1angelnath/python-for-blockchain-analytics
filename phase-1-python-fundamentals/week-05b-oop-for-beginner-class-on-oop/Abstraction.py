#Abstraction is a fundamental concept in object-oriented programming (OOP) that allows us to hide the complex implementation details of a class and expose only the necessary functionalities to the user.
#It helps in reducing complexity and increasing efficiency by hiding unnessary details from the user. 
# In Python, abstraction can be achieved using abstract classes and methods.

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
