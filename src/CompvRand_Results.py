# Dots Game Driver
import Dots, Dots_RandMove_Comp, Q_Learning_Comp_Alt
#Get the Trained Q Models
import pickle
import numpy as np
from keras.models import load_model
#TODO ADD LEARING RATE Use 0.001 Play with the value
# Exploring Epsilon try about 10 - 50%
def assessPerformance(aComp, numGames, boardSize, aDrawNow):
    numP1Wins = 0
    numP2Wins = 0
    numDraws = 0
    playerTypes2Use = [Dots.PlayerType.RandMoves, Dots.PlayerType.QLearning]
    for tEpisode in range(numGames):
        myGame = Dots.Game(boardSize, aDrawNow, tEpisode)
        gameOver = False
        while not gameOver:
            aWall = aComp.genMove(myGame)
            gameOver = myGame.playGame(ruleSet = 1, playerTypes = playerTypes2Use, wall2Update = aWall)
            if gameOver:
                if aDrawNow:
                    print("Game Over!")
                    print(f"Final Score: Player1: {myGame.score[Dots.Owner.Player1]}, Player2: {myGame.score[Dots.Owner.Player2]}")
                if myGame.score[Dots.Owner.Player1] > myGame.score[Dots.Owner.Player2]:
                   numP1Wins = numP1Wins+1
                elif (myGame.score[Dots.Owner.Player2] > myGame.score[Dots.Owner.Player1]):
                   numP2Wins = numP2Wins+1
                else:
                   numDraws = numDraws+1
    p1WinPercent = numP1Wins/numGames
    p2WinPercent = numP2Wins/numGames
    drawPercent = numDraws/numGames
    tRet = (p1WinPercent, p2WinPercent, drawPercent)    
    print(f"Random Moves Won {p1WinPercent}% of the Time")
    print(f"Q Learned Moves Won {p2WinPercent}% of the Time")
    print(f"Draws Occured {drawPercent}% of the Time")
    return tRet


if __name__ == "__main__":
    numGames = 1000
    tDrawNow = False
    useFcnApprox = False
    boardSize = 3
    #Retrieve the Q Tables
    trainingSet = 10000
    with open(f"comp{boardSize}x{boardSize}_QVals_{trainingSet}.pkl", "rb") as filePtr: 
        tCompDict = pickle.load(filePtr)
    model = load_model("QComp_Table_Seeded.h5")
    #model = load_model("QComp_Learned.h5")
    compInpParams = {}
    compInpParams["QTable"] = tCompDict
    compInpParams["Player"] = Dots.Owner.Player2
    compInpParams["boardSize"] = boardSize
    compInpParams["useFcnApprox"] = useFcnApprox
    compInpParams["model"] = model
    
    # No more Exploring time to crush the opponent
    # Set epsilon to 0
    tComp = Q_Learning_Comp_Alt.Q_Learning_Comp(compInpParams, epsilon = 0, gamma = .5, seed = None)
    
    assessPerformance(tComp, numGames, boardSize, tDrawNow)
