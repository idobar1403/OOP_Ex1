import copy
import json
import sys
from json import JSONEncoder
import os
import pandas as pd
import math


class Elevator:
    # the constructor for the elevator
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
    # this function returns the current floor of the elevator at any given time
    def whereAtTime(self, time):
        close_start = self.startTime + self.closeTime;
        stop_open = self.stopTime + self.openTime;
        listlen = len(self.callList)
        if (listlen == 0):
            return 0
        if (time < self.callList[0].runTime):  # the time is smaller than the run time of the first call
            return 0;
        elif (self.callList[listlen - 1].runTime < time):  # the time is after the last call
            return self.callList[listlen - 1].floor
        else:  # the rime is in between calls
            for i in range(1, listlen):
                if (time >= self.callList[i - 1].runTime and time <= self.callList[i].runTime):
                    if (time - close_start <= self.callList[i - 1].runTime):
                        return self.callList[i - 1].floor
                    if (time + stop_open >= self.callList[i].runTime):
                        return self.callList[i].floor
                    else:
                        time1 = time - self.callList[
                            i - 1].runTime - close_start  # time1 is the amount of time from the closest floor to the time we were given
                        if (self.callList[i - 1].floor < self.callList[i].floor):  # going up
                            Floor = int(math.ceil(self.callList[i - 1].floor + time1 * self.speed))
                            if (Floor > self.callList[i].floor):
                                Floor = self.callList[i].floor
                            return Floor
                        else:
                            # going down
                            Floor = int(math.ceil(self.callList[i - 1].floor - time1 * self.speed))
                            if (Floor < self.callList[i].floor):
                                Floor = self.callList[i].floor
                            return Floor


class Building:
    # constructor fot building
    def __init__(self, building):
        self.minFloor = building['_minFloor']
        self.maxFloor = building['_maxFloor']
        self.ElevList = []


class Triplet:
    # constructor for triplet that holds the floor, the original arriving time and the real arriving time
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
        # changes the runTime of the triplet and return the difference between the times
        sum = 0
        time = self.findTime(p2, x)
        if p2.runTime < time:
            sum += time - p2.minTime
            p2.runTime = time
        return sum

    def clone(self):
        # get new object with the same values
        return Triplet(self.floor, self.minTime, self.runTime)

# the function returns the best elevator for the given call
def findElev(elevators, src, dest):
    # if there is only one elevator it will give all the calls the same elevator
    if len(elevators) == 1:
        return elevators[0].id
    min = sys.maxsize
    index = 0
    count = 0
    for x in elevators:
        temp = []
        src1 = copy.copy(src)
        dest1 = copy.copy(dest)
        # the elevators starts at floor 0
        if len(x.callList) == 0:
            x.callList.append(Triplet(0, 0, 0))
        # creating new list with the same objects as the original
        for i in range(len(x.callList)):
            temp.append(x.callList[i].clone())
        src1.runTime = src1.minTime
        t = src1.findTime(dest1, x)
        dest1.minTime = t
        dest1.runTime = t
        i = 0
        # checking where the source will be in the array
        for y in range(1, len(temp)):
            previous_triplet = temp[y - 1]
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
            # if the source is in the array we will check the destination place
            for z in range(i + 1, len(temp)):
                previous_triplet = temp[z - 1]
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
            # if the source place is at the end we will add the source and the destination at the end
            temp.append(src1)
            temp.append(dest1)
        temp[0].runTime = temp[1].minTime + x.closeTime + x.startTime
        sum = 0
        # sum all the changes in time that the source and the destination adds
        for y in range(1, len(temp)):
            sum = sum + temp[y - 1].changeTime(temp[y], x)
        # check for the min time difference
        if sum < min:
            index = x.id
            place = count
            min = sum
            temp1 = copy.copy(temp)
        count += 1
    elevators[place].callList = temp1
    return index


def readfiles(s1, s2, s3):
    # try to open the json file
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
    # try to open the calls file
    try:
        calls = pd.read_csv(s2, header=None)
        output = pd.read_csv(s2, header=None)
    except:
        print("Not csv file")
    # running over all of the calls and find best elevator for each call
    for x in calls.itertuples():
        source = Triplet(x[3], x[2], x[2])
        dest = Triplet(x[4], 0, 0)
        output.loc[x[0], 5] = findElev(mybuilding.ElevList, source, dest)
        calls.loc[x[0], 5] = output.loc[x[0], 5]
    output.to_csv(r'' + s3, header=False, index=False)


if __name__ == '__main__':
    # reading files from user
    readfiles(sys.argv[1], sys.argv[2], sys.argv[3])
