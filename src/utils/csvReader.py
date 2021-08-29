import sys
import re
import csv


# def csv_reader(fileName):    
#     try:
#         rowList = []
#         columnsLength = 0
#         with open(fileName, newline='\n') as f:
#             reader = csv.reader(f)
#             for row in reader:
#                 # Get the first row 
#                 if len(rowList) == 0:
#                     columnsLength = len(row)
#                 # Add row to list
#                 if len(row) != columnsLength:
#                     continue
#                 rowList.append(row)
#                 print(row, " Length: ", len(row))
#     except Exception:
#         print("Failed to read csv")
#     else:
#         print("Column Length: ", columnsLength)

def csv_reader(fileName):    
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
                        print("Before conversion: ", column)
                        isNumber = dataTypeMap[currentColumn]
                        print("Is number?: ", isNumber)
                        if isNumber == True:
                            try:
                                newRow.append(float(column))
                            except Exception as e:
                                # Failed to convert to float
                                print(e)
                                rowIsValid = False
                                break
                        else:
                            newRow.append(column)
                        print(column)
                        currentColumn += 1
                    print("New Row: ", newRow)
                    row = newRow
                # Check if each row has correct column length
                if len(row) == columnLength and rowIsValid:
                    listofRows.append(row)
    except Exception:
        print("Failed to read csv")
    else:
        print("")
        return listofRows

fileName = sys.argv[1]
dataList = csv_reader(fileName)
for row in dataList:
    print(row)