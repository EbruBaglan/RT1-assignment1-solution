from __future__ import print_function
import time
from sr.robot import *

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels>
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed*2
    R.motors[0].m1.power = -speed*2
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

# Below-defined bubbleSort function does not belong to me, here is the source:
# https://github.com/aniketsharma00411/algorithmsUse/blob/master/Python/Sorting/bubble_sort.py
def bubbleSort(arr):
    """"
    Function for bubblesorting angle array

    Args: arr (array): the array of observed
      angles at an instant.

    """
    n = len(arr)
 
    # Traverse through all array elements
    for i in range(n-1):
    # range(n) also work but outer loop will repeat one time more than needed.
 
        # Last i elements are already in place
        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j + 1] :
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def largestgap(n):
    """"
    Function for finding the 2 angles where a huge increase in sorted angle array is observed. These values
       refer to the angle intervals where our robot can move to (the apertures/corridors/roads).

    Args: n (array): the array of observed angles in increasing order at an instant.
    """
    i = 0
    intervals0 = [0 for x in range(len(n)-1)]
    
    for i in range(1,len(n)-1):             # The difference between consecutive two elements in sorted array is calculated here.
         intervals0[i] = (n[i+1]-n[i])      

    intervals0[0] = n[1]-n[0]+n[-1]-n[-2]   # The first element is for 180 degree aperture. The angle between +180 and highest angle is
    intervals1 = intervals0                 # added to the angle between -180 and lowest angle, to get the angle between highest and
                                            #  lowest angle at backwards of robot.
    max_index0 = intervals1.index(max(intervals1))      # Maximum jump's index is obtained.
    
    if max_index0 == 0:                     # This part is hard to visualize. If the maximum jump is observed at the first element,
        ang1 = (n[1]+n[-2])/2               # we should find the mean of a minimum angle(negative) and a maximum angle (positive).
        if ang1 == 0:                       # If their mean is 0 (for instance +160 degree and -160 degree), our turning angle is actually 180 degree.
            ang1 = 180                      # Meaning total backwards. So instead of 0, the value of 180 is assigned to correct this.
        elif ang1/abs(ang1) == +1:          # If the mean of maximum jump is positive, (per esampio +170 degree and -160 degree),
            ang1 = ang1 - 180               # mean value turns out to be +5. However it is not compliant with our navigation. To correct this,
        elif ang1/abs(ang1) == -1:          # we should subtract 180 from +5 (actual mean is -175). And for the other case, vice versa.
            ang1 = ang1 + 180               
        
        intervals1[0] = 0                   # Assigning 0 to first element, to find the second largest.
        
        max_index1 = intervals1.index(max(intervals1))  # The second largest element's index is found here.
        ang2 = (n[max_index1] + n[max_index1+1])/2      # The mean of that angle and its next one is calculated here.
        return ang1, ang2                               # Values are returned.

    else:
        ang1 = (n[max_index0] + n[max_index0+1])/2      # The mean of the highest jump is obtained here.
        intervals1[max_index0] = 0                      # Assigning 0 to get the second largest.

        max_index1 = intervals1.index(max(intervals1))  
        ang2 = (n[max_index1] + n[max_index1+1])/2      # The mean of the second highest jump is obtained here.
        return ang1, ang2                               # Angles are returned.

def silver_radar(silver_sight_angle, silver_sight_distance):
    """"
    Function for radaring for a nearby silver. If there is one
       in given angle values and given distance, it will either
       turn to it or grab it, leave it behind and go on the journey.

    Args: silver_sight angle (int): the angle range to look for.
       silver_sight_distance (int): the distance range to look for.

    """
    i = 0
    markers = R.see()
    for token in markers:
        if token.info.marker_type is MARKER_TOKEN_SILVER and abs(token.rot_y) <= silver_sight_angle and token.dist <= silver_sight_distance:
            rot_y = int(token.rot_y)
            dist = int(token.dist)              # In case of silver existence, its rotation and distance is obtained, and i becomes 1.
            i = i + 1                           # In absence, i keeps 0, and there is nothing else to check in the rest of this function.

    if i != 0:
        if abs(rot_y) >=6 and dist >= 0.4:      # If rotation is greater than 6 unit with distance higher than 0.4 m, robot turns to the silver for better alignment.
            turn(rot_y/6.0, 0.94)
        
        elif dist <= 0.4 and R.grab():          # If the silver is closer than 0.4 m and R.grab is successful, robot turns behind, leaves it, and goes on its journey.
            turn(30, 1)
            R.release()
            turn(-30,1)

def gold_radar(desired_max_angle, desired_max_dist):
    """"
    Function for checking for any gold in +/-desired_max_angle within desired_max_dist range.
       It just checks if there is one or none. When returned zero, means existence of gold.

    Args: desired_max_angle (int): the maximum angle range to look for.
       desired_max_dist (float/int): the distance range to look for.
    """
    i = 0
    markers = R.see()
    for token in markers:
        if token.info.marker_type is MARKER_TOKEN_GOLD and abs(token.rot_y) <= desired_max_angle and token.dist <= desired_max_dist:
            i = i + 1

    if i != 0:
        return 0

def see_the_big_picture(desired_max_dist):
    """"
    Function for radaring golds in +/-180 degree within desired_max_dist range.
       The angles of goldens are taken into an array with -180 and 180 degree angles.
       Sorting the angles in bubblesort and finding the biggest two jumps in 2 angle values,
       robot now knows where there are 2 apertures/roads it can lead to. Notice that, the road
       it has come from will have absolute higher value than the road it should turn to.
       That is why it should find the absolute minimum in value, and turn to that way.

    Args: desired_max_dist (float/int): the distance range to look for.
    """
    i = 0
    rot_list = [180 for r in range(200)]                # The rotation list is initiated with 180 degree, as we would later on add this value to the array
                                                        # to calculate the difference between the absolute maximum.
    markers = R.see()
    for token in markers:
        if token.info.marker_type is MARKER_TOKEN_GOLD and token.dist <= desired_max_dist:
            rot_list[i] = int(token.rot_y)
            i = i + 1                                   # Number of golds detected are taken with the associated rotations.

    rot_list[i+1] = -180                                # -180 degree is also added to the array, as the difference between minimum angle also need to be calculated.
    sortedrotlist = bubbleSort(rot_list[0:i+2])         # Rotations are sorted in increasing order.
    angle1, angle2 = largestgap(sortedrotlist)          # The middle of biggest two jumps in sorted rotation list refers to the directions we can turn to.
    return angle1, angle2                               # Among these, one of them is the road we come from, and the other one is the one we should turn to.

def check_and_avoid_golds():
    """"
    Function for radaring golds in within +/- 40 degree and 0.7m range
      by calling gold_radar function. If the output of gold_radar equals zero,
      there exists AT LEAST ONE gold marker. In this case, we need to detect
      TWO possible corridors' angles and drove towards there.
      angle1 and angle2 refers to the possible apertures we can drive to.
      Among these, one is the one we came from (with higher absolute value),
      and the other one is the road we should take. We get the one with lower value
      and turn towards that direction.

    Args: no args.
    """
    if gold_radar(40, 0.7) == 0:
        angle1, angle2 = see_the_big_picture(2.4)
        print("\n\ncheck_and_avoid_golds: The possible angles to turn are...\n\n         ", angle1," and ", angle2, "\n\n")
        # Above line is to follow the flow of the code. Can be uncommented for debugging purposes.
        if min(abs(angle1),abs(angle2)) == abs(angle1):
            turn(angle1/6,1)
        else:
            turn(angle2/6,1)

while 1:                            # This is our routine.
    drive(100,0.04)                 # The robot drives at 100 m/s and for 0.04 s.                
    check_and_avoid_golds()         # Then, it checks its front side for gold, and avoids it in this chunk of check_and_avoid_golds function.
    silver_radar(80, 1.3)           # After clearing obstacles, it checks for silver around (within +/- 80 angle and 1.3 m distance, to be precise).