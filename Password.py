import random
# imports for database
import requests
import pandas as pd

# importing the API
from rdoclient import RandomOrgClient
#from randomorg import RandomOrgClient
# import used for validating URLs
import validators



# Ensures that the genrated password is valid
def Valid_Password(password, special, number, lower, upper):
    # A password is valid if it contains at least one upper case letter,
    # one lower case letter, one number, and one special characters
    #API_KEY = "1b4847da-504e-49b4-8256-797d1338de64"
    r = RandomOrgClient(API_KEY)
    random_ints = []

    up = 0
    low = 0
    num = 0
    spec = 0

    for num in password:
        if num >= 65 and num <= 90:
            up += 1
        if num >= 97 and num <= 122:
            low += 1
        if num >= 48 and num <= 57:
            number = True
        if num >= 33 and num <= 47:
            special = True

    if not upperCase:
        random_ints.append(r.generate_integers(1, 65, 90))  # Upper case letter
    if not lowerCase:
        random_ints.append(r.generate_integers(1, 97, 122))  # Lower case letter
    if not number:
        random_ints.append(r.generate_integers(1, 48, 57))  # Number
    if not special:
        random_ints.append(r.generate_integers(1, 33, 47))  # Special character

    return random_ints
# If the user already has this website in their database, ask if they want
    # to override the existing password
    #select_query = db.select(password_table).where(
        #password_table.c.website == website)
    #result = connection.execute(select_query)

    # Check if the website exists in the database
    #if result.fetchone():
        #valid_input = False
        #while valid_input is not True:
            #user_input = input(
                #f"The website '{website}' is already has a password. Would you like of override it?(Y/N) ")
            #if user_input.lower() == "y":
                # Deletes the website from the database
                #delete_query = db.delete(password_table).where(
                    #password_table.c.website == website)
                #result = connection.execute(delete_query)
                #valid_input = True
            #elif user_input.lower() == "n":
                # returns without creating password
                #valid_input = True
                #return
            #else:
                #print("Your input was invalid, try again")

def Create_Password(length, special, number, lower, upper):
    
    API_KEY = "1b4847da-504e-49b4-8256-797d1338de64"
    r = RandomOrgClient(API_KEY)
    # Generates PASSWORD_LENGTH number of random integers from 33 to 126

    random_spec =[]
    random_num = []
    random_low = []
    random_up = []

    if int(special) > 0:
        random_spec = r.generate_integers(special, 33, 47)
    if int(number) > 0:
        random_num = r.generate_integers(number, 48, 57)
    if int(lower) > 0:
        random_low = r.generate_integers(lower, 97, 122)
    if int(upper) > 0:
        random_up = r.generate_integers(upper, 65, 90)

    
    #random_ints = r.generate_integers(length, 33, 126)

    #special_ints = Valid_Password(random_ints, special, number, lower, upper)

    random_ints = []

    for num in random_spec:
        random_ints.append(num)
    for num in random_num:
        random_ints.append(num)
    for num in random_low:
        random_ints.append(num)
    for num in random_up:
        random_ints.append(num)
    length = random.randint(10, 30)
    if (length > special + number + lower + upper):
        new_ints = r.generate_integers(length - (special + number + lower + upper), 33, 126)
        for num in new_ints:
            random_ints.append(num)    

    password = ""

    for char in random_ints:
        password += chr(char)

    #scrambles the password
    shuffled_password = "".join(random.sample(password, len(password)))
    # Inserts the password into the database
    #ins = password_table.insert().values(website=website, password=password)
    #connection.execute(ins)

    return shuffled_password


def Quick_Create_Password():
    API_KEY = "1b4847da-504e-49b4-8256-797d1338de64"

    r = RandomOrgClient(API_KEY)
    # Using random.randint() to minimize the calls to the API
    PASSWORD_LENGTH = random.randint(10, 25)

    # Generates PASSWORD_LENGTH number of integers from 33 to 126
    random_ints = r.generate_integers(PASSWORD_LENGTH, 33, 126)

    special_ints = Valid_Password(random_ints)

    # Adds the characters that would make the password valid onto the end of the password
    if len(special_ints) != 0:
        i = len(random_ints) - 1
        for num in special_ints:
            random_ints[i] = num[0]
            i = i - 1

    password = ""

    for char in random_ints:
        password += chr(char)

    website = "No website, password was quick generated"

    # Inserts the password into the database
    ins = password_table.insert().values(website=website, password=password)
    connection.execute(ins)

    print()
    print("PassWord: " + password)
    print()


def Print_Password():
    # Retrieve and print the contents of the table
    select_query = db.select(password_table)
    result = connection.execute(select_query)

    print()
    print("Here are your passwords:")
    print()

    for row in result:
        print("Website:", row[0])
        print("Password:", row[1])
        print()


#data = {}
#passwords = pd.DataFrame.from_dict(data)
#engine = db.create_engine('sqlite:///passwords_data_base.db')
#connection = engine.connect()

# Define the table schema
#metadata = db.MetaData()
#password_table = db.Table('password_table', metadata,
 #                         db.Column('website', db.String),
  #                        db.Column('password', db.String))

# Create the table
#metadata.create_all(engine)

