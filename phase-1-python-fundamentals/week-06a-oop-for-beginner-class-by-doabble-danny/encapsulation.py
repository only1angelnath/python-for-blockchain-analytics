#Encapsulation is a fundamental concept in object-oriented programming (OOP) that restricts access to certain components of an object, such as its attributes and methods. 
# This is done to protect the internal state of the object and to prevent unintended interference from outside code. 
# In Python, encapsulation is typically achieved using private and protected attributes, as well as getter and setter methods.

#The bad example 

class BadBankAccount:
    def __init__(self, balance):
        self.balance = balance

account = BadBankAccount(0.0)
account.balance = -1 # Oh dear -- balance should not be allowed to be negative
print(account.balance)

# Why is this bad? The `balance` attribute can be set negative in the __init__ method and can be set directly. Setting a negative balance is not allowed in our banking app.


#The good example

class BankAccount:
    def __init__(self):
        self._balance = 0.0 # The underscore indicates that this attribute is intended to be protected and should not be accessed directly from outside the class.


    @property #creating a getter property for the balance attribute
    def balance(self):
        return self._balance

    def deposit(self, amount): #creating an instance method to deposit money into the bank account
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount


    def withdraw(self, amount): #creating an instance method to withdraw money from the bank account
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount

account = BankAccount()
print(account.balance)

account.deposit(1.99)
print(account.balance)

account.withdraw(1)
print(account.balance)

# account.withdraw(100) #this will raise a ValueError because the withdrawal amount is greater than the current balance
# print(account.balance)