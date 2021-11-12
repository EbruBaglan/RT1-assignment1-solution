Research Track 1 - Assignment 1 - Solution
================================

This is a solution to the proposed problem by in the Research Track 1 course offered by the Università degli Studi di Genova in 2021-2022 Fall semester by Professor Carmine Recchiuto. The assignment requires the robot to avoid crashing the golden tokens and collecting and leaving behind the silver tokens. The simulator used is a simple, portable robot simulator developed by [Student Robotics] (https://studentrobotics.org). Notice that some of the arenas and the exercises have been modified for the Research Track I course by Professor Carmine Recchiuto.

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the `test.py` script to test out the simulator.

## How to run the solution to the assignment
-----------------------------

To run the script in the simulator, use `run.py`, passing it the file name. 

The solution for the assignment can be found inside the main directory, named solution.py.

When done, you can run the program with:

```bash
$ python run.py solution.py
```

Solution Explaining Video
---------

Not to take too much time, here is an explanatory video that you can see both my flowchart and code. Notice that the video is visible to only the ones with the link, so it is only Professor Carmine Recchiuto who can view the video.


[![Explanation of the flowchart and the code](https://img.youtube.com/vi/CarIHrRCf3Q/0.jpg)](https://www.youtube.com/watch?v=CarIHrRCf3Q)

### Flowchart ###

![alt text](https://i.ibb.co/XksfB1s/flowchart.png)


The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.
