import json
import sys

import numpy as np
import pandas as pd
import math

class Elevator:
    def __init__(self, Elevator):
        self.id=Elevator['_id']
        self.speed = Elevator['_speed']
        self.minFloor=Elevator['_minFloor']
        self.maxFloor=Elevator['_maxFloor']
        self.closeTime=Elevator['_closeTime']
        self.openTime=Elevator['_openTime']
        self.startTime=Elevator['_startTime']
        self.stopTime=Elevator['_stopTime']
        self.callList=[]

    def _str_(self):
        s1="elevator="
        s2=self.id
        s3=self.speed
        s=s1 , s2,s3
        return s


class Building:
    def __init__(self, building):
        self.minFloor=building['_minFloor']
        self.maxFloor=building['_maxFloor']
        self.ElevList=[]
    def _str_(self):
        s1="minFloor="
        s2=self.minFloor
        s3="maxFloor="
        s4=self.maxFloor
        s5="numOfElev="
        s6=self.numOfElev
        s=s1 , s2 , s3 , s4 , s5 , s6
        return s



class Pairs:
    def __init__(self, floor, minTime, runTime):
        self.floor=floor
        self.minTime=minTime
        self.runTime=runTime
    def findTime(self,dest,x):
        dist=abs(self.floor-dest.floor)
        constTime=x.closeTime+x.openTime+x.startTime+x.stopTime
        speedTime=dist/x.speed
        time=constTime+speedTime+self.runTime
        return time
    def copy(self):
        return type(self)(self.floor,self.minTime,self.runTime)
def changeTime(p1,p2,x):
    sum=0
    dist=abs(p1.floor-p2.floor)
    constTime=x.closeTime+x.openTime+x.startTime+x.stopTime
    speedTime=dist/x.speed
    time=constTime+speedTime+p1.runTime
    if (p2.runTime<time):
        sum+=time-p2.runTime
        p2.runTime=time
    return sum

def findElev(ElevList,src,dest):
    if(len(ElevList)==1):
        return ElevList[0].id
    min=sys.maxsize
    index=0
    count=0
    for x in ElevList:
        src1=src.copy()
        dest1=dest.copy()
        src1.runTime=src1.minTime
        temp=x.callList.copy()
        t=src1.findTime(dest, x)
        sum=t-src1.runTime
        dest1.minTime=t
        dest1.runTime=t
        i=0
        for y in range(1,len(temp)):
            time= temp[y-1].findTime(src1,x)
            if (time>src1.runTime):
                if((src1.floor>temp[y-1].floor and src1.floor<temp[y].floor)or(src1.floor>temp[y].floor and src1.floor<temp[y-1].floor)):
                    temp.insert(y,src1)
                    i=y
                    break
        if(i>0):
            j=0
            for z in range(i+1,len(temp)):
                time=temp[z-1].findTime(dest1,x)
                if(time>dest1.runTime):
                    if((dest1.floor>temp[z-1].floor and dest1.floor<temp[z].floor)or(dest1.floor>temp[z].floor and dest1.floor<temp[z-1].floor)):
                        temp.insert(z, dest1)
                        j = z
                        break
            if(j==0):
                temp.append(dest1)
        else:
            temp.append(src1)
            temp.append(dest1)
        if(len(temp)==0):
            temp.insert(src1)
            temp.insert(dest1)
        temp[0].runTime=temp[0].minTime+x.closeTime+x.startTime
        for y in range(1,len(temp)):
            sum=sum+changeTime(temp[y-1],temp[y],x)
        if(sum<min):
            index=x.id
            place=count
            min=sum
            temp1=temp.copy()
        count+=1
    ElevList[place].callList = temp1
    return index



def readfiles(s1, s2,s3):
    try:
        with open(s1) as f:
            building=json.load(f)
    except:
        print("Not json file!!")
    mybuilding = Building(building)
    count=0
    for e in building['_elevators']:
       count_e=Elevator(e)
       mybuilding.ElevList.append(count_e)
       count=count+1
    try:
         calls = pd.read_csv(s2,header=None)
         output = pd.read_csv(s3,header=None)
    except:
        print("Not csv file")

   # output = calls.copy()
    for x in calls.itertuples():
        source=Pairs(x[3],x[2],x[2])
        dest= Pairs(x[4], 0.0, 0.0)
        output.loc[x[0],5]=findElev(mybuilding.ElevList, source,dest)
        calls.loc[x[0],5]=output.loc[x[0],5]
    output.to_csv(r'/Users/idobar/Bsc/Year 2/OOP/Ex1/OOP_Ex1/out.log', header=False)
   # return output
if __name__ == '__main__':
    with open(sys.argv[0], 'r') as f:
        build = f.read()
    with open(sys.argv[1], 'r') as f:
        calls = f.read()
    with open(sys.argv[2], 'r') as f:
        out = f.read()
    readfiles(sys.argv[1],sys.argv[2],sys.argv[3])