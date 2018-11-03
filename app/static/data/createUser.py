from nessie import createBill, createPurchase, createDeposit, requestPurchasesByAccountID, requestDepositsByAccountID, ACCOUNT_ID
from functools import reduce

def createUser():
    # Create Bill: account_id, status, payee, nickname, payment_date, recurring_date
    # Create Deposit: account_id, medium, date, status, description
    # Create Purchases: account_id, merchant_id, medium, purchase_date, amount, status, description

    status = "completed"

    # Weekly Transactions
    weekDates = ["2017-12-11", "2017-12-18", "2017-12-25", "2018-01-01", "2018-01-08"]
    for date in weekDates:
        createPurchase(ACCOUNT_ID, "57cf75cfa73e494d8675fa32", "balance", date, 30, status, "Sheetz") # Tranport
        # createPurchase(ACCOUNT_ID, "Uber", "balance", date, 7, status, "Transportation") # Transport
        createPurchase(ACCOUNT_ID, "57cf75cfa73e494d8675f9fb", "balance", date, 20, status, "CVS Pharmacy") # Food
        createPurchase(ACCOUNT_ID, "57cf75cfa73e494d8675fa28", "balance", "2018-01-08", 7, status, "Subway") # Food
        createPurchase(ACCOUNT_ID, "57cf75cfa73e494d8675f863", "balance", "2018-01-08", 60, status, "Whole Foods") # Utilites

    # Bi-Weekly Transaction
    biWeekDates = ["2017-12-15", "2017-12-30", "2018-1-15"]
    for date in biWeekDates:
        createDeposit(ACCOUNT_ID, "balance", date, status, 200, "work")

    # Monthly Transactions
    createPurchase(ACCOUNT_ID, "57cf75cfa73e494d8675f9c6", "balance", "2017-01-03", 60, status, "Vans")
    createPurchase(ACCOUNT_ID, "57cf75cfa73e494d8675f802", "balance", "2017-01-03", 800, status, "Phoenix Park Hotel")
    createPurchase(ACCOUNT_ID, "57cf75cfa73e494d8675f8bd", "balance", "2017-01-07", 11, status, "Mead Center - Movies")
    createPurchase(ACCOUNT_ID, "57cf75cfa73e494d8675f9fc", "balance", "2017-01-03", 80, status, "AT&T")
    # createPurchase(ACCOUNT_ID, "Sling", "balance", "2017-01-03", 20, status, "Television")

    # createPurchase(ACCOUNT_ID, "iPhone X", "balance", "2017-01-03", 800, status, "Christmas")

if __name__ == '__main__':
    # Uncomment to recreate user
    # createUser()
    with open("purchases.json", "w") as file:
        file.write("[" + reduce(lambda x, y: str(x) + "," + str(y), requestPurchasesByAccountID(ACCOUNT_ID)) + "]")
    with open("deposits.json", "w") as file:
        file.write("[" + reduce(lambda x, y: str(x) + "," + str(y), requestDepositsByAccountID(ACCOUNT_ID)) + "]")
