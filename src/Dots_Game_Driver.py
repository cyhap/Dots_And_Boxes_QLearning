# Dots Game Driver
import Dots, Dots_RandMove_Comp, Q_Learning_Comp_Alt
from keras.models import load_model
import pickle
if __name__ == "__main__":
    numEpochs = 1
    tDrawNow = True
    boardSize = int(input("Input n for the nxn game grid: "))
    print("There are 3 Player Type Options:\n 1 - Human\n 2 - Random Moves Comp\n 3 - Q Learning Comp")
    player1Type = int(input("Please Enter Player 1's Type: "))
    player2Type = int(input("Please Enter Player 2's Type: "))
    playerTypeMapping = {1: Dots.PlayerType.Human,
                         2: Dots.PlayerType.RandMoves,
                         3: Dots.PlayerType.QLearning
                        }
    playerTypes2Use = [playerTypeMapping.get(player1Type), playerTypeMapping.get(player2Type)]
    #Initialize Q Learning
    useFcnApprox = True
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
    mySmartComp = Q_Learning_Comp_Alt.Q_Learning_Comp(compInpParams, epsilon = 0, gamma = .5, seed = None)
    
    for tEpisode in range(numEpochs):
        myGame = Dots.Game(boardSize, tDrawNow)
        gameOver = False
        while not gameOver:
            aWall = mySmartComp.genMove(myGame)
            gameOver = myGame.playGame(ruleSet = 1, playerTypes = playerTypes2Use, wall2Update = aWall)
            if gameOver:
                print("Game Over!")
                print(f"Final Score: Player1: {myGame.score[Dots.Owner.Player1]}, Player2: {myGame.score[Dots.Owner.Player2]}")
    

