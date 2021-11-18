import copy
import json
import sys
from json import JSONEncoder
import os
import pandas as pd
import math



class Elevator:
    def __init__(self, Elevator):
        self.id = Elevator['_id']
        self.speed = Elevator['_speed']
        self.minFloor = Elevator['_minFloor']
        self.maxFloor = Elevator['_maxFloor']
        self.closeTime = Elevator['_closeTime']
        self.openTime = Elevator['_openTime']
        self.startTime = Elevator['_startTime']
        self.stopTime = Elevator['_stopTime']
        self.callList = []

    def whereAtTime(self, time):
        if len(self.callList) > 0:
            if 0 <= time <= (self.callList[0].runTime + self.startTime + self.closeTime):
                return 0
            for i in range(1, len(self.callList)):
                previous_call = self.callList[i-1]
                current_call = self.callList[i]
                timeDif = time - (previous_call.runTime + self.startTime + self.closeTime)

                if previous_call.runTime <= time < current_call.runTime:
                    if previous_call.findTime(current_call, self) < current_call.runTime:
                        return previous_call.floor
                    if time > (previous_call.runTime + self.startTime + self.closeTime):
                        floor_difference = math.ceil(timeDif * self.speed)
                        if previous_call.floor < current_call.floor:
                            curr = previous_call.floor + floor_difference
                        else:
                            curr = previous_call.floor - floor_difference
                        return curr
                    else:
                        return previous_call.floor
            return self.callList[-1].floor


class Building:
    def __init__(self, building):
        self.minFloor = building['_minFloor']
        self.maxFloor = building['_maxFloor']
        self.ElevList = []


class Triplet:
    def __init__(self, floor, minTime, runTime):
        self.floor = floor
        self.minTime = minTime
        self.runTime = runTime

    def findTime(self, dest, x):
        # finds what the run time of the triplet should be
        dist = abs(self.floor - dest.floor)
        if dist == 0:
            return self.runTime
        constTime = x.closeTime + x.openTime + x.startTime + x.stopTime
        speedTime = dist / x.speed
        time = constTime + speedTime + self.runTime
        return time

    def changeTime(self, p2, x):
        # changes the runTime of the triplet
        sum = 0
        time = self.findTime(p2, x)
        if p2.runTime < time:
            sum += time - p2.minTime
            p2.runTime = time
        return sum

    def clone(self):
        return Triplet(self.floor, self.minTime, self.runTime)

def findElev(elevators, src, dest):
    if len(elevators) == 1:
        return elevators[0].id
    min = sys.maxsize
    index = 0
    count = 0
    for x in elevators:
        temp = []
        src1 = copy.copy(src)
        dest1 = copy.copy(dest)
        if len(x.callList) == 0:
            x.callList.append(Triplet(0, 0, 0))
        for i in range(len(x.callList)):
            temp.append(x.callList[i].clone())
        src1.runTime = src1.minTime
        t = src1.findTime(dest1, x)
        dest1.minTime = t
        dest1.runTime = t
        i = 0
        for y in range(1, len(temp)):
            previous_triplet = temp[y-1]
            current_triplet = temp[y]
            time = previous_triplet.findTime(src1, x)
            if time > src1.runTime:
                if (src1.floor >= previous_triplet.floor and src1.floor <= current_triplet.floor) or (
                        src1.floor >= current_triplet.floor and src1.floor <= previous_triplet.floor):
                    temp.insert(y, src1)
                    i = y
                    break
        if i > 0:
            j = 0
            for z in range(i + 1, len(temp)):
                previous_triplet = temp[z-1]
                current_triplet = temp[z]
                time = previous_triplet.findTime(dest1, x)
                if (time > dest1.runTime):
                    if ((dest1.floor >= previous_triplet.floor and dest1.floor <= current_triplet.floor) or (
                            dest1.floor >= current_triplet.floor and dest1.floor <= previous_triplet.floor)):
                        temp.insert(z, dest1)
                        j = z
                        break
            if j == 0:
                temp.append(dest1)
        else:
            temp.append(src1)
            temp.append(dest1)
        temp[0].runTime = temp[1].minTime + x.closeTime + x.startTime
        sum = 0
        for y in range(1, len(temp)):
            sum = sum + temp[y - 1].changeTime(temp[y], x)
        if sum < min:
            index = x.id
            place = count
            min = sum
            temp1 = copy.copy(temp)
        count += 1
    elevators[place].callList = temp1
    return index


def readfiles(s1, s2, s3):
    try:
        with open(s1) as f:
            building = json.load(f)
            mybuilding = Building(building)
    except:
        print("Not json file!!")

    count = 0
    for e in building['_elevators']:
        count_e = Elevator(e)
        mybuilding.ElevList.append(count_e)
        count = count + 1
    try:
        calls = pd.read_csv(s2, header=None)
        output = pd.read_csv(s3, header=None)
    except:
        print("Not csv file")

    for x in calls.itertuples():
        source = Triplet(x[3], x[2], x[2])
        dest = Triplet(x[4], 0, 0)
        output.loc[x[0], 5] = findElev(mybuilding.ElevList, source, dest)
        calls.loc[x[0], 5] = output.loc[x[0], 5]
    for y in mybuilding.ElevList:
        print(y.id, " AT ", y.whereAtTime(55))
    output.to_csv(os.path.join(os.getcwd(), 'out_b.csv'), index=False, header=False)
    # df=pd.DataFrame(output)
    # df.set_axis(['Name','Time','Src','Dst','Status','Elev'], axis='columns', inplace=True)
    # print(df['Elev'])
    # import plotly.express as px
    # fig=px.scatter(df, x="Elev", y="Src", animation_frame="Time", animation_group="Elev", hover_name="Elev",
    #            log_x=True, size_max=55, range_x=[1, 100], range_y=[0, 100])
    # fig.show()


if __name__ == '__main__':
    #readfiles('B5.json', 'Calls_b.csv', 'Calls_b.csv')
    readfiles(sys.argv[1],sys.argv[2],sys.argv[3])
