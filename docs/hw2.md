## HW2: CSV Reader Report
### Usage
```Shell
$ python3 csvReader.py <.csv File Name>
```
To output the cleaned the original ```.csv``` file, uncomment line ```93``` in the ```csvReader.py```
```Python
# convert back to csv (uncomment line below)
toCsv(cleanedCsvList, "cleaned.csv")
```

**csvReader.py**

```Python
"""
This is a python script to data mine a csv file and 
return list of list of data points. This is a part of
HW1 and HW2
"""

import sys
import re
import time

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
                    # print("Data Type Map: ", dataTypeMap)
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
        # for row in listofRows:
        #     print(row)
        print("Length of data", len(listofRows))
        return listofRows
```

## POM3 Runtime Report
**csvReader.py**
```Python
# Measure runtime
startTime = time.time()
csv_reader(sys.argv[1])
totalDuration = time.time() - startTime
print("Runtime: ", totalDuration, " seconds")
```

The runtime to read and clean pom3a.csv is **0.0619 seconds**

## Invalid Rows Example
I modified row 20, 21, 50, and 51 to make it invalid
**pom3a-modified.csv**
```Shell
row 20 ,1.01842058254,5.65156386288,0.439436866794,18.7473314896,9.53839835298,3.5626617163,2.67581072348,9.9575819528,784.733261285,0.322026398189,0.180656934307
row 21
0.169520130447,jkl,6.67271822305,0.513748143098,6.33427829053,14.6624717106,0.924383271512,4.88822321482,16.5997184106,325.119138361,0.236250118956,0.416666666667
row 50 
hello,1.02854740347,6.9466240011,hello,84.8719586081,36.4442397908,3.79771348879,4.92699545345,14.265223051,1252.57339236,0.348923946602,0.260323159785
row 51
0.14980297866,1.12719673855,7.95924811772,0.6191934631,33.2633218794,2.66262205226,0.282125938775,0.379793253465,1.21176558547,348.591990624,0.02220886879,hello

```
**Output**
Here is the output of our code
```Shell
python3 csvReader.py ../../pom3a-modified.csv
Invalid data type in row:  20
Invalid data type in row:  21
Invalid data type in row:  51
Invalid data type in row:  52
Invalid column length in row:  9977
Length of data 9972
Runtime: %s seconds 0.06659603118896484
```