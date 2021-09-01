"""
This is a python script to data mine a csv file and 
return list of list of data points. This is a part of
HW1 and HW2
"""

import sys
import re
import time
import csv # only for converting list of list to .csv

def csv_reader(fileName):    
    #: Function to get list of list representation of a csv file (HW1)
    #: param: file name or path
    #: return: list of list data points
    try:
        with open(fileName, newline='') as f:
            columnLength = 0
            rowCounter = 0
            listofRows = []
            dataTypeMap = []
            for row in f:
                # Count row
                rowCounter += 1
                # Remove white spaces
                row = "".join(row.split())
                # Remove the rest of string after '#'
                row = re.sub('#.*$', '', row)
                # Split string into columns
                row = row.split(",")
                # Get the column length
                rowIsValid = True
                if len(listofRows) == 0:
                    columnLength = len(row)
                    for i in range(0, columnLength):
                        dataTypeMap.append(bool(re.match(r'.*[A-Z]', row[i])))
                    # print("Data Type Map: ", dataTypeMap)
                else:
                    # Check if row length is valid
                    if len(row) != columnLength:
                        rowIsValid = False
                        print("Invalid column length in row: ", rowCounter)
                    else:                       
                        # Convert data to its data type (number, strings, etc)
                        currentColumn = 0
                        newRow = []
                        for column in row:
                            # print("Before conversion: ", column)
                            isNumber = dataTypeMap[currentColumn]
                            # print("Is number?: ", isNumber)
                            if isNumber == True:
                                try:
                                    newRow.append(float(column))
                                except Exception as e:
                                    # Failed to convert to float
                                    print("Invalid data type in row: ", rowCounter)
                                    rowIsValid = False
                                    break
                            else:
                                newRow.append(column)
                            # print(column)
                            currentColumn += 1
                        # print("New Row: ", newRow)
                        row = newRow
                # Check if each row has correct column length
                if len(row) == columnLength and rowIsValid:
                    listofRows.append(row)
    except Exception as e:
        print("Failed to read csv: ", e)
    else:
        for row in listofRows:
            print(row)
        print("Size of data", len(listofRows), " rows")
        return listofRows

def toCsv(listofList, newFileName):
    #: Function to convert list of list to .csv
    #: param: list of list data points
    #: param: new file name
    #: return: none

    with open(newFileName, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(listofList)

# Measure runtime
startTime = time.time()
cleanedCsvList = csv_reader(sys.argv[1])
totalDuration = time.time() - startTime
print("Runtime: ", totalDuration, " seconds")

# convert back to csv (uncomment line below)
# toCsv(cleanedCsvList, "cleaned.csv")