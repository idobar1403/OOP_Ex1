


import json
import numpy as np
import pandas as pd

def readfiles(s1, s2):
    with open (s1) as f:
        building=json.load(f)
    for e in building['_elevators']:
        print(e)
    print(building)
    calls=pd.read_csv(s2)

    print(calls.head())
    print("\n")
    print("\n")
    output=pd.read_csv(s2)
    print(output.head())
   # for x in output:
   #     output['0.1']=1;
   # print(output.head())


readfiles("C:/Users/nechd\Desktop\OOP_2021-main\Assignments\Ex1\data\Ex1_input\Ex1_Buildings\B1.json",
          "C:/Users/nechd\Desktop\OOP_2021-main\Assignments\Ex1\data\Ex1_input\Ex1_Calls\Calls_a.csv")



