# Table vs Fcn Approx Test
"""
This Script is used to play a computer that has a Q Table vs a Fcn Approx
to further assess which one is "better"
"""
import Dots, Dots_RandMove_Comp, Q_Learning_Comp_Alt, NN_Regression_Fcn_Approx
import CompvRand_Results
import pickle
from keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    numEpisodes = 1000
    tDrawNow = False
    boardSize = 3
    useFcnApprox = True
    numGamesPerUpdate = 1000
    numGamesPerRetrain = 10000
    playerTypes2Use = [Dots.PlayerType.QLearning, Dots.PlayerType.QLearning]
    #Initialize Q Learning
    #Using Dictionary's Defualt function I can make my Q tables without all of the states ahead of time.
    #The learned table data
    with open(f"comp{boardSize}x{boardSize}_QVals_{10000}.pkl", "rb") as filePtr: 
        tCompDict = pickle.load(filePtr)
    MasterQTable = tCompDict
    #MasterQTable = {} #Use this when starting from Scratch
    seed1 = None
    seed2 = None
    #Assign Player to Each Comp
    p1 = Dots.Owner.Player1
    p2 = Dots.Owner.Player2
    # Load the model that be used by the 2 Q Learners
    # This essentially loads a model to train from scratch
    numSq = boardSize*boardSize
    #model = NN_Regression_Fcn_Approx.regressionModel(boardSize) # No previous experience at all
    # Commented out below are other options of seeded functional approximations
    model = load_model("QComp_Table_Seeded.h5") # Using NN Approx of a Q Table
    #model = load_model("QComp_Learned.h5") # Using NN Approx of QvQ Training
    comp1InpParams = {}
    comp1InpParams["QTable"] = MasterQTable
    comp1InpParams["Player"] = p1
    comp1InpParams["boardSize"] = boardSize
    comp1InpParams["useFcnApprox"] = useFcnApprox
    comp1InpParams["model"] = model
    comp2InpParams = {}
    comp2InpParams["QTable"] = MasterQTable
    comp2InpParams["Player"] = p2
    comp2InpParams["boardSize"] = boardSize
    comp2InpParams["useFcnApprox"] = False
    comp2InpParams["model"] = model
    epsilon = 0.05
    mySmartComp1 = Q_Learning_Comp_Alt.Q_Learning_Comp(comp1InpParams, epsilon = epsilon, gamma = .75, seed = seed1)
    mySmartComp2 = Q_Learning_Comp_Alt.Q_Learning_Comp(comp2InpParams, epsilon = epsilon, gamma = .75, seed = seed2)
    ComputerDict = {Dots.Owner.Player1:mySmartComp1, 
                    Dots.Owner.Player2:mySmartComp2
                   }
    numP1Wins = 0
    numP2Wins = 0
    numDraws = 0
    for tEpisode in range(numEpisodes):
    
        myGame = Dots.Game(boardSize, tDrawNow, randomSeed = tEpisode)
        gameOver = False
        while not gameOver:
            tComp = ComputerDict[myGame.turn]
            aWall = tComp.genMove(myGame)
            gameOver = myGame.playGame(ruleSet = 1, playerTypes = playerTypes2Use, wall2Update = aWall)
            #tComp.updateQValues(myGame)
            if gameOver:
                if myGame.score[Dots.Owner.Player1] > myGame.score[Dots.Owner.Player2]:
                   numP1Wins = numP1Wins+1
                elif (myGame.score[Dots.Owner.Player2] > myGame.score[Dots.Owner.Player1]):
                   numP2Wins = numP2Wins+1
                else:
                   numDraws = numDraws+1
                if tDrawNow:
                    print("Game Over!")
                    print(f"Final Score: Player1: {myGame.score[Dots.Owner.Player1]}, Player2: {myGame.score[Dots.Owner.Player2]}")
                #mySmartComp1.reset(numGamesPerRetrain) # Reset the Stored State Action Pair to None
                #mySmartComp2.reset(numGamesPerRetrain) # Reset the Stored State Action Pair to None
    p1WinPercent = numP1Wins/numEpisodes
    p2WinPercent = numP2Wins/numEpisodes
    drawPercent = numDraws/numEpisodes
        
    objects = ('Q Fcn Approx', 'Q Table', 'Draws')
    ypos = np.arange(len(objects))
    performance = [p1WinPercent, p2WinPercent, drawPercent]
    plt.barh( ypos, performance, align='center', alpha=0.5)
    plt.yticks(ypos, objects)
    plt.xlabel("Number of Games Played")
    plt.ylabel("Percent Wins")
    plt.title(f"Q_Functional_Approximation vs Q Table {boardSize}x{boardSize}") 

    plt.show()
