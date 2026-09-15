#Static Method and Instance Method

#Static Method in python is a method that belongs to a class rather than an instance of the class. 
# It does not require an instance of the class to be called and does not have access to the instance (self) or class (cls) variables. 
# Static methods are defined using the `@staticmethod` decorator.
#protected method is used to indicate that a method is intended for internal use within the class or its subclasses.
#Private method is used to indicate that a method is intended for internal use within the class only

class BankAccount:
    MIN_BALANCE = 100 #this is a static attribute that defines the minimum balance required to open a bank account

    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance #we create a protected instance attribute to store the balance of the bank account

    def deposit(self, amount): #this is an instance attribute that allows the user to deposit money into their bank account
        if self._is_valid_amount(amount): #we call the protected method to check if the amount to be deposited is valid
            self._balance += amount
            self.__log_transaction("deposit", amount) #we call the private method to log the transaction details
        else:
            print("Deposit amount must be greater than 0.")

    def _is_valid_amount(self, amount): #this is a protected method that checks if the amount to be deposited is valid
        return amount > 0

    def __log_transaction(self, transaction_type, amount):
        print(f"Logging {transaction_type} of {amount} for {self.owner}.") #this is a private method that logs the transaction details

    @staticmethod #this is a static method 
    def is_valid_interest_rate(rate): #this is a static method that checks if the interest rate is valid
        return 0 <= rate <= 5 #the interest rate must be between 0 and 5


account = BankAccount("Mide", 500)
account.deposit(200)

account._is_valid_amount(100) #this is how we call a protected method from an instance of the class

# print(BankAccount.is_valid_interest_rate(3)) #this is how we call a static method without creating an instance of the class
# print(BankAccount.is_valid_interest_rate(10)) #this is how we call a static method without creating an instance of the class

