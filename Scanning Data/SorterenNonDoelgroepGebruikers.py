# imports
import csv
from pathlib import Path
import pandas as pd

# A function to gain all the necessary paths
def scan_users(UserList, FileLocation):

    #This path should still be looked up dynamically
    print('Opening the CSV file containing the users to scan')
    with open(Path(r'..\Find FileshareLocations script\GroupFilteringCSV.csv'), mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            try:
                user = row[0].lower()
                UserList.append(user)
                FileLocation.append(row[1])
            except:
                continue
    return UserList, FileLocation


# The below function should replacethe (create_csv_paths)
def create_csv_paths(FilePathArray):
    with open(r'.\CreatedFilterscriptPaths.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for item in FilePathArray:
            filewriter.writerow(item)
    print('Created the file "CreatedFilterscriptPaths.csv"')


# The below function should replacethe (create_csv_groups)
def create_csv_groups(FileGroupArray):
    with open(r'.\CreatedFilterscriptGroupRightsGeenDoelgroep.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for item in FileGroupArray:
            filewriter.writerow(item)
    print('Created the file "CreatedFilterscriptGroupRightsGeenDoelgroep.csv"')


# Vul de lijst met groepen van de doelgroep(of niet de doelgroep)
def check_doubles(UserList, UserSmallList, FileLocation):
    GroupFileRightsBig = []
    Totalamount= len(UserList)
    counter = 0
    while Totalamount >= counter:
        try:
            CompareIncludeList = [FileLocation[counter], UserList[counter]]
            if CompareIncludeList[1] not in UserSmallList:
                GroupFileRightsBig.append(CompareIncludeList)
        except:
            print("Completed")
        counter += 1
    print(str(len(GroupFileRightsBig)) + " amount of rights in this array")
    return GroupFileRightsBig


# Zoek alle filepaden op bij desbetreffende G-File rechten
def deliver_filepaths():
    GroupFileRightsSmall = []
    PathToList = []
    with open(Path(r'..\Find FileshareLocations script\Fileshare Filtered Gfile Rechten.csv'), mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            try:
                GroupFileRightsSmall.append(row[0])
                PathToList.append(row[1])
            except:
                continue
    return PathToList, GroupFileRightsSmall


def crosscheck_fileshares(PathToList, GroupFileRightsSmall, GroupFileRightsBig):
    # Hier moeten de filegroepen met elkaar worden vergeleken, en dan moet er een lijst met Filepaden worden gecreëerd die vervolgens in een CSV komen
    FilteredFilePaths = []
    #find all the filepaths and create an array including the unique paths
    for item in GroupFileRightsBig:
        i = 0 
        for group in GroupFileRightsSmall:
            try:
                if item[0] == group:
                    item = item[1].lower()
                    FilteredFilePaths.append([PathToList[i], item])
            except:
                continue
            i += 1

    return FilteredFilePaths


# Fill all the unique info about the users
def fill_UserSmallList(UserSmallList):
    # If I change the Users in this CSV File, I will get the paths that are only used by those specific groups. This can be easily used for the Pilot
    with open(Path(r'..\Find FileshareLocations script\Alle OT applicaties met bijbehorende Users en Laptops.csv'), mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            try:
                row = row[1].lower()
                UserSmallList.append(row)
            except:
                continue
    return UserSmallList


def main():
    # Disclaimer: This entire script is work in progress.

    # All records
    UserList = []
    FileLocation = []

    # Specific unique records
    UserSmallList = []

    #lists for the CSV
    # Fill the UserSmallList and other info with the unique target group names
    print("Adding data to arrays")
    UserSmallList = fill_UserSmallList(UserSmallList)

    # parse all the data into arrays to scan
    UserList, FileLocation = scan_users(UserList, FileLocation)
    GroupFileRightsBig = check_doubles(UserList, UserSmallList, FileLocation)

    # Create arrays containing the GFile rights
    print("Creating Arrays with GFile rights")
    PathToList, GroupFileRightsSmall = deliver_filepaths()
    FilteredFilePaths = crosscheck_fileshares(PathToList, GroupFileRightsSmall, GroupFileRightsBig)

    # Create the CSV files
    print("Creating CSV files")
    create_csv_groups(GroupFileRightsBig)
    create_csv_paths(FilteredFilePaths)

if __name__ == "__main__":
    main()