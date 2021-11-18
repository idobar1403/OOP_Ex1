import unittest

from Ex1 import Building, Elevator,Triplet, findElev

class MyTestCase(unittest.TestCase):

    def test_findTime(self):

        dict1= {"_id": 0, "_speed": 5.0, "_minFloor": -0, "_maxFloor": 100, "_closeTime": 1.0,
                    "_openTime": 1.0, "_startTime": 1.0,"_stopTime": 1.0}
        dict2 = {"_id": 1, "_speed": 10.0, "_minFloor": -0, "_maxFloor": 100, "_closeTime": 2.0,
                    "_openTime": 2.0, "_startTime": 2.0, "_stopTime": 2.0}

        Elev1 = Elevator(dict1)
        Elev2 = Elevator(dict2)
        trip1 = Triplet(10, 14.25, 14.25)
        trip2 = Triplet(30, 0, 0)
        trip3 = Triplet(25, 16.25, 16.25)
        trip4 = Triplet(0, 0, 0)

        t1=trip1.findTime(trip2,Elev1)
        t2=trip3.findTime(trip4,Elev2)

        timeact1=22.25
        timeact2=26.75
        self.assertEqual(t1, timeact1)
        self.assertEqual(t2, timeact2)


    def test_changeTime(self):

        dict1 = {"_id": 0, "_speed": 5.0, "_minFloor": -0, "_maxFloor": 100, "_closeTime": 1.0,
                     "_openTime": 1.0, "_startTime": 1.0, "_stopTime": 1.0}

        Elev1 = Elevator(dict1)

        # pre change
        trip1 = Triplet(10, 14.25, 14.25)
        trip2 = Triplet(30,22.25, 22.75)
        trip3 = Triplet(25, 16.25, 16.25)
        trip4 = Triplet(0, 25.25, 25.25)
        # after change
        trip5 = Triplet(10, 14.25, 14.25)
        trip6 = Triplet(30, 22.25, 26.25)
        trip7 = Triplet(25, 16.25, 21.25)
        trip8 = Triplet(0, 25.25, 36.25)

        trip1.changeTime(trip3,Elev1);
        trip3.changeTime(trip2, Elev1);
        trip2.changeTime(trip4, Elev1);

        self.assertEqual(trip1.runTime, trip5.runTime)  # add assertion here
        self.assertEqual(trip2.runTime, trip6.runTime)  # add assertion here
        self.assertEqual(trip3.runTime, trip7.runTime)  # add assertion here
        self.assertEqual(trip4.runTime, trip8.runTime)  # add assertion here
        self.assertEqual(trip1.minTime, trip5.minTime)  # add assertion here
        self.assertEqual(trip2.minTime, trip6.minTime)  # add assertion here
        self.assertEqual(trip3.minTime, trip7.minTime)  # add assertion here
        self.assertEqual(trip4.minTime, trip8.minTime)  # add assertion here


    def test_whereAtTime(self):
        dict1 = {"_id": 0, "_speed": 5.0, "_minFloor": -0, "_maxFloor": 100, "_closeTime": 1.0,
                     "_openTime": 1.0, "_startTime": 1.0, "_stopTime": 1.0}

        Elev1 = Elevator(dict1)
        trip5 = Triplet(10, 14.25, 14.25)
        trip7 = Triplet(25, 16.25, 21.25)
        trip6 = Triplet(30, 22.25, 26.25)
        trip8 = Triplet(0, 25.25, 36.25)
        Elev1.callList.append(trip5)
        Elev1.callList.append(trip7)
        Elev1.callList.append(trip6)
        Elev1.callList.append(trip8)

        floor1=Elev1.whereAtTime(15)
        floor2 = Elev1.whereAtTime(27)
        floor3 = Elev1.whereAtTime(23)
        floor4 = Elev1.whereAtTime(5)
        floor5 = Elev1.whereAtTime(20)
        floor6 = Elev1.whereAtTime(18)
        floor7 = Elev1.whereAtTime(50)

        self.assertEqual(10,floor1)
        self.assertEqual(30, floor2)
        self.assertEqual(25, floor3)
        self.assertEqual(10, floor4)
        self.assertEqual(25, floor5)
        self.assertEqual(19, floor6)
        self.assertEqual(0, floor7)



    def test_findElev(self):

        dict3={"_minFloor": -2,"_maxFloor": 10,}
        dict1 = {"_id": 0, "_speed": 5.0, "_minFloor": 0, "_maxFloor": 100, "_closeTime": 1.0,
                     "_openTime": 1.0, "_startTime": 1.0, "_stopTime": 1.0}
        dict2 = {"_id": 1, "_speed": 10.0, "_minFloor": 0, "_maxFloor": 100, "_closeTime": 1.5,
                    "_openTime": 1.5, "_startTime": 1.5, "_stopTime": 1.5}

        building1=Building(dict3)
        Elev1 = Elevator(dict1)
        Elev2 = Elevator(dict2)
        building1.ElevList.append(Elev1)
        building1.ElevList.append(Elev2)

        trip1 = Triplet(10, 14.25, 14.25)
        trip2 = Triplet(30, 0, 0)
        trip3 = Triplet(25, 16.25, 16.25)
        trip4 = Triplet(0, 0, 0)
        call1E = findElev(building1.ElevList,trip1,trip2)
        call2E = findElev(building1.ElevList,trip3,trip4)

        self.assertEqual(call1E,0)
        self.assertEqual(call2E, 1)


if __name__ == '__main__':
    unittest.main()
