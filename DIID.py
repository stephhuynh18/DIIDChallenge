# -*- coding: utf-8 -*-
"""
Assumptions:
    -Can we assume the plateau is rectagular?
        I am asssuming it is.
        If was not not, instead of storing bounds I would store a dictionary(hash map) containing a bool 
        indicating whether a grid position was traversable
    -Can be assume all the terrain is traversable?
        I am assuming it is.
        If it was not, I would be required to use a hash mpa as stated above 
    -Can we assume that there is a function that determines if the terrain in front of a rover is traversable?
        I am assuming there is.
        If not there would be no way to determine the boundaries of the plateau and all the rovers would fall off. 
        Also the mention of onboard cameras indicates that there is a method to determine if the terrain directly
        in front of the rover can be seen.
    -Can we assume that the rovers should not collide?
        I am assuming that rovers cannot collide 
    -If the rover cannot move any further should it stop or go back to its start?
        I am assuming that since the purpose of the rovers are discovery they would just stop and send a message
        
"""

from enum import IntEnum

class Directions(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3
    
    
class DIID():
    
    roverPos = set()
    
    #TODO: Add checking of boundaries, whether rover exists, whether rover will collide, 
    """
    Name: move_rover
    Description: Calcualtes the movemnt of a single rover
    Return: List containing three elements: X(int), Y(int), Orientation(string)
    Inputs: startPos -- list containing three elements describing the rover's starting position [x(int), y(int), orientation(string)]
            instructions -- list containing string elements describing the movement of the rover as described in the instructions
    """
    def move_rover(self, startPos, instructions):
        if not(startPos) or type(startPos)!=list or len(startPos)!=3:
            raise ValueError
        
        if not(instructions) or type(instructions)!=list or len(instructions)<0:
            raise ValueError
        
        try:
            x = int(startPos[0])
            y = int(startPos[1])
            orientation = startPos[2].strip().upper()
            
            orientation = self.convertToNum(orientation)
            
            currPos = [x,y]
            for i in instructions:
                i = i.strip().upper()
                
                if i == "L":
                    orientation -= 1
                elif i == "R":
                    orientation += 1
                elif i == "M":
                    change = self.convertToCoord(orientation)
                    currPos[0] += change[0]
                    currPos[1] += change[1]
                else:
                    raise ValueError
                
                if orientation < 0 :
                    orientation = 3
                
                if orientation > 3 : 
                    orientation = orientation%4
            
            orientation = self.convertToLetter(orientation)
            currPos.append(orientation)
            return currPos
        
        except ValueError:
            raise
    
    """
    Name: converToLetter
    Description: convert num to associated letter describing direction
    Return: string
    Inputs: direction(int)
    """    
    def convertToLetter(self, direction):
        if direction == Directions.N:
            return "N"
        elif direction == Directions.S:
            return "S"
        elif direction == Directions.E:
            return "E"
        elif direction == Directions.W:
            return "W"
        
    """
    Name: convertToCoord
    Description: convert num to associated coordinate describing change in direction
    Return: [int, int]
    Inputs: direction (int)
    """   
    def convertToCoord(self, direction):
        if direction == Directions.N:
            return [1,0]
        elif direction == Directions.S:
            return [-1,0]
        elif direction == Directions.E:
            return [0,1]
        elif direction == Directions.W:
            return [0,-1]
        else:
            raise ValueError
    
    """
    Name: convertToNum
    Description: convert string to associated num describing direction
    Return: int
    Inputs: direction (string)
    """   
    def convertToNum(self, direction):
        if direction == "N":
            return Directions.N
        elif direction == "S":
            return Directions.S
        elif direction == "E":
            return Directions.E
        elif direction == "W":
            return Directions.W
        else:
            raise ValueError
            
        

solution = DIID()
print(solution.move_rover([0,0,"N"], ["M", "M", "M", "R", "M", "M", "L", "M", "L", "M", "L", "M"]))
print(solution.move_rover([5,3,"S"], ["R", "M", "M", "R", "M", "L", "L", "M", "M", "M", "M"]))

#print(solution.move_rover([], ["M", "M", "M", "R", "M", "M", "L", "M", "L", "M", "L", "M" ]))
#print(solution.move_rover(123, ["M", "M", "M", "R", "M", "M", "L", "M", "L", "M", "L", "M" ]))
#print(solution.move_rover(["e",0,"N"], ["M", "M", "M", "R", "M", "M", "L", "M", "L", "M", "L", "M"]))

#print(solution.move_rover([0,0,"N"], []))
#print(solution.move_rover([0,0,"N"], "fewef"))
#print(solution.move_rover([0,0,"N"], ["M", "M", "M", "R", "M", "M", "L", "M", "L", "3", "L", "M"]))

    
    

