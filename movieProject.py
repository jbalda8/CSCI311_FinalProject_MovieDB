import cx_Oracle
import pandas as pd
import numpy as np
from tabulate import tabulate

# Database connection. Note I am hiding my actual database password information
connection = cx_Oracle.connect('connection goes here')

cursor = connection.cursor()

# Admin login credentials
adminUsername = "jbalda"
adminPassword = "password"

# Member login credentials
memberUsername = ['10', '11', '12', '13', '14']
memberPassword = "memberpassword"

# Main menu
def menu():
    print("""
    1) Admin
    2) Member
    3) Exit
    """)
    menuResponse = str(input("What is your choice: "))
    while menuResponse not in ['1', '2', '3']:
        menuResponse = (input("That is not a valid choice. Choose 1, 2, or 3: "))
    if menuResponse == '1':
        inputUsername = str(input("What is your admin username: "))
        inputPassword = str(input("What is your admin password: "))
        while (inputUsername != adminUsername) or (inputPassword != adminPassword):
            inputUsername = str(input("That login combination is incorrect. What is your admin username: "))
            inputPassword = str(input("What is your admin password: "))
    elif menuResponse == '2':
        inputUsername = str(input("What is your member username: "))
        inputPassword = str(input("What is your member password: "))
        while (inputUsername not in memberUsername) or (inputPassword != memberPassword):
            inputUsername = str(input("That login combination is incorrect. What is your member username: "))
            inputPassword = str(input("What is your member password: "))
    return menuResponse

# If user chooses Admin from main menu
def adminMenu():
    print("""
        1) Add new movie
        2) Add new member
        3) Search and update movie
        4) Search and delete movie
        5) Search and update member
        6) Search and delete member
        """)
    adminResponse = str(input("What is your choice: "))
    while adminResponse not in ['1', '2', '3', '4', '5', '6']:
        adminResponse = (input("That is not a valid choice. Choose 1, 2, 3, 4, 5, or 6: "))
    return adminResponse


# If user chooses member from main menu
def memberMenu():
    print("""
        1) Search movie
        2) Rent movie
        3) Return movie
        """)
    memberResponse = str(input("What is your choice: "))
    while memberResponse not in ['1', '2', '3']:
        memberResponse = (input("That is not a valid choice. Choose 1, 2, or 3: "))
    return memberResponse

def searchMovie():
    updateID = None
    while updateID is None:
        identifier = str(input("What is the title of the movie you want to update: "))
        for row in cursor.execute("SELECT movie_id FROM mm_movie WHERE movie_title = :mybv", mybv=identifier):
            for item in row:
                updateID = item
    pd.DataFrame()
    updateID = int(updateID)
    for row in cursor.execute("SELECT * FROM mm_movie WHERE movie_title = :mybv", mybv=identifier):
        arr = np.array(row)

    df = pd.DataFrame([arr], columns=['MOVIE_ID', 'MOVIE_TITLE', 'MOVIE_CAT_ID', 'MOVIE_VALUE', 'MOVIE_QTY'])
    print(tabulate(df, headers='keys', tablefmt='psql'))
    return updateID

def searchMember():
    updateID = None
    while updateID is None:
        identifier = input("What is the member's ID: ")
        for row in cursor.execute("SELECT member_id FROM mm_member WHERE member_id = :mybv", mybv=int(identifier)):
            for item in row:
                updateID = item
    pd.DataFrame()
    updateID = int(updateID)
    for row in cursor.execute("SELECT * FROM mm_member WHERE member_id = :mybv", mybv=updateID):
        arr = np.array(row)

    df = pd.DataFrame([arr], columns=['MEMBER_ID', 'LAST', 'FIRST', 'LICENSE_NO', 'LICENSE_ST', 'CREDIT_CARD',
                                      'SUSPENSION', 'MAILING_LIST'])
    print(tabulate(df, headers='keys', tablefmt='psql'))

class AdminApp:
    def __init__(self):
        self.adminResponse = adminMenu()

    def addMovie(self):
        movieTitle = str(input("What is the movie title: "))
        try:
            movieCat = int(input("What is the movie category: "))
            movieVal = int(input("What is the movie value: "))
            movieQty = int(input("What is the movie quantity: "))
            out_str = cursor.var(str)
        except:
            print("There was an error with that input!")
        finally:
            cursor.callproc('add_movie', [movieTitle, movieCat, movieVal, movieQty, out_str])
            return out_str.getvalue()

    def addMember(self):
        memberLast = str(input("What is the member's last name: "))
        memberFirst = str(input("What is the member's first name: "))
        memberLicense = str(input("What is the member's license number: "))
        memberState = str(input("What is the state of the member's license: "))
        memberCredit = str(input("What is the member's credit card number: "))
        memberMailing = str(input("Does the member want to be on the mailing list (Y or N): "))
        out_str = cursor.var(str)
        out_int = cursor.var(int)
        cursor.callproc('add_member',  [memberLast, memberFirst, memberLicense, memberState,
                                        memberCredit, memberMailing, out_str, out_int])
        return out_str.getvalue()

    def searchUpdateMovie(self):
        updateID = searchMovie()

        updateTitle = str(input("What is the updated movie title: "))

        try:
            updateCat = int(input("What is the updated movie category: "))
            updateVal = int(input("What is the updated movie value: "))
            updateQty = int(input("What is the updated movie quantity: "))
        except:
            print("There was an error with that input!")
        finally:
            update_output = cursor.callfunc('update_movie', str, [updateID, updateTitle,
                                                                  updateCat, updateVal, updateQty])
            return update_output

    def searchDeleteMovie(self):
        deleteID = searchMovie()

        check = str(input("Are you sure you want to delete this movie (Y or N): "))
        while check not in ['Y', 'N']:
            check = str(input("Are you sure you want to delete this movie (Y or N): "))
        if check == 'Y':
            update_output = cursor.callfunc('delete_movie', str, [deleteID])
            return update_output
        else:
            no_movie = "No movie was deleted!"
            return no_movie

    def searchUpdateMember(self):
        updateID = searchMember()

        update_check = 'None'
        while update_check == 'None':
            updateColumn = str(input("Which column would you like to update: "))
            updateValue = str(input("What is the updated value: "))
            update_check = cursor.callfunc('update_member', str, [updateID, updateColumn, updateValue])
            if update_check == 'None':
                print("There was an error with the input. Try again!")
        return update_check

    def searchDeleteMember(self):
        deleteID = searchMember()

        check_member = str(input("Are you sure you want to delete this member (Y or N): "))
        while check_member not in ['Y', 'N']:
            check_member = str(input("Are you sure you want to delete this member (Y or N): "))
        if check_member == 'Y':
            delete_output = cursor.callfunc('delete_member', str, [deleteID])
            return delete_output
        else:
            no_movie = "No member was deleted!"
            return no_movie


# Class to hold all functions for member
class MemberApp:
    def __init__(self):
        self.memberResponse = memberMenu()

    def rentMovie(self):
        searchID = None
        while searchID is None:
            identifier = str(input("What is the title of the movie you want to rent: "))
            for row in cursor.execute("SELECT movie_id FROM mm_movie WHERE movie_title = :mybv", mybv=identifier):
                for item in row:
                    searchID = item
        paymentOptions = ['Account', 'Credit Card', 'Check', 'Cash', 'Debit Card']
        paymentMethod = str(input("How would you like to pay for the movie: "))
        while paymentMethod not in paymentOptions:
            paymentMethod = input("How would you like to pay for the movie: ")
        memberConfirm = input("Please confirm your member username to rent movie: ")
        while memberConfirm not in memberUsername:
            memberConfirm = input("Please confirm your member username to rent movie: ")
        memberConfirm = int(memberConfirm)

        rental_output = cursor.callfunc('rent_movie', str, [identifier, paymentMethod, memberConfirm])
        return rental_output

    def returnMovie(self):
        searchID = None
        while searchID is None:
            identifier = str(input("What is the title of the movie you want to return: "))
            for row in cursor.execute("SELECT movie_id FROM mm_movie WHERE movie_title = :mybv", mybv=identifier):
                for item in row:
                    searchID = item
        memberConfirm = input("Please confirm your member username to return movie: ")
        while memberConfirm not in memberUsername:
            memberConfirm = input("Please confirm your member username to return movie: ")
        memberConfirm = int(memberConfirm)

        return_output = cursor.callfunc('return_movie', str, [identifier, memberConfirm])
        return return_output

# Heart of program
def main():
    menuResonse = menu()
    if menuResonse == '1':
        continueBooleanFirst = True
        while continueBooleanFirst:
            app = AdminApp()
            if app.adminResponse == '1':
                outcome = app.addMovie()
                print(outcome)
            elif app.adminResponse == '2':
                outcome = app.addMember()
                print(outcome)
            elif app.adminResponse == '3':
                update_outcome = app.searchUpdateMovie()
                print(update_outcome)
            elif app.adminResponse == '4':
                delete_outcome = app.searchDeleteMovie()
                print(delete_outcome)
            elif app.adminResponse == '5':
                updateMember_outcome = app.searchUpdateMember()
                print(updateMember_outcome)
            elif app.adminResponse == '6':
                deleteMember_outcome = app.searchDeleteMember()
                print(deleteMember_outcome)
            continueAdmin = str(input("Would you like to do another task (Y or N): "))
            while continueAdmin not in ['Y', 'N']:
                continueAdmin = str(input("I am not sure what you mean. Please answer Y or N: "))
            if continueAdmin == 'N':
                continueBooleanFirst = False
                print("You have signed out! Have a nice day!!")

    elif menuResonse == '2':
        continueBooleanSecond = True
        while continueBooleanSecond:
            app = MemberApp()
            if app.memberResponse == '1':
                searchMovie()
            elif app.memberResponse == '2':
                rent_movie_outcome = app.rentMovie()
                print(rent_movie_outcome)
            elif app.memberResponse == '3':
                return_movie_outcome = app.returnMovie()
                print(return_movie_outcome)
            continueMember = str(input("Would you like to do another task (Y or N): "))
            while continueMember not in ['Y', 'N']:
                continueMember = str(input("I am not sure what you mean. Please answer Y or N: "))
            if continueMember == 'N':
                continueBooleanSecond = False
                print("You have signed out! Have a nice day!!")