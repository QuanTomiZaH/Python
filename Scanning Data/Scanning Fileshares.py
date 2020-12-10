# Imports
import os
import pandas as pd
import datetime
import csv
from pathlib import Path
from hurry.filesize import size

# For this script to run, you will need to install python3(latest)
# Then run the following commands:
# pip install pandas
# pip install pathlib
# pip install hurry.filesize
# pip install datetime

# Recursively run through all folders in the given path
def collect_fileinfo(path, FileAmountCounter):
    filesurvey = []

    for row in os.walk(path): 
        LocalFileScanning = 0
        for filename in row[2]:
            try:
                full_path: Path = Path(row[0]) / Path(filename)
            except:
                full_path: Path = Path(row[0]) / Path(filename)
            
            try:
                WindowsFilename, file_extension = os.path.splitext(full_path)
            except:
                WindowsFilename = "Filename not found"
                file_extension = "Extenstion not found"
            
            try:
                LastModifiedReadable = datetime.datetime.fromtimestamp(full_path.stat().st_mtime)
            except:
                LastModifiedReadable = "Timestamp for last modified not accessible"
            
            try:
                LastAccessReadable = datetime.datetime.fromtimestamp(full_path.stat().st_atime)
            except:
                LastAccessReadable = "Timestamp for last accessed not available"
            
            try:
                RawFileSize = full_path.stat().st_size
            except:
                RawFileSize = "Rawfilesize not acessible"
            
            try:
                ReadableBytes = size(RawFileSize)
            except:
                ReadableBytes = "Cannot convert to readable bytes"
            
            try:
                filesurvey.append([full_path, path, WindowsFilename, filename, file_extension, ReadableBytes, RawFileSize, LastModifiedReadable, LastAccessReadable])
            except:
                print("error appending the Row to the dataframe")
            
            FileAmountCounter +=1
            LocalFileScanning += 1
    
    return filesurvey, FileAmountCounter, LocalFileScanning


# A function to add a list to a new dataframe and to transpose the data; after that add the data
def append_dataframe(DataList, TotalDF):
    LocalDF = pd.DataFrame(DataList)
    TotalDF = TotalDF.append(LocalDF, ignore_index=True)

    return TotalDF


# Create the dataframe
def create_totaldf():
    print("Creating the DataFrame")
    Dataframecreate = pd.DataFrame()
    return Dataframecreate


# A function to gain all the necessary paths
def define_scanningpaths():
    #This path should still be looked up dynamically
    print('Opening the CSV file containing the locations to scan')
    with open(Path(r'.\Scanlocation.csv'), mode='r') as csv_file: # Path needs to be edited for the specific location to run
        ListPaths = []
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            p: Path = Path(row[0])
            ListPaths.append(p)
    print('Scanning these locations:')
    print(ListPaths)
    return ListPaths


def iterate_FileSources(item, FileAmountCounter, TotalDF):
    # Get the data and append this to the Dataframe
    print("Scanning location: " + str(item))
    data, FileAmountCounter, LocalFileScanning = collect_fileinfo(item, FileAmountCounter)
    TotalDF = append_dataframe(data, TotalDF)
    print("Scanned " + str(LocalFileScanning) + " files in " + str(item))
    print("Scanned " + str(FileAmountCounter) + " files total for dataset: " + str(item))
    return TotalDF, FileAmountCounter


def create_csv(Document, Counter):
    Name = r'.\DataOutputFileInformation' + str(Counter) + '.csv'
    print(Name)
    Document.to_csv(Name, encoding='utf-8') # Path to drop the CSV has to be dynamically added
    print('Created a CSV file number ' + str(Counter))


def main():
    sources = define_scanningpaths()        # Defining the paths to scan
    Counter = 5
    for item in sources:
        TotalDF = create_totaldf()              # Creating the DataFrame
        FileAmountCounter = 0                   # Initiate the counter to track the amount of files scanned
        TotalDF, FileAmountCounter = iterate_FileSources(item, FileAmountCounter, TotalDF)       # Start scanning files
        print('Total amount of files scanned: ' + str(FileAmountCounter))
        create_csv(TotalDF, Counter)                     # Create a CSV output for use
        Counter += 1

if __name__ == "__main__":
    main()