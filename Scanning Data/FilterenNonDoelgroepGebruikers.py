# imports
import csv
from pathlib import Path
import pandas as pd
import re

def format_paths():
    FilePaths = []
    #This path should still be looked up dynamically
    print('Opening the CSV file containing the users to scan')
    with open(Path(r'.\CreatedFilterscriptPathsGeenDoelgroep.csv'), mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            try:
                tempvariable = row[0]
                TypeRights = ""
                if "-LeesRechten" in tempvariable:
                    tempvariable = re.sub("-LeesRechten", "", tempvariable)
                    TypeRights = "Leesrechten"
                elif "-MuteerRechten" in tempvariable:
                    tempvariable = re.sub("-MuteerRechten", "", tempvariable)
                    TypeRights = "MuteerRechten"
                elif "-Eigenaar" in tempvariable:
                    tempvariable = re.sub("-Eigenaar", "", tempvariable)
                    TypeRights = "Eigenaar"
                FilePaths.append(tempvariable)
                FilePaths.append(TypeRights)
            except:
                continue
            # To create a new file with the correct filepaths to use in PowerBI
            with open(Path(r'.\PowerBiUsersAndPathsNonDoelgroep.csv'), mode='a', encoding='utf-8', newline='') as csv_BI:
                try:
                    row.append(tempvariable)
                    row.append(TypeRights)
                    filewriter = csv.writer(csv_BI, delimiter=',')
                    filewriter.writerow(row)
                except:
                    continue
        print("Created the 'PowerBiUsersAndPaths.csv' in the folder 'Sort Filepaths'")
    return FilePaths

def sort_uniquepaths(FilePaths, FilepathsSorted):
    for item in FilePaths:
        if item not in FilepathsSorted:
            FilepathsSorted.append(item)
    return FilepathsSorted

#def create_csv(Filepathchecker):
#    # This should reference to a location in Scanning script and then that python script should look for this document
#    with open(r'\FilePathsSortedNonDoelgroepGebruikers.csv', 'w', newline='') as csvfile:
#        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#        for item in Filepathchecker:
#            filewriter.writerow([item])
#    print("Created the file 'FilePathsSorted.csv' in the folder 'Sort Filepaths'")

def main():
    # Creating the document containing all the fileshare paths, neatly ordened
    Filepathchecker = []
    FilePaths = format_paths()
    Filepathchecker = sort_uniquepaths(FilePaths, Filepathchecker)
    #create_csv(Filepathchecker)  

if __name__ == "__main__":
    main()