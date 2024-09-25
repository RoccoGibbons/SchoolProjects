import os
from pathlib import Path
import csv
from random import randint

#This makes a new CSV file if one is not present in the current working directory
def csvMake():
    working_directory = os.getcwd()

    field_names = ['CYPHER_TYPE', 'INPUT', 'OUTPUT', 'KEY']

    with open(working_directory + "\data.csv", "a") as file_object:
        dict_object = csv.DictWriter(file_object, fieldnames=field_names)
        dict_object.writeheader()
        file_object.close()

#This adds your all the data needed in the CSV file
def csvAppend(cypher_type, input, output, key):
    working_directory = os.getcwd()

    with open(working_directory + "\data.csv", "a", newline='') as file_object:
        writer = csv.writer(file_object)
        writer.writerow([cypher_type, input, output, key])
        file_object.close()

#This checks if the wanted message + key pair is in the CSV file
def csvCheck(cypher_type, output, key):
    working_directory = os.getcwd()
    rows = []

    #Turns each line in csv into its own dictionary and putting that in rows list
    with open(working_directory + "\data.csv", "r") as file_object:
        csv_reader = csv.DictReader(file_object)
        for row in csv_reader:
            if row["CYPHER_TYPE"] == cypher_type:
                rows.append(row)
        file_object.close()

    for row in rows:
        if row["OUTPUT"] == output and row["KEY"] == key:
            return row["INPUT"]
    return False

#This encrypts your message using a caesar cipher
def caesarEncrypt():
    sentence = input("Please enter the sentence that you want to encrypt: ")
    key = randint(1, 25)
    result = ""

    for letter in sentence:
        letter = ord(letter)
        
        #uppercase
        if letter > 64 and letter < 91:
            letter += key
            if letter > 90:
                letter -= 26

        #lowercase
        elif letter > 96 and letter < 123:
            letter += key
            if letter > 122:
                letter -= 26
        
        result += chr(letter)

    print(f"Your encrypted message is {result}")
    print(f"Your key is {key}")

    csvAppend("caesar", sentence, result, key)

#This decrypts your caesar message
def caesarDecrypt():
    sentence = input("Please input your encrypted message: ")

    key_presence = input("Do you have your key? y/n: ")
    if key_presence.lower() == "y" or key_presence.lower() == "yes":
        while True:
            key = input("Please enter your key: ")
            if not key.isdigit():
                print("Please enter a valid key")
            key = int(key)
            if key < 1 or key > 26:
                print("Please enter a valid key")
            else:
                break
        
        msg = csvCheck("caesar", sentence, key)

        #If msg is in database
        if msg != False:
            print("The message was found in the database")
            print(f"The decrypted message is: {msg}")
            return
        
        #If msg is not in database but have the key
        result = ""
        for letter in sentence:
            letter = ord(letter)

            #uppercase
            if letter > 64 and letter < 91:
                letter -= key
                if letter < 65:
                    letter += 26
            
            #lowercase
            elif letter > 96 and letter < 123:
                letter -= key
                if letter < 97:
                    letter += 26
            
            result += chr(letter)

        print("The message was not found in the database")
        print(f"The decrypted message is {result}")
        return

    #If they do not have the key
    print("Here is a list of possible decryptions, if one looks like it forms a coherent sentence - that is your decrypted message")
    for i in range(26):
        result = ""
        for letter in sentence:
            letter = ord(letter)
            letter += i
            if (letter > 90 and letter < 97) or letter > 122:
                letter -= 26
            result += chr(letter)
        print(result)

#This encrypts your message using a substitution cipher
def substitutionEncrypt():
    sentence = input("Please enter the sentence that you want to encrypt: ")

    alphabet_dict = {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': '', 'i': '', 'j': '', 'k': '', 'l': '', 'm': '', 'n': '', 
                     'o': '', 'p': '', 'q': '', 'r': '', 's': '', 't': '', 'u': '', 'v': '', 'w': '', 'x': '', 'y': '', 'z': ''}
    
    key = ""
    
    alphabet_constant = "abcdefghijklmnopqrstuvwxyz"
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    #Create unique key and store it in a dictionary and a string
    for i in range(len(alphabet_constant)):
        position = randint(0, len(alphabet) - 1)
        key += alphabet[position]
        alphabet_dict[alphabet_constant[i]] = alphabet[position]
        alphabet = alphabet[:position] + alphabet[position+1:]
    
    #binary number, if 1 then capital, if 0 then not capital
    upper_case_test = ""
    for letter in sentence:
        if ord(letter) > 64 and ord(letter) < 91:
            #is a capital letter
            upper_case_test += "1"
        else:
            upper_case_test += "0"

    sentence = sentence.lower()

    encrypted = ""
    for letter in sentence:
        #is a letter
        if ord(letter) > 96 and ord(letter) < 123:
            encrypted += alphabet_dict[letter]
        #is a symbol
        else:
            encrypted += letter
    
    result = ""
    for i in range(len(encrypted)):
        if upper_case_test[i] == "1":
            result += encrypted[i].upper()
        else:
            result += encrypted[i]

    print(f"Your encrypted message is {result}")
    print(f"Your key is {key}")

    csvAppend("substitution", sentence, result, key)

#This decrypts your substitution cypher
def substitutionDecrypt():
    sentence = input("Please input your encrypted message: ")
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    valid_key = False
    while valid_key == False:
        valid_key = True
        key = input("Please enter your key: ")

        for letter in key:
            if letter in alphabet:
                alphabet.replace(letter, '')
                continue
            else:
                print("Key is not valid")
                valid_key = False
                break
    
    #check csv file
    msg = csvCheck("substitution", sentence, key)

    if msg != False:
        print("The message was found in the database")
        print(f"The decrypted message is: {msg}")
        return
    
    else:
        alphabet_dict = {}
        alphabet_constant = "abcdefghijklmnopqrstuvwxyz"
        
        for i in range(len(key)):
            alphabet_dict[key[i]] = alphabet_constant[i]
        
        result = ""
        for letter in sentence:
            result += alphabet_dict[letter]
        
        print("The message was not found in the database")
        print(f"The decrypted message is {result}")
        
        return


#---------------Beginning of main code---------------

#Checks if there is a CSV file already in the working directory
working_directory = os.getcwd()
file = Path(working_directory + "\data.csv")
if not file.is_file():
    csvMake()

#Working loop
while True:
    print("Welcome to the encryption/ decryption ")

    #Checks for valid inputs
    option = input("Encrypt: 1 Decrypt: 2 Exit: 3\n")
    if not option.isdigit():
        print("Please input a valid option")
        continue
    if option not in ["1", "2", "3"]:
        print("Please input a valid option")
        continue

    #Encryption
    if option == "1":
        print("What cypher do you want to use?")
        cypher = input("Caesar: 1 Substitution: 2\n")

        #Checks validity of user input
        if not cypher.isdigit():
            print("Please input a valid cypher")
            continue

        if cypher not in ["1", "2"]:
            print("Please input a valid cypher")
            continue
        
        #Runs the cyphers
        if cypher == "1":
            caesarEncrypt()
        elif cypher == "2":
            substitutionEncrypt()


    #Decryption
    elif option == "2":
        print("Which cypher are you decrypting?")
        cypher = input("Caesar: 1 Substitution: 2\n")

        #Checks validity of user input
        if not cypher.isdigit():
            print("Please input a valid cypher")
            continue

        if cypher not in ["1", "2"]:
            print("Please input a valid cypher")
            continue
        
        #Runs the decrypters
        if cypher == "1":
            caesarDecrypt()
        elif cypher == "2":
            substitutionDecrypt()

    #Exit loop
    elif option == "3":
        print("Thank you for using the encryption/ decryption software")
        break
    
    #Catch unexpected results
    else:
        print("How did we get here: Achievment unlocked")
        continue