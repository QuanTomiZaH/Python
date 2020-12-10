# imports
import csv
from pathlib import Path

def format_Users(UsernameArray):
    FilteredUserInfo = []
    NotFilteredUserInfo = []
    NewUsers = []
    temparray = []
    #This path should still be looked up dynamically
    print('Opening the CSV file containing the old user document to scan and process')
    with open(Path(r'.\Alle OT gebruiker te vernieuwen.csv'), mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        
        for row in csv_reader: 
            temparray.append(row[0])
            try:
                if row[0] in UsernameArray:
                    FilteredUserInfo.append(row)
                elif row[0] not in UsernameArray:
                    NotFilteredUserInfo.append(row)
            except:
                continue

        for item in UsernameArray:
            if item not in temparray:
                NewUsers.append([item])

    return FilteredUserInfo, NotFilteredUserInfo, NewUsers

def get_NewUsernames():
    UsernameArray = []
    #This path should still be looked up dynamically
    print('Opening the CSV file containing the new users to scan')
    with open(Path(r'.\Laatste gegevens OT-Users met LT-nr.csv'), mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            try:
                UsernameArray.append(row[1])
            except:
                continue
    return UsernameArray

def create_csv(FilteredUserInfo):
    # This should reference to a location in Scanning script and then that python script should look for this document
    with open(r'.\TotalUsersSorted.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for item in FilteredUserInfo:
            filewriter.writerow(item)

def create_csv_not_users(FilteredUserInfo):
    # This should reference to a location in Scanning script and then that python script should look for this document
    with open(r'.\NotUsersAnymoreSorted.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for item in FilteredUserInfo:
            filewriter.writerow(item)

def create_csv_newusers(NewUsers):
    # This should reference to a location in Scanning script and then that python script should look for this document
    with open(r'.\NewUsers.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for item in NewUsers:
            filewriter.writerow(item)

def main():
    # Creating the document containing all the fileshare paths, neatly ordened
    UsernameArray = get_NewUsernames()
    FilteredUserInfo, NotFilteredUserInfo, NewUsers = format_Users(UsernameArray)
    create_csv(FilteredUserInfo)
    create_csv_not_users(NotFilteredUserInfo)
    create_csv_newusers(NewUsers)

if __name__ == "__main__":
    main()