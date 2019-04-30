"""
This Script is used to do the Q Training
It uses to QLearning Agents that share a Q table
Because they are separate agents each agent remembers
the last SA pair it saw when it comes time to update.
However as they play each other all of the values within that
table are modified.
Once training is complete either the Q table or NN model that
was used as a functional approximation of the Q table is saved
for result assessment and seeding of other training.
There are a few switches available.
    - numEpidoes: Number of games the agents play against each other
    - tDrawNow: Provide output and a graphic visualization of what is happening during the games
    - boardSize: Size of the nxn board
    - useFcnApprox: True - A NN model will be used to as a functional approximation of the Q table
                    False - A Q Table will be used
    - numGamesPerUpdate: This parameter is only relevant when using the functional approximation.
                         It determines how often a new NN will be generated/trained
These switches are provided in the first few lines of the "Main" check.
Note the seeding was added for debugging purposes only. Feel free to change seeds or set them to None
for no seeding at all.

Set numGames per update equal to numEpisodes to used an input functional approximation model for the
duration of training.
"""
import Dots, Dots_RandMove_Comp, Q_Learning_Comp_Alt, NN_Regression_Fcn_Approx
import CompvRand_Results
import pickle
from keras.models import load_model
import matplotlib.pyplot as plt

if __name__ == "__main__":
    numEpisodes = 10000
    tDrawNow = False
    boardSize = 2
    useFcnApprox = True
    numGamesPerUpdate = 250
    numGamesPerRetrain = 250
    playerTypes2Use = [Dots.PlayerType.QLearning, Dots.PlayerType.QLearning]
    #Initialize Q Learning
    #Using Dictionary's Defualt function I can make my Q tables without all of the states ahead of time.
    #The Q Learning Computers will Share a Dictionary
    #The following two lines are only applicable for the seeding of a 3x3 with a 2x2
    #with open(f"comp3x3_QVals_Converted.pkl", "rb") as filePtr: 
    #    tCompDict = pickle.load(filePtr)
    with open(f"comp{boardSize}x{boardSize}_QVals_{numEpisodes}.pkl", "rb") as filePtr: 
        tCompDict = pickle.load(filePtr)
    MasterQTable = tCompDict
    #MasterQTable = {} #Use this when starting from Scratch
    seed1 = 1234
    seed2 = 5678
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
    comp2InpParams["useFcnApprox"] = useFcnApprox
    comp2InpParams["model"] = model
    epsilon = .1
    mySmartComp1 = Q_Learning_Comp_Alt.Q_Learning_Comp(comp1InpParams, epsilon = epsilon, gamma = .75, seed = seed1)
    mySmartComp2 = Q_Learning_Comp_Alt.Q_Learning_Comp(comp2InpParams, epsilon = epsilon, gamma = .75, seed = seed2)
    ComputerDict = {Dots.Owner.Player1:mySmartComp1, 
                    Dots.Owner.Player2:mySmartComp2
                   }
    numGamesAssessed = 100 # Num games used to check performance against a random player
    performancePtsP1 = []
    performancePtsP2 = []
    performancePtsDr = []
    gamesAtPts = []
    for tEpisode in range(numEpisodes):
        myGame = Dots.Game(boardSize, tDrawNow, randomSeed = tEpisode)
        gameOver = False
        while not gameOver:
            tComp = ComputerDict[myGame.turn]
            aWall = tComp.genMove(myGame)
            gameOver = myGame.playGame(ruleSet = 1, playerTypes = playerTypes2Use, wall2Update = aWall)
            tComp.updateQValues(myGame)
            if gameOver:
                if tDrawNow:
                    print("Game Over!")
                    print(f"Final Score: Player1: {myGame.score[Dots.Owner.Player1]}, Player2: {myGame.score[Dots.Owner.Player2]}")
                mySmartComp1.reset(numGamesPerRetrain) # Reset the Stored State Action Pair to None
                mySmartComp2.reset(numGamesPerRetrain) # Reset the Stored State Action Pair to None
        if tEpisode%numGamesPerUpdate == 0:
            mySmartComp1.epsilon = 0 # Set to 0 so it makes the best moves
            (p1Ws, p2Ws, draws) = CompvRand_Results.assessPerformance(mySmartComp1, numGamesAssessed, boardSize, tDrawNow)
            performancePtsP1.append(p1Ws*100)
            performancePtsP2.append(p2Ws*100) 
            performancePtsDr.append(draws*100)
            gamesAtPts.append(tEpisode)
            mySmartComp1.epsilon = epsilon # Reset it back
            

    #for states in mySmartComp1.QTable:
    #    print (f"{states}: {mySmartComp1.QTable[states]}")
    print(f"This is the len of the Dict {len(mySmartComp1.QTable)}")
    #for states in mySmartComp2.QTable:
    #    print (f"{states}: {mySmartComp2.QTable[states]}")
    if not useFcnApprox:
        outFile = f"comp{boardSize}x{boardSize}_QVals_{numEpisodes}.pkl"
        print(f"Writing results to {outFile}")
        with open(outFile, "wb") as filePtr:
            pickle.dump(mySmartComp1.QTable, filePtr)
            pickle.dump(mySmartComp2.QTable, filePtr)
    mySmartComp1.saveModel()
    randMovePlt, = plt.plot(gamesAtPts, performancePtsP1, 'r-o', label = 'Random Moves')
    QLearnPlt,   = plt.plot(gamesAtPts, performancePtsP2, 'b-o', label = 'Q Learner')
    DrawsPlt,    = plt.plot(gamesAtPts, performancePtsDr, 'g-o', label = 'Draws')
    handles = [randMovePlt, QLearnPlt, DrawsPlt]
    plt.legend(handles = handles)
    plt.xlabel("Number of Games Trained")
    plt.ylabel("Percent Wins")
    plt.title(f"Performance vs Training Board Size: {boardSize}") 
    plt.legend(handles = handles)
    plt.show()
