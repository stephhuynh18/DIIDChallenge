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
    
    """
    Description: parses input, for each rover checks if it in collision with another rover, calculates intial rover movement,
                 writes end positions to file
    Return: None
    Inputs: inputFile (string), outputfile(string)
    """
    def __init__(self, inputFile, outputFile):
        self.allRoverPos = set()
        self.leftB = None
        self.rightB = None
        self.topB = None
        self.bottomB = None
        
        try:
            lines = self.parse_input(inputFile)
            
            for i in range(0, len(lines), 2):
                startPos = lines[i]
                #check if two rovers start at same position
                if (startPos[0], startPos[1]) in self.allRoverPos:
                    print("Error: Two rovers cannot start in the same position; cannot instantiate.")
                    raise ValueError
                else:
                    self.allRoverPos.add( (startPos[0], startPos[1]) )
                    self.updateBoundaries(startPos[0], startPos[1])

            
            output = []
            i = 1
            while i < len(lines):
                startPos = lines[i-1]
                instructions = lines[i]
                self.allRoverPos.remove( (startPos[0], startPos[1]) )
                
                success, endPos = self.move_rover(startPos, instructions)
                self.allRoverPos.add((endPos[0], endPos[1]))
                #can move rover
                if success:
                    output.append(" ".join(str(c) for c in endPos))
                #can't move rover or rover will collide 
                else:
                    output.append("Error: Unable to move rover at " + " ".join(str(c) for c in endPos) )

                i+=2
                
            with open(outputFile, 'w') as f:
                for pos in output:
                    f.write(pos)
                    f.write('\n')
        
        except ValueError:
            raise
    
    
    """
    Name: updateBoundaries
    Description: updates the boundaries if they are exceeded
    Return: None
    Inputs: x (int), y (int)
    """
    def updateBoundaries(self, x, y):
        if not(self.leftB) or x < self.leftB:
            self.leftB = x
        if not(self.rightB) or x > self.rightB:
            self.rightB = x
        
        if not(self.topB) or y > self.topB:
            self.topB = y 
        if not(self.bottomB) or y < self.bottomB:
            self.bottomB = y
          
            
    """
    Name: checkBoundaries
    Description: check if the seen terrain is within the safe boundaries
    Return: True if x and y are within the currently seen boundaries and False otherwise
    Inputs: x (int), y (int)
    """
    def checkBoundaries(self, x, y):
        if x < self.leftB or x > self.rightB or y > self.topB or y < self.bottomB: 
            return False
        return True
    
    
    """
    Name: parse_input
    Description: Parses the file 
    Return: List containing the starting positions and instructions
    Inputs: fileName
    """
    def parse_input(self, fileName):
        output = []        
        with open(fileName) as f:
            i = 0
            for line in f:
                cleaned = line.strip().upper()
                if cleaned:
                    #parse odd lines as these are starting positions
                    if i%2==0:
                        startPos = cleaned.split(" ")
                        if len(startPos)!=3:
                            output.append("Error: Incorrect input -- " + line)
                        else:
                            try:
                                x = int(startPos[0])
                                y = int(startPos[1])
                                direction = startPos[2]
                                output.append([x,y,direction])
                            except ValueError:
                                raise
                    #don't parse instructions
                    else:
                        output.append(cleaned)
                i+=1
                
            if len(output)%2 != 0:
                raise ValueError 
                
        return output
    
    
    """
    Name: checkTerrain
    Description: Temp function replacing what would actually be in place 
    Return: True if terrain is clear 
    Inputs: x (int), y (int)
    """
    def checkTerrain(self, x, y):
        if x < 0 or x > 20 or y < 0 or y > 20:
            return False
        return True
    
    
    """
    Name: move_all_rovers
    Description: moves serveral rovers as indicated by the input file then writes ending position to a file
    Return: None
    Inputs: inputFile (string), outputfile(string)
    """         
    def move_all_rovers(self, inputFile, ouputFile):
        try:
            lines = self.parse_input(inputFile)
            output = []
            i = 1
            
            while i < len(lines):
                startPos = lines[i-1]
                instructions = lines[i]
                #make sure rover exists
                if (startPos[0], startPos[1]) not in self.allRoverPos:
                    output.append("Error: Rover does not exist.")
                else:
                    self.allRoverPos.remove((startPos[0], startPos[1]))
                    
                    success, endPos = self.move_rover(startPos, instructions) 
                    self.allRoverPos.add((endPos[0], endPos[1]))
                    if success:
                        output.append(" ".join(str(c) for c in endPos))
                    else:
                        output.append("Error: Unable to move rover at " + " ".join(str(c) for c in endPos) )
                i+=2
            
            with open(ouputFile, 'w') as f:
                for pos in output:
                    f.write(pos)
                    f.write('\n')
        
        except ValueError:
            raise         
            
            
    """
    Name: move_rover
    Description: Calcualtes the movemnt of a single rover
    Return: Bool indicating if the move was successful, 
            List containing three elements: X(int), Y(int), Orientation(string)
    Inputs: startPos -- list describing the rover's starting position [x(int), y(int), orientation(string)]
            instructions -- string describing the movement of the rover
    """
    def move_rover(self, startPos, instructions):
        if not(startPos) or type(startPos)!=list or len(startPos)!=3:
            raise ValueError
        
        if not(instructions) or type(instructions)!=str:
            raise ValueError
        
        try:
            x = int(startPos[0])
            y = int(startPos[1])
            orientation = startPos[2]
            
            orientation = self.convertToNum(orientation)
            
            currPos = [x,y]
            for i in instructions:
                #keep last just in case boundary is reached or collision happens
                #so stop before crashing and do not continue but don't go back to start
                lastX = currPos[0]
                lastY = currPos[1]
                lastD = orientation
                
                if i == "L":
                    orientation -= 1
                elif i == "R":
                    orientation += 1
                elif i == "M":
                    change = self.convertToCoord(orientation)
                    currPos[0] += change[0]
                    currPos[1] += change[1]
                    #if there is a collision return current position
                    if (currPos[0], currPos[1]) in self.allRoverPos:
                        return False, [lastX, lastY, self.convertToLetter(lastD)]
                    #if you are outside of the currently seen boundaries check the terrain in front to ensure there is no failures
                    if not(self.checkBoundaries(currPos[0], currPos[1])):
                        #if the terrain is clear update the boundaries
                        if (self.checkTerrain(currPos[0], currPos[1])):
                            self.updateBoundaries(currPos[0], currPos[1])
                        #terrain is not clear so return the current position of the rover
                        else:
                            return False, [lastX, lastY, self.convertToLetter(lastD)]
                else:
                    raise ValueError
                
                if orientation < 0 :
                    orientation = 3
                if orientation > 3 : 
                    orientation = orientation%4
            
            orientation = self.convertToLetter(orientation)
            currPos.append(orientation)
            return True, currPos
        
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
        else:
            raise ValueError
        
        
    """
    Name: convertToCoord
    Description: convert num to associated coordinate describing change in direction
    Return: [int, int]
    Inputs: direction (int)
    """   
    def convertToCoord(self, direction):
        if direction == Directions.N:
            return [0,1]
        elif direction == Directions.S:
            return [0,-1]
        elif direction == Directions.E:
            return [1,0]
        elif direction == Directions.W:
            return [-1,0]
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

def main():
    startFileName = "test5.txt"
    outputFileName = "test5out.txt"
    
    moveFileName = "test6.txt"
    outputMoveFileName = "test6out.txt"
    
    solution = DIID(startFileName, outputFileName)
    solution.move_all_rovers(moveFileName, outputMoveFileName)
    
main()

################################################################

#correct input
#test1 = DIID("test.txt", "testout.txt")
 
#collission
#test2 = DIID("test2.txt", "test2out.txt")

#incorrect num lines
#test3 = DIID("test3.txt", "test3out.txt")

#incorrect input
#test4 = DIID("test4.txt", "test4out.txt")

#incorrect start input
#test7 = DIID("test7.txt", "test7out.txt")


################################################################

#correct move input with one outside of boundaries
#test5 = DIID("test5.txt", "test5out.txt")
#test5.move_all_rovers("test6.txt", "test6out.txt")

#incorrect move input
#test5.move_all_rovers("test7.txt", "test8out.txt")

#rover does not exist
#test5.move_all_rovers("test8.txt", "test9out.txt")


################################################################
#correctInput
#print(solution.move_rover([0,0,"N"], "MMMRMMLMLMLM"))
#print(solution.move_rover([5,3,"S"], "RMMRMLLMMMM"))

#incorrect start pos
#print(solution.move_rover([], "MMMRMMLMLMLM"))
#print(solution.move_rover(123, "MMMRMMLMLMLM"))
#print(solution.move_rover(["e",0,"N"], "MMMRMMLMLMLM"))

#incorrect directions
#print(solution.move_rover([0,0,"N"], ""))
#print(solution.move_rover([0,0,"N"], "fewef"))
#print(solution.move_rover([0,0,"N"], "MMMRMMLML3LM"))

    
    

