
# OOP_Ex1
## Ido Bar & Yehudit Brickner

Our assignment is to create an <b>offline algorithm</b> for elevators that the average wait time is as small as possible.

We were provided with csv files with the calls for the elevator, and json files that contain the object Building. The object Building contains the object Elevator. 

Before we started to write code for this project, we looked up similar project dealing with elevators and articles about the best way to program elevators. Below are links to what we found:
1.	https://www.geeksforgeeks.org/smart-elevator-pro-geek-cup/
2.	https://towardsdatascience.com/elevator-optimization-in-python-73cab894ad30
3.	https://www.popularmechanics.com/technology/infrastructure/a20986/the-hidden-science-of-elevators/
4.	https://www.npr.org/templates/story/story.php?storyId=6799860
___________________________________________________________________________________________________________________________________________
To run our code, you will need to import pandas to your python environment if it isn’t installed already. To do so you can run this code to install.
“pip install pandas”

Our program contains 3 classes:

1.	Building: the building gets most of attributes from the json file. We added an attribute of ElevList to contain the number of elevators in the building.
2.	Elevator: the elevator also gets most of its attributes from the json file. We added the attribute CallList to so that we can follow the calls that the elevator has.
3.	Triplets: this is an object that we made up. We used this object to follow the time as we added more calls to the Elevators CallList.
The Triplets have 3 attributes:
<br><b>a.</b>	Floor: this is ether the source or destination of the call.  
<b>b.</b>	MinTime: this is the smallest time that we can leave the floor and start going to the next floor. This happens because the algorithm is offline we are planning what the elevator will do without the elevator moving.
<br><b>c.</b>	RunTime: this is the time that the elevator actually gets to the floor. As we add more calls to the Elevators CallList we will be Updating this                      attribute.
<br>And our program has 2 function and the main outside of the classes.
____________________________________________________________________________________________________________________________________________________

### Our algorithm:
We start with the function <b>readfilies</b>, we will read the json and csv file.
<br>From the json file we will create the Building and Elevator/s.
<br>From the csv we will create 2 data frames. The first called calls, and the second called output. We will be changing the output data frame and, in the end, save it as a new csv.

With a for loop, we will go through the rows of the calls data frame and create 2 triplets for each row. Triplet src contains the source floor, and triplet dest contains the destination floor. We will use the same for loop to change the output file with the function findElev. That function finds the best elevator for each call and then we change the output file so that, that number elevator takes the call. When we finish the for loop, we save the data frame output to the computer.

The function <b>findElev</b> gets the buildings ElevList and the 2 triplets.
<br>The first thing we will check is if the building has 1 elevator. If there is only 1 elevator, we will right away return that the elevator taking the call is elevator 0.
<br>If there are more than 1 elevator, we will go through all the elevators in the building and find the elevator that when we add the new call to it, the overall change in the time is the least. When we run this function, we don’t want to change the original callList and triplets, so we make copies of all of them. In the middle of the findElev function we will call the findTime function. After we run the find time function, we will go through the triplets in the elevators callList till we find the right spot to triplets in. we will find the spots to put them in by looking at the time first. We will only add in the triplet if its runtime is bigger than the first triplet we are looking at and if the floor is in between or equals the 2 floors that we are looking at. We will also only add in the dest after the src.
<br>After adding in the src and dest we will go through the CallList and call the function chageTime to change the time we get to each floor, and to calculate amount of time added by adding this call.
<br>After running the changeTime function we will keep track which elevator had the least change in time when adding the call. And that will be the elevator taking the call.

The function <b>findTime</b> calculates how long it will take to get to the dest from the src, if we pick up the src triplet right as the call is made, and don’t stop along the way. <br>We will calculate the runtime by adding the closeTime + openTime + startTime + stopTime + the number of floors between the src and dest / by the speed + the runTime of the src and return all those times as the variable time.

The function <b>changeTime</b> does the same calculation as the function findTime,
<br>but it is dose the calculation between pairs of consecutive triplets in the callList to see how much time we added to the CallList by adding the call to the elevator.
<br>If the time is bigger than the dest run time than we will change the dest runtime and add the difference to a variable sum. At the end of the function, we will return sum.

In the elevator class we have a function <b>whereAtTime</b> that calculates where the elevator is at a given time, if the elevator is in between floors, it will return the bigger floor.

We can calculate the time by going through the callList and comparing the given time to the runtime. Once we figure out between which calls the time is we can calculate where the elevator is by: 
<br>Floors=time-(openTime+closeTime+startTime+stopTime+runTime)
<br>Floors*speed will give us the number of floors we are from the floor in the callList.
<br>than we just add or subtract the floors from the floor in the calllList.
<br>If time-closeTime-startTime is smaller than the callList runtime than we are still on that floor.
<br>If time+ stopTime+openTime is bigger than the next callList runtime than we are on that floor.
<br>If the time is before the first runtime in the callList than we will calculate where it is on its way to the first call- if the calculation gives a number that is passed the floor than it is waiting in the floor of the first call.
<br>If the time is bigger than the last runtime In the callList than the elevator is at the last floor.
<br>If the callList has no calls the elevator is on 0.
__________________________________________________________________________________________________________________________________________________________________________________
#### Here is a UML diagram of our program:
https://github.com/idobar1403/OOP_Ex1/blob/main/uml-elevators-offline.png
_________________________________________________________________________________________________________________________________________________________________________________
Here are our best results rounded up to 1 spot after the decimal:

|   	    | B1     |	B2	| B3   |	B4  |	B5   |
|---------|--------|------|------|------|------|
| Calls_a |	113	  | 42.6 |	27.8 |	21 |	15.5 |
| Calls_b	|		    |      | 522.1 |	183.2 |	35.3 |
| Calls_c	|		    |      | 541.8 |	186.7 |	35.2 |
| Calls_d	|		   |       | 506 | 181.2 |	36.4 |


For buildings 1, and 2 we only ran calls_a because this is the only csv file with calls that are in the floor range of these buildings. (-2,10)

