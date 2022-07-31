from datahandler.datahandler import DataHandler
from models.account.account import Account, A


datahandler = DataHandler("../test_data")
a = A(1)
account = Account("user", "test", "test", a)
datahandler.add_account(account)
accounts = datahandler.get_accounts()
print(accounts)
print(accounts[0])
print(accounts[0].a)
print(accounts[0].a.id)
print(accounts[0].username)
print(accounts[0].password)
print(accounts[0].account_type)

print(accounts[3])