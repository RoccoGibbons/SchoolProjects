import os
from pathlib import Path
import csv
from random import randint
from time import sleep

def caesarPrint():
    print("""
 ______                               
|      |.---.-.-----.-----.---.-.----.
|   ---||  _  |  -__|__ --|  _  |   _|
|______||___._|_____|_____|___._|__|                                    
""")

def subPrint():
    print("""
 _______         __           __   __ __          __   __              
|     __|.--.--.|  |--.-----.|  |_|__|  |_.--.--.|  |_|__|.-----.-----.
|__     ||  |  ||  _  |__ --||   _|  |   _|  |  ||   _|  ||  _  |     |
|_______||_____||_____|_____||____|__|____|_____||____|__||_____|__|__|                                                             
""")

def streamPrint():
    print("""
 _______ __                             
|     __|  |_.----.-----.---.-.--------.
|__     |   _|   _|  -__|  _  |        |
|_______|____|__| |_____|___._|__|__|__|
""")

# This makes a new CSV file if one is not present in the current working directory
def csvMake():
    working_directory = os.getcwd()

    field_names = ['CIPHER_TYPE', 'INPUT', 'OUTPUT', 'KEY']

    with open(working_directory + "\data.csv", "a") as file_object:
        dict_object = csv.DictWriter(file_object, fieldnames=field_names)
        dict_object.writeheader()
        file_object.close()

#This adds your all the data needed in the CSV file
def csvAppend(cipher_type, input, output, key):
    working_directory = os.getcwd()

    with open(working_directory + "\data.csv", "a", newline='') as file_object:
        writer = csv.writer(file_object)
        writer.writerow([cipher_type, input, output, key])
        file_object.close()

#This checks if the wanted message + key pair is in the CSV file
def csvCheck(cipher_type, output, key):
    working_directory = os.getcwd()
    rows = []

    #Turns each line in csv into its own dictionary and putting that in rows list
    with open(working_directory + "\data.csv", "r") as file_object:
        csv_reader = csv.DictReader(file_object)
        for row in csv_reader:
            if row["CIPHER_TYPE"] == cipher_type:
                rows.append(row)
        file_object.close()

    for row in rows:
        if row["OUTPUT"] == output and row["KEY"] == key:
            return row["INPUT"]
    return False

#This encrypts your message using a caesar cipher
def caesarEncrypt():
    os.system('cls')
    caesarPrint()

    sentence = input("\nPlease enter the sentence that you want to encrypt:\n")

    sleep(0.5)

    while True:
        os.system('cls')
        caesarPrint()

        choice = input("\n    Choose key: 1\n    Get a random key: 2\n\n")
        if choice not in ["1", "2"]:
            print("\nPlease choose a valid option")
            sleep(1)
        else:
            break
    
    sleep(0.5)
    while True:
        os.system('cls')
        caesarPrint()

        if choice == "1":
            key = input("Enter key:\n")
            if key.isdigit() == False:
                print("\nPlease enter a valid key")
                sleep(1)
                continue
            elif int(key) < 1 or int(key) > 25:
                print("\nPlease enter a key inbetween 1 and 25")
                sleep(1)
                continue
            break
        elif choice == "2":
            key = randint(1, 25)
            break

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
            letter += int(key)
            if letter > 122:
                letter -= 26
        
        result += chr(letter)

    sleep(0.5)
    os.system('cls')
    caesarPrint()
    
    print(f"\nYour encrypted message is {result}")
    print(f"Your key is {key}")

    csvAppend("caesar", sentence, result, key)

    input("\nPress any key to continue")
    sleep(0.2)

#This decrypts your caesar message
def caesarDecrypt():
    os.system('cls')
    caesarPrint()

    sentence = input("\nPlease input your encrypted message:\n")

    sleep(0.5)
    os.system('cls')
    caesarPrint()

    key_presence = input("\nDo you have your key? y/n: \n")
    sleep(0.5)

    if key_presence.lower() == "y" or key_presence.lower() == "yes":
        while True:
            os.system('cls')
            caesarPrint()

            key = input("\nPlease enter your key:\n")

            if not key.isdigit():
                print("\nPlease enter a valid key")
                sleep(1)
                continue
            if int(key) < 1 or int(key) > 26:
                print("\nPlease enter a valid key")
                sleep(1)
            else:
                break
        
        msg = csvCheck("caesar", sentence, key)

        sleep(0.5)

        # If msg is in database
        if msg != False:
            os.system('cls')
            caesarPrint()
            print("\nThe message was found in the database")
            print(f"The decrypted message is: {msg}")
            input("\nPress any key to continue")
            sleep(0.2)
            return
        
        #If msg is not in database but have the key
        result = ""
        for letter in sentence:
            letter = ord(letter)

            #uppercase
            if letter > 64 and letter < 91:
                letter -= int(key)
                if letter < 65:
                    letter += 26
            
            #lowercase
            elif letter > 96 and letter < 123:
                letter -= int(key)
                if letter < 97:
                    letter += 26
            
            result += chr(letter)

        os.system('cls')
        caesarPrint()
        print("\nThe message was not found in the database")
        print(f"The decrypted message is {result}")
        input("\nPress any key to continue")
        sleep(0.2)
        return

    #If they do not have the key
    os.system('cls')
    caesarPrint()
    print("\nHere is a list of possible decryptions, if one looks like it forms a coherent sentence - that is your decrypted message")

    for i in range(26):
        result = ""
        for letter in sentence:
            letter = ord(letter)
            if letter > 64 and letter < 91:
                letter += i
                if letter > 90:
                    letter -= 26
            elif letter > 96 and letter < 123:
                letter += i
                if letter > 122:
                    letter -= 26
            result += chr(letter)
        print(result)
    input("\nPress any key to continue")
    sleep(0.2)


#This encrypts your message using a substitution cipher
def substitutionEncrypt():
    os.system('cls')
    subPrint()

    sentence = input("\nPlease enter the sentence that you want to encrypt:\n")

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
    
    sleep(0.5)
    os.system('cls')
    subPrint()

    print(f"\nYour encrypted message is {result}")
    print(f"Your key is {key}")

    csvAppend("substitution", sentence, result, key)
    input("\nPress any key to continue")

#This decrypts your substitution cipher
def substitutionDecrypt():
    os.system('cls')
    subPrint()

    sentence = input("\nPlease input your encrypted message:\n")
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    sleep(0.5)

    valid_key = False
    while True:
        os.system('cls')
        subPrint()
        valid_key = True
        key = input("\nPlease enter your key:\n")

        if len(key) != 26:
            sleep(0.5)
            os.system('cls')
            subPrint()
            print("\nKey is not correct length")
            valid_key = False
            sleep(1)
            continue

        for letter in key:
            if letter in alphabet:
                alphabet.replace(letter, '')
                continue
            else:
                sleep(0.5)
                os.system('cls')
                subPrint()
                print("\nKey is not valid")
                valid_key = False
                sleep(1)
                break

        if valid_key == True:
            break
        
    
    # check csv file
    msg = csvCheck("substitution", sentence, key)

    sleep(0.5)
    os.system('cls')
    subPrint()

    if msg != False:
        print("\nThe message was found in the database")
        print(f"The decrypted message is: {msg}")
        input("\nPress any key to continue")
        sleep(0.2)
        return
    
    else:
        alphabet_dict = {}
        alphabet_constant = "abcdefghijklmnopqrstuvwxyz"
        
        for i in range(len(key)):
            alphabet_dict[key[i]] = alphabet_constant[i]
        
        upper_case_test = ""
        for letter in sentence:
            if ord(letter) > 64 and ord(letter) < 91:
                #is a capital letter
                upper_case_test += "1"
            else:
                upper_case_test += "0"

        sentence = sentence.lower()
        
        lower_case = ""
        for letter in sentence:
            if letter in alphabet_dict:
                lower_case += alphabet_dict[letter]
            else:
                lower_case += letter
        
        result = ""
        for i in range(len(lower_case)):
            if upper_case_test[i] == "1":
                result += lower_case[i].upper()
            else:
                result += lower_case[i]
                
        print("\nThe message was not found in the database")
        print(f"The decrypted message is {result}")
        input("\nPress any key to continue")
        sleep(0.2)
        return

#Turns a string into binary
def stringToBinary(string):
    ascii = []
    for letter in string:
        ascii.append(ord(letter))

    binary = ""
    for value in ascii:
        value = bin(value)
        value = str(value)[2:]
        if len(value) < 8:
            extra = 8 - len(value)
            value = ("0" * extra) + value
        binary += value
    
    return binary

#Turns binary into a string of characters
def binaryToString(binary):
    #Split into groups of bytes
    binary = [binary[i:i+8] for i in range(0, len(binary), 8)]

    result = ""

    for byte in binary:
        result += chr(int(byte, 2))
    return repr(result)[1:-1]

#Turns binary into hexadecimal
def binaryToHex(binary):
    #Split into groups of nibbles
    binary = [binary[i:i+4] for i in range(0, len(binary), 4)]

    result = "0x"

    for nibble in binary:
        pos = 0
        value = 0
        for bit in nibble:
            if pos == 0 and bit == "1":
                value += 8
            elif pos == 1 and bit == "1":
                value += 4
            elif pos == 2 and bit == "1":
                value += 2
            elif pos == 3 and bit == "1":
                value += 1
            pos += 1
        values = {10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}
        if value < 10:
            result += str(value)
        else:
            result += values[value]
    
    return result 

#Turns a hexadecimal value into binary
def hexToBinary(hex):
    hex = hex[2:]
    binary = ""
    values = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
    for x in hex:
        if x in values:
            x = values[x]
        else:
            x = int(x)

        for i in range(4):
            if i == 0 and x // 8 >= 1:
                binary += "1"
                x -= 8
            elif i == 1 and x // 4 >= 1:
                binary += "1"
                x -= 4
            elif i == 2 and x // 2 >= 1:
                binary += "1"
                x -= 2
            elif i == 3 and x // 1 >= 1:
                binary += "1"
                x -= 1
            else:
                binary += "0"
    
    return binary

#This encrypts your message using a stream cipher
def streamEncrypt():
    os.system('cls')
    streamPrint()
    sentence = input("\nPlease enter the sentence you want to encrypt:\n")

    #Generate random key
    key = ""
    for i in range(len(sentence) * 8):
        key += str(randint(0, 1))

    binary = stringToBinary(sentence)

    encrypted = ""

    #Perfoms XOR bitwise operation on both binary strings
    for i in range(len(binary)):
        encrypted += str(int(binary[i]) ^ int(key[i]))

    result_store = binaryToHex(encrypted)
    hex_key = binaryToHex(key)

    #These display ASCII versions of the key and msg but due to special characters (\n etc), I could not find out how to reverse it for the decrypt
    #Now just the hex versions are given and stored
    #result_display = binaryToString(encrypted)
    #char_key = binaryToString(key)

    sleep(0.5)
    os.system('cls')
    streamPrint()

    print(f"\nYour encrypted message is {result_store}")
    print(f"Your key is {hex_key}")    

    csvAppend("stream", sentence, result_store, hex_key)
    input("\nPress any key to continue")
    sleep(0.2)
    return 

#This decrypts your stream cipher
def streamDecrypt():
    while True:
        error = 0
        os.system('cls')
        streamPrint()

        sentence = input("\nPlease enter your encrypted message in hexadecimal (Prefix it with 0x):\n")
        sleep(0.5)

        for char in sentence:
            if char.isdigit() == False:
                if not (ord(char) > 64 and ord(char) < 71) and char != 'x':
                    os.system('cls')
                    streamPrint()

                    print("\nInvalid input, please enter a hexadecimal")
                    sleep(1)
                    error = 1
                    break
        if error == 0:
            break
    
    while True:
        error = 0
        os.system('cls')
        streamPrint()

        key = input("\nPlease enter your key in hexadecimal (Prefix it with 0x):\n")
        sleep(0.5)

        for char in key:
            if char.isdigit() == False:
                if ord(char) < 64 and ord(char) > 71:
                    os.system('cls')
                    streamPrint()

                    print("\nInvalid input, please enter a hexadecimal")
                    sleep(1)
                    error = 1
                    break
        if error == 0:
            break

    #This is if the inputs were the ASCII versions of the key/ msg, but if either contained special characters it broke
    # sentence_bin = stringToBinary(sentence)
    # key_bin = stringToBinary(key)
    # sentence_hex = binaryToHex(sentence_bin)
    # key_hex = binaryToHex(key_bin)

    # check csv file
    msg = csvCheck("stream", sentence, key)
    
    if msg != False:
        sleep(0.5)
        os.system('cls')
        streamPrint()

        print("\nThe message was found in the database")
        print(f"The decrypted message is: {msg}")
        input("\nPress any key to continue")
        sleep(0.2)
        return
    
    key_bin = hexToBinary(key)
    sentence_bin = hexToBinary(sentence)    

    result_bin = ""
    for i in range(len(sentence_bin)):
        result_bin += str(int(sentence_bin[i]) ^ int(key_bin[i]))

    result = binaryToString(result_bin)
    sleep(0.5)
    os.system('cls')
    streamPrint()

    print("\nThe message was not found in the database")
    print(f"The decrypted message is {result}")
    input("\nPress any key to continue")
    sleep(0.2)
    return


#---------------Beginning of main code---------------

#Checks if there is a CSV file already in the working directory
working_directory = os.getcwd()
file = Path(working_directory + "\data.csv")
if not file.is_file():
    csvMake()


#Working loop
while True:
    os.system('cls')
    print(""" ________         __                                             _______                               __                        _____                               __    _____ 
|  |  |  |.-----.|  |.----.-----.--------.-----.     ______     |    ___|.-----.----.----.--.--.-----.|  |_     .-----.----.    |     \.-----.----.----.--.--.-----.|  |_ |__   |
|  |  |  ||  -__||  ||  __|  _  |        |  -__|    |______|    |    ___||     |  __|   _|  |  |  _  ||   _|    |  _  |   _|    |  --  |  -__|  __|   _|  |  |  _  ||   _|',  ,-'
|________||_____||__||____|_____|__|__|__|_____|                |_______||__|__|____|__| |___  |   __||____|    |_____|__|      |_____/|_____|____|__| |___  |   __||____| |--|  
                                                                                         |_____|__|                                                    |_____|__|          '--'  
""")

    #Checks for valid inputs
    option = input("   Encrypt: 1\n   Decrypt: 2\n   Exit: 3\n\n")
    if not option.isdigit():
        print("Please input a valid option")
        sleep(1)
        os.system('cls')
        continue
    if option not in ["1", "2", "3"]:
        print("Please input a valid option")
        sleep(1)
        os.system('cls')
        continue

    sleep(0.5)

    #Encryption
    if option == "1":
        while True:
            os.system('cls')
            print("""
 _______                               __   __              
|    ___|.-----.----.----.--.--.-----.|  |_|__|.-----.-----.
|    ___||     |  __|   _|  |  |  _  ||   _|  ||  _  |     |
|_______||__|__|____|__| |___  |   __||____|__||_____|__|__|
                        |_____|__|                         
""")
            print("\nWhat cipher do you want to use?\n")
            cipher = input("   Caesar: 1\n   Substitution: 2\n   Stream: 3\n\n")

            #Checks validity of user input
            if not cipher.isdigit():
                print("Please input a valid cipher")
                sleep(1)
                os.system('cls')
                continue

            if cipher not in ["1", "2", "3"]:
                print("Please input a valid cipher")
                sleep(1)
                os.system('cls')
                continue

            break
        
        sleep(0.5)
        #Runs the ciphers
        if cipher == "1":
            caesarEncrypt()
        elif cipher == "2":
            substitutionEncrypt()
        elif cipher == "3":
            streamEncrypt()
        else:
            sleep(0.5)
            os.system('cls')
            print("Something went wrong")
            sleep(1)


    #Decryption
    elif option == "2":
        while True:
            sleep(0.5)
            os.system('cls')
            print("""
 _____                               __   __              
|     \.-----.----.----.--.--.-----.|  |_|__|.-----.-----.
|  --  |  -__|  __|   _|  |  |  _  ||   _|  ||  _  |     |
|_____/|_____|____|__| |___  |   __||____|__||_____|__|__|
                       |_____|__|                         
""")
            print("\nWhich cipher are you decrypting?\n")
            cipher = input("   Caesar: 1\n   Substitution: 2\n   Stream: 3\n\n")

            #Checks validity of user input
            if not cipher.isdigit():
                print("Please input a valid cipher")
                continue

            if cipher not in ["1", "2", "3"]:
                print("Please input a valid cipher")
                continue

            break
        
        sleep(0.5)
        #Runs the decrypters
        if cipher == "1":
            caesarDecrypt()
        elif cipher == "2":
            substitutionDecrypt()
        elif cipher == "3":
            streamDecrypt()
        else:
            sleep(0.5)
            os.system('cls')
            print("Something went wrong")
            sleep(1)

    #Exit loop
    elif option == "3":
        sleep(0.5)
        os.system('cls')
        print("""
 _______                 __ __                
|     __|.-----.-----.--|  |  |--.--.--.-----.
|    |  ||  _  |  _  |  _  |  _  |  |  |  -__|
|_______||_____|_____|_____|_____|___  |_____|
                                 |_____|      
""")
        break
    
    #Catch unexpected results
    else:
        sleep(0.5)
        os.system('cls')
        print("How did we get here: Achievment unlocked")
        sleep(1)
        continue