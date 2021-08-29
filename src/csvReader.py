"""
This is a python script to data mine a csv file and 
return list of list of data points. This is a part of
HW1 and HW2
"""

import sys
import re

def csv_reader(fileName):    
    #: Function to get list of list representation of a csv file (HW1)
    #: param: file name or path
    #: return: list of list data points
    try:
        with open(fileName, newline='') as f:
            columnLength = 0
            listofRows = []
            dataTypeMap = []
            for row in f:
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
                    print("Data Type Map: ", dataTypeMap)
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
                                # print(e)
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
    except Exception:
        print("Failed to read csv")
    else:
        for row in listofRows:
            print(row)
        print("Length of data", len(listofRows))
        return listofRows

# csv_reader(sys.argv[1])