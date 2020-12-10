# imports
import csv
from pathlib import Path
import os

def create_csv_totaldata(filenamesArray):
    # Opening the dynamically created path to the CSV to append
    for name in filenamesArray:
        print("Opening " + name + " and appending the CSV")
        with open(Path(name), 'r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                with open(Path(r'.\TotalDataSet.csv'), 'a', newline='', encoding='utf-8') as csvfiletotal:
                    filewriter = csv.writer(csvfiletotal, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow(row)
        print("Finished appending " + name)
    print("Successfully appended the datasets")
    
def count_csv_concatenatefiles(path):
    filenamesArray = []
    # This command will also walk through all subfolders. So make sure you don't create subfolders or change the script
    for row in os.walk(path): 
        try:
            for filename in row[2]:
                # If you want to change the name of the CSV files to append, you can change the search params
                if filename.find("DataOutputFileInformation") == 0: 
                    filenamesArray.append(filename)
        except:
            print("Error in finding the documents")
    return filenamesArray

def main():
    path = r'.'
    filenamesArray = count_csv_concatenatefiles(path)
    print(filenamesArray)
    create_csv_totaldata(filenamesArray)


if __name__ == "__main__":
    main()