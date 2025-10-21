# Colour Identification Camera

Imagine a rubik's cube. It has six sides, with nine coloured squares on each side. The way to solve it is not by getting one side to be all the same colour. Rather, the goal is to match the cubes to be in specific spots. This program does exactly that. 

This program utilises opencv to allow the code to access a camera. It is currently optimised for a windows 11 computer. It will divide the camera feed into nine rectangles of equal size. When it has identified that at least 60% of the rectangle contains the colour needed, it will mark the rectangle green. Once all nine rectangles are green, the program will end.
