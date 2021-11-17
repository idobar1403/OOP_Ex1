import copy
import json
import sys
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

    def whereAtTime(self, time):
        close_start=self.startTime+self.closeTime;
        stop_open=self.stopTime+self.openTime;
        listlen=len(self.callList)
        count=0
        if (len(self.callList) == 0):
            return 0;
        elif (time<self.callList[0].runTime): # the time is smaller than the run time of the first call
            if (self.callList[0].floor >0): #going up
               Floor=int(math.ceil(time*self.speed))
               if (Floor>self.callList[0].floor):
                   return self.callList[0].floor
               else:
                   return Floor
            elif(self.callList[0].floor <0): #going down
                Floor= int(math.ceil(time*self.speed))*-1
                if(Floor<self.callList[0].floor):
                    return self.callList[0].floor
                else:
                    return Floor
            else: # staying on 0
                return 0;
        elif (self.callList[listlen-1].runTime<time): # the time is after the last call
            return self.callList[listlen-1].floor
        else: # the rime is in between calls
            for i in range(1, listlen):
                if (time >= self.callList[i - 1].runTime and time <= self.callList[i].runTime):
                    if (time-close_start<=self.callList[i - 1].runTime):
                        return self.callList[i - 1].floor
                    if(time+stop_open >=self.callList[i].runTime):
                        return self.callList[i].floor
                    else:
                        time1=time-self.callList[i - 1].runTime - close_start # time1 is the amount of time from the closest floor to the time we were given
                        if (self.callList[i - 1].floor < self.callList[i].floor): # going up
                            Floor=int (math.ceil(self.callList[i - 1].floor+time1*self.speed))
                            return Floor
                        else:
                            #going down
                            Floor=int (math.ceil(self.callList[i - 1].floor-time1*self.speed))
                            return Floor


class Building:
    def __init__(self, building):
        self.minFloor=building['_minFloor']
        self.maxFloor=building['_maxFloor']
        self.ElevList=[]

class Triplet:
    def __init__(self, floor, minTime, runTime):
        self.floor=floor
        self.minTime=minTime
        self.runTime=runTime

    def findTime(self,dest,x):
        # finds what the run time of the triplet should be
        dist=abs(self.floor-dest.floor)
        if (dist==0):
            return 0
        constTime=x.closeTime+x.openTime+x.startTime+x.stopTime
        speedTime=dist/x.speed
        time=constTime+speedTime+self.runTime
        return time

    def changeTime(self,p2,x):
        # changes the runTime of the triplet
        sum=0
        time=self.findTime(p2,x)
        if (p2.runTime<time):
            sum+=time-p2.runTime
            p2.runTime=time
        return sum

    def copy(self):
        return type(self)(self.floor,self.minTime,self.runTime)



def findElev(ElevList,src,dest):
    if(len(ElevList)==1):
        return ElevList[0].id
    min=sys.maxsize
    index=0
    count=0
    for x in ElevList:
        src1=src.copy()
        dest1=dest.copy()
        if (len(x.callList)==0):
            x.callList.append(Triplet(0,0,0))
        src1.runTime=src1.minTime
        temp=copy.deepcopy(x.callList)
        t=src1.findTime(dest, x)
        #sum=t-src1.runTime
        dest1.minTime=t
        dest1.runTime=t
        i=0
        for y in range(1,len(temp)):
            time= temp[y-1].findTime(src1,x)
            if (time>src1.runTime):
                if((src1.floor>=temp[y-1].floor and src1.floor<=temp[y].floor)or(src1.floor>=temp[y].floor and src1.floor<=temp[y-1].floor)):
                    temp.insert(y,src1)
                    i=y
                    break
        if(i>0):
            j=0
            for z in range(i+1,len(temp)):
                time=temp[z-1].findTime(dest1,x)
                if(time>dest1.runTime):
                    if((dest1.floor>=temp[z-1].floor and dest1.floor<=temp[z].floor)or(dest1.floor>=temp[z].floor and dest1.floor<=temp[z-1].floor)):
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
        sum=0
        for y in range(1,len(temp)):
            sum=sum+temp[y-1].changeTime(temp[y],x)
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
            mybuilding = Building(building)
    except:
        print("Not json file!!")

    count=0
    for e in building['_elevators']:
        count_e=Elevator(e)
        mybuilding.ElevList.append(count_e)
        count=count+1

    try:
        calls = pd.read_csv(s2,header=None)
        output = pd.read_csv(s2,header=None)
    except:
        print("Not csv file")


    for x in calls.itertuples():
        source=Triplet(x[3],x[2],x[2])
        dest= Triplet(x[4], 0.0, 0.0)
        output.loc[x[0],5]=findElev(mybuilding.ElevList, source,dest)

    output.to_csv(r''+s3+'.csv', header=False, index=False)




if __name__ == '__main__':
     readfiles("B2.json","Calls_a.csv","out")





    #with open(sys.argv[0], 'r') as f:
     #   build = f.read()
    #with open(sys.argv[1], 'r') as f:
      #  calls = f.read()
    #with open(sys.argv[2], 'r') as f:
     #   out = f.read()
    #readfiles(sys.argv[1],sys.argv[2],sys.argv[3])
