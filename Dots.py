"""
Dots and Boxes aka (Shermin Squares)
This files serves as the class definition of the game.
It uses the turtle draw package to provide a simple
visual representation of the Games states.
- 2 Players
- Board Must be Square
- Can play with Human, Random Moves, or Q Learning Agent
Running this python script will initiate a Human v Human Game.
Last Updated: 4/28/19
"""
from enum import Enum
import turtle, Dots_RandMove_Comp
import random
import numpy as np

class PlayerType(Enum):
   Human = 1
   RandMoves = 2
   QLearning = 3

class Owner(Enum):
   Player1 = 1
   Player2 = 2
   NeitherPlayer = 3

class Side:
   def __init__(self):
       self.owner = Owner.NeitherPlayer


   def changeOwner(self, aOwner):
       self.owner = aOwner


   def updatePosition(self, aPos):
       [[x1,y1],[x2,y2]] = aPos
       drawSpacing = 50 # Used to get some spacing when drawing with turtle
       self.wallPos = [[drawSpacing*x1,-y1*drawSpacing],[x2*drawSpacing,-y2*drawSpacing]]
       #Multiply All Y Values by -1 for turtle draw package


class Square:
   def __init__(self, leftSide, topSide, rightSide, botSide, aPos):
       self.sideList = [leftSide, topSide, rightSide, botSide]
       self.owner = Owner.NeitherPlayer
       self.Pos = aPos
       self.claimed = False


   def updateOwner(self, aOwner):
       if (Owner.NeitherPlayer not in [x.owner for x in self.sideList] and not self.claimed):
           self.owner = aOwner
           self.claimed = True


class Game:
   # Game Size will be the size of the Gameboard
   # (i.e. Gameboard will have aSize x aSize squares)
   def __init__(self, aSize, displayOn=True, randomSeed = 1):
       numSides = 2*aSize*(aSize+1)
       np.random.seed(randomSeed) # For repeatability of who goes first
       self.allSides = [Side() for x in range(numSides)]
       self.allSquares = self.buildBoard(aSize)
       self.displayOn = displayOn
       if self.displayOn:
           self.drawBoard()
       startingPlayer = random.randint(0,1)
       if startingPlayer:
           tPl = Owner.Player2
       else:
            tPl = Owner.Player1
       self.turn = tPl
       #Player1's Score and Player2's Score
       self.score = {}
       self.score[Owner.Player1] = 0
       self.score[Owner.Player2] = 0 
       self.turnsElapsed = startingPlayer
       self.moveSelectionDict = {PlayerType.Human : self.humanMove,
                         PlayerType.RandMoves : self.getRandMove,
                        }


   def getRandMove(self):
       return Dots_RandMove_Comp.gen_RandMove(self)


   def drawBoard(self):
       draw_lines([aWall.wallPos for aWall in self.allSides], 'grey', dots = 1)
       draw_lines([aWall.wallPos for aWall in self.allSides if aWall.owner == Owner.Player1], 'blue', dots = 1)
       draw_lines([aWall.wallPos for aWall in self.allSides if aWall.owner == Owner.Player2], 'orange', dots = 1)


   def getSquareFromTerminal(self):
       #DEFINE FOR A HUMAN
       print("Enter the Coordinates of the Square you'd like to modify")
       theSquare = []
       while not theSquare: #Coords are Empty
           try:
               aCoord = input("(0,0) in top left x to the right and y down: ")
               [x, y] = aCoord.split(",")
               aCoord = [int(x), int(y)]
               theSquare = [tSquare for tSquare in self.allSquares if tSquare.Pos == aCoord]
               if not theSquare: #Square Position was not found
                       print("Sorry Square not found. Please Try again")
           except ValueError:
               print("Oops. Input misunderstood. Please try again.")
       return theSquare[0]

   
   def getSideFromTerminal(self, aSquare):
       tMap = {"U":aSquare.sideList[1],
               "D":aSquare.sideList[3],
               "L":aSquare.sideList[0],
               "R":aSquare.sideList[2]}
       tSide = []
       while not tSide:
           tSideStr = input("Please Enter U, D, L, or R to choose a side: ").upper()
           tSide = tMap.get(tSideStr)
           if not tSide: #Side was not found
                   print("Sorry Side not found. Please Try again")
       return tSide
   

   def humanMove(self):
       validMove = False
       while not validMove: # Make sure the side isnt already owned
           # Get the Square Coords From the User (0,0) in top left x to the right and y down
           tSq = self.getSquareFromTerminal()
           # Get the Side Of that Square From the User (UDLR)
           tWall = self.getSideFromTerminal(tSq)
           # Update that Wall
           if tWall.owner == Owner.NeitherPlayer:
               validMove = True
           else:
               print("Sorry. That wall is already owned.")
       return tWall
           
   # Ruleset = 1 means you will get to go again when you earn a point
   # Ruleset = 2 means no matter what you alternate with the other player
   # wall2Update will only be used by the computer players
   def playGame(self, ruleSet, playerTypes, wall2Update = None):
       if (len([x for x in self.allSides if x.owner == Owner.NeitherPlayer]) > 0):
           # Determine Turn
           if (self.turn == Owner.Player1):
               playerStr = "Player1"
           elif(self.turn == Owner.Player2):
               playerStr = "Player2"
           else:
               input("ERROR Unrecognized Player")
               #Exit
           if self.displayOn:
               print(f"Score: Player1: {self.score[Owner.Player1]}, Player2: {self.score[Owner.Player2]}")
               print("It is "+ playerStr + "'s Turn")
           aFcn = self.moveSelectionDict.get(playerTypes[self.turnsElapsed % 2])
           if aFcn:
               tWall = aFcn()
           else:
               tWall = wall2Update
           tWall.changeOwner(self.turn)
           # Update with Completed Squares
           lastScore = self.score.copy()
           self.score[Owner.Player1] = 0
           self.score[Owner.Player2] = 0
           self.reward = -1*lastScore[(self.turn)]
           for aSq in self.allSquares:
               aSq.updateOwner(self.turn)
               # Update Scores
               if aSq.owner == Owner.Player1:
                   self.score[Owner.Player1] = self.score[Owner.Player1] + 1
                   if self.turn == Owner.Player1: 
                       self.reward = self.reward + 1
               elif aSq.owner == Owner.Player2:
                   self.score[Owner.Player2] = self.score[Owner.Player2] + 1
                   if self.turn == Owner.Player2: 
                       self.reward = self.reward + 1
           # Draw the updated walls
           if self.displayOn:
               if self.turn == Owner.Player1:
                   draw_lines([tWall.wallPos], 'blue', dots = 1)
               elif self.turn == Owner.Player2:
                   draw_lines([tWall.wallPos], 'orange', dots = 1)
           if (len([x for x in self.allSides if x.owner == Owner.NeitherPlayer]) == 0):
               if self.score[Owner.Player1] > self.score[Owner.Player2]:
                   winner = Owner.Player1
               elif (self.score[Owner.Player1] > self.score[Owner.Player2]):
                   winner = Owner.Player2
               else:
                   winner = Owner.NeitherPlayer
               if self.turn == winner:
                   self.reward = self.reward + 5
               gameOver = True
               return gameOver
           # Based on the rules implemented chose whos turn it is based on the events that just transpired
           playerOptions = [Owner.Player1, Owner.Player2]
           if ruleSet == 1:
               if lastScore == self.score: # Then the current player has not scored
                   self.turnsElapsed = self.turnsElapsed + 1
                   # By not incrementing when the score was updated the turn will continue to be that players
           else :
               self.turnsElapsed = self.turnsElapsed + 1
           # Update the Who's Turn it is
           self.turn = playerOptions[self.turnsElapsed % 2]
           gameOver = False
           return gameOver
    

   # Returns a list of Squares that will be the gameboard
   def buildBoard(self, aSize):
       gameBoardSquares = []
       numSidesUsed = 0
       # Start with Top Left Move Right then Down
       for aSquareYIdx in range(aSize):
           for aSquareXIdx in range(aSize):
               tPos = [aSquareXIdx, aSquareYIdx]
               if (aSquareXIdx == 0): # New Square so New Sides
                   tLeftSide = self.allSides[numSidesUsed]
                   numSidesUsed = numSidesUsed + 1
                   tRightSide = self.allSides[numSidesUsed]
                   numSidesUsed = numSidesUsed + 1
               else:
                   idxOfSq = [sq.Pos for sq in gameBoardSquares].index([aSquareXIdx-1, aSquareYIdx ])
                   tLeftSide = gameBoardSquares[idxOfSq].sideList[2]
                   tRightSide = self.allSides[numSidesUsed]
                   numSidesUsed = numSidesUsed + 1
               if (aSquareYIdx == 0):
                   tTopSide = self.allSides[numSidesUsed]
                   numSidesUsed = numSidesUsed + 1
                   tBotSide = self.allSides[numSidesUsed]
                   numSidesUsed = numSidesUsed + 1
               else:
                   idxOfSq = [sq.Pos for sq in gameBoardSquares].index([aSquareXIdx, aSquareYIdx-1 ])
                   tTopSide = gameBoardSquares[idxOfSq].sideList[3]
                   tBotSide = self.allSides[numSidesUsed]
                   numSidesUsed = numSidesUsed + 1
               dist2Side = 0.5
               tLeftSide.updatePosition(([aSquareXIdx-dist2Side, aSquareYIdx - dist2Side],\
                   [aSquareXIdx-dist2Side, aSquareYIdx + dist2Side]))
               tRightSide.updatePosition(([aSquareXIdx+dist2Side, aSquareYIdx - dist2Side],\
                   [aSquareXIdx+dist2Side, aSquareYIdx + dist2Side]))
               tTopSide.updatePosition(([aSquareXIdx-dist2Side, aSquareYIdx - dist2Side],\
                   [aSquareXIdx+dist2Side, aSquareYIdx - dist2Side]))
               tBotSide.updatePosition(([aSquareXIdx-dist2Side, aSquareYIdx + dist2Side],\
                   [aSquareXIdx+dist2Side, aSquareYIdx + dist2Side]))
               aSquare = Square(tLeftSide, tTopSide, tRightSide, tBotSide, tPos)
               gameBoardSquares.append(aSquare)

       return gameBoardSquares
    

def draw_lines(lines, color='black', width=3, dots=0):
    """draw every line in lines"""
    turtle.pen(speed=0,shown=False)
    turtle.color(color)
    turtle.width(width)
    for line in lines:
        (p0, p1) = list(line)
        if p0 != p1:
            turtle.penup()
            turtle.goto(p0)
            draw_dot(p0,color='blue',size=6)
            turtle.pendown()
            turtle.goto(p1)
        if dots>0: draw_dot(p1,color=color,size=dots)


def draw_dot(loc,color='red',size=8):
    """put a dot at location loc"""
    turtle.penup()
    turtle.goto(loc)
    turtle.dot(size,color)


#Consider using turtle on click functionality to get a position of the click or drag and find
# The closest wall to that as the selection
if __name__=="__main__":
    boardSize = int(input("Input n for the nxn game grid: "))
    myGame = Game(boardSize)
    gameOver = False
    while not gameOver:
        gameOver = myGame.playGame(ruleSet = 1, playerTypes = [PlayerType.Human, PlayerType.Human])
    print("Game Over!")
    print(f"Final Score: Player1: {myGame.score[Owner.Player1]}, Player2: {myGame.score[Owner.Player2]}")
    input("Hit enter to Close the Gui")
