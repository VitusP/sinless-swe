import os
import sys
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from src.dataStructure import Sample


returnedSample = Sample.read(sys.argv[1])
# for row in returnedSample.rows:
#     print(row)

for col in returnedSample.cols:
    print(col.name)
