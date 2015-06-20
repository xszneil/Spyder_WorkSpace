'''
Created on 2014-7-15

@author: ZhuJiaqi
'''

class BankAccount:
    bank = "BOA"#class var is shared by instance, carefully change
    
    def __init__(self):
        self.balance = 0

    def withdraw(self, amount):
        self.balance -= amount
        return self.balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

def main():
    a = BankAccount()
    b = BankAccount()
    print a.deposit(100)
    print b.deposit(50)
    print b.withdraw(10)
    print a.withdraw(10)
    print a.bank
    print b.bank

if __name__ == "__main__":
    main()
