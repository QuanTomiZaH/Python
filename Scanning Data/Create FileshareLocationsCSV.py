# imports
import csv
from pathlib import Path
import pandas as pd

# A function to gain all the necessary paths
def scan_users(UserList, FileLocation):

    #This path should still be looked up dynamically
    print('Opening the CSV file containing the users to scan')
    with open(Path(r'.\GroupFilteringCSV.csv'), mode='r') as csv_file:
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
    with open(r'..\Sort Filepaths\CreatedFilterscriptPaths.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for item in FilePathArray:
            filewriter.writerow(item)
    print('Created the file "CreatedFilterscriptPaths.csv"')

# The below function should replacethe (create_csv_groups)
def create_csv_groups(FileGroupArray):
    with open(r'..\Extra Output\CreatedFilterscriptGroupRights.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for item in FileGroupArray:
            filewriter.writerow(item)
    print('Created the file "CreatedFilterscriptGroupRights.csv"')

def check_doubles(UserList, UserSmallList, FileLocation):
    GroupFileRightsBig = []
    Totalamount= len(UserList)
    counter = 0
    while Totalamount >= counter:
        for item in UserSmallList:
            try:
                if UserList[counter] == item:
                    GroupFileRightsBig.append([FileLocation[counter], UserList[counter]])
            except:
                continue
        counter += 1
    return GroupFileRightsBig


def deliver_filepaths():
    GroupFileRightsSmall = []
    PathToList = []
    with open(Path(r'.\Fileshare Filtered Gfile Rechten.csv'), mode='r') as csv_file:
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
    with open(Path(r'.\Kolham Alle OT applicaties met bijbehorende Users en Laptops.csv'), mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            try:
                row = row[1].lower()
                UserSmallList.append(row)
            except:
                continue
    return UserSmallList


def main():
    # Disclaimer: This entire script is very ugly and work in progress.

    # All records
    UserList = []
    FileLocation = []

    # Specific unique records
    UserSmallList = []

    #lists for the CSV
    # Fill the UserSmallList and other info with the unique target group names
    UserSmallList = fill_UserSmallList(UserSmallList)

    # parse all the data into arrays to scan
    UserList, FileLocation = scan_users(UserList, FileLocation)
    GroupFileRightsBig = check_doubles(UserList, UserSmallList, FileLocation)

    # Create arrays containing the GFile rights
    PathToList, GroupFileRightsSmall = deliver_filepaths()
    FilteredFilePaths = crosscheck_fileshares(PathToList, GroupFileRightsSmall, GroupFileRightsBig)

    create_csv_groups(GroupFileRightsBig)
    create_csv_paths(FilteredFilePaths)

if __name__ == "__main__":
    main()