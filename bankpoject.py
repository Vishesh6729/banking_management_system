import json
import random
import string
from pathlib import Path


class Bank:

    database = 'data.json'
    data = []

    # Load existing data from JSON file
    try:
        if Path(database).exists():
            with open(database, 'r') as fs:
                data = json.loads(fs.read())
        else:
            print("No such file exists. A new database will be created.\n")

    except Exception as err:
        print(f"An error occurred: {err}")


    # Update / save data into JSON file
    @classmethod
    def __update(cls):

        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(cls.data, indent=4))


    # Generate random account number
    @classmethod
    def __accountgenerate(cls):

        alph = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)

        id = alph + num + spchar

        random.shuffle(id)

        return "".join(id)


    # Create account
    def creataccount(self):

        try:
            info = {
                "name": input("Tell your name :-\n"),
                "age": int(input("Tell your age :-\n")),
                "email": input("Tell your email id :-\n"),
                "pin": int(input("Tell your 4 digit pin :-\n")),
                "accountNo.": Bank.__accountgenerate(),
                "balance": 0
            }

            # Check age
            if info['age'] < 18:
                print("Sorry, you must be at least 18 years old.\n")
                return

            # Check PIN
            if len(str(info['pin'])) != 4:
                print("PIN must contain exactly 4 digits.\n")
                return

            print("\nYour account is created successfully!")

            for i in info:
                print(f"{i} : {info[i]}")

            print("\nPlease note down your account number.")

            Bank.data.append(info)

            Bank.__update()

        except ValueError:
            print("Please enter valid numeric values for age and PIN.")


    # Deposit money
    def depositemoney(self):

        accnumber = input("Please enter your account number :-\n")

        try:
            pin = int(input("Please enter your PIN as well :-\n"))
        except ValueError:
            print("PIN must contain numbers only.")
            return

        userdata = [
            i for i in Bank.data
            if i['accountNo.'] == accnumber and i['pin'] == pin
        ]

        if not userdata:
            print("Sorry, no data found.")
            return

        try:
            amount = int(input("How much do you want to deposit? :-\n"))
        except ValueError:
            print("Please enter a valid amount.")
            return

        if amount > 10000 or amount <= 0:
            print("You can deposit more than 0 and up to 10000.")
            return

        userdata[0]['balance'] += amount

        Bank.__update()

        print("Money is deposited successfully.")
        print(f"Your new balance is: {userdata[0]['balance']}")


    # Withdraw money
    def withdrawmoney(self):

        accnumber = input("Please enter your account number :-\n")

        try:
            pin = int(input("Please enter your PIN as well :-\n"))
        except ValueError:
            print("PIN must contain numbers only.")
            return

        userdata = [
            i for i in Bank.data
            if i['accountNo.'] == accnumber and i['pin'] == pin
        ]

        if not userdata:
            print("Sorry, no data found.")
            return

        try:
            amount = int(input("Enter the amount you want to withdraw :-\n"))
        except ValueError:
            print("Please enter a valid amount.")
            return

        if amount <= 0:
            print("Withdrawal amount must be greater than 0.")
            return

        if amount > userdata[0]['balance']:
            print("You don't have that much money.")
            return

        userdata[0]['balance'] -= amount

        Bank.__update()

        print("Money is withdrawn successfully.")
        print(f"Your remaining balance is: {userdata[0]['balance']}")


    # Show account details
    def showdetails(self):

        accnumber = input("Please enter your account number :-\n")

        try:
            pin = int(input("Please enter your PIN as well :-\n"))
        except ValueError:
            print("PIN must contain numbers only.")
            return

        userdata = [
            i for i in Bank.data
            if i['accountNo.'] == accnumber and i['pin'] == pin
        ]

        if not userdata:
            print("Sorry, no data found.")
            return

        print("\nYour information is:\n")

        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")


    # Update account details
    def updatingdetails(self):

        accnumber = input("Please enter your account number :-\n")

        try:
            pin = int(input("Please enter your PIN as well :-\n"))
        except ValueError:
            print("PIN must contain numbers only.")
            return

        userdata = [
            i for i in Bank.data
            if i['accountNo.'] == accnumber and i['pin'] == pin
        ]

        if not userdata:
            print("Sorry, no data found.")
            return

        print("\nYou cannot change age, account number and balance.\n")
        print("Fill the details for changes or leave them empty to keep old values.\n")

        newname = input("Enter your new name or press Enter to skip :-\n")
        newemail = input("Enter your new email or press Enter to skip :-\n")
        newpin = input("Enter your new 4 digit PIN or press Enter to skip :-\n")

        # Name
        if newname == "":
            newname = userdata[0]['name']

        # Email
        if newemail == "":
            newemail = userdata[0]['email']

        # PIN
        if newpin == "":
            newpin = userdata[0]['pin']
        else:
            if not newpin.isdigit() or len(newpin) != 4:
                print("PIN must contain exactly 4 digits.")
                return

            newpin = int(newpin)

        newdata = {
            "name": newname,
            "email": newemail,
            "pin": newpin
        }

        # Update only changed values
        for i in newdata:

            if newdata[i] == userdata[0][i]:
                continue

            else:
                userdata[0][i] = newdata[i]

        Bank.__update()

        print("\nYour bank account details were successfully updated.\n")


    # Delete account
    def deleteaccount(self):

        accnumber = input("Please enter your account number :-\n")

        try:
            pin = int(input("Please enter your PIN as well :-\n"))
        except ValueError:
            print("PIN must contain numbers only.")
            return

        userdata = [
            i for i in Bank.data
            if i['accountNo.'] == accnumber and i['pin'] == pin
        ]

        if not userdata:
            print("Sorry, no data found.")
            return

        check = input(
            "Press Y if you want to delete your account "
            "or N if you don't want to delete it :-\n"
        )

        if check == 'Y' or check == 'y':

            index = Bank.data.index(userdata[0])

            Bank.data.pop(index)

            Bank.__update()

            print("Account deleted successfully.")

        else:
            print("Account deletion cancelled.")


# Create object
user = Bank()


# Menu
print("\n========== BANK MANAGEMENT SYSTEM ==========\n")

print("Press 1 for creating an account")
print("Press 2 for depositing money")
print("Press 3 for withdrawing money")
print("Press 4 for account details")
print("Press 5 for updating the details")
print("Press 6 for deleting the account")


# User choice
try:
    response = int(input("\nEnter your response :- "))

except ValueError:
    print("Please enter a number from 1 to 6.")
    response = 0


# Calling appropriate method
if response == 1:
    user.creataccount()

elif response == 2:
    user.depositemoney()

elif response == 3:
    user.withdrawmoney()

elif response == 4:
    user.showdetails()

elif response == 5:
    user.updatingdetails()

elif response == 6:
    user.deleteaccount()

else:
    print("Invalid choice. Please select a number between 1 and 6.")