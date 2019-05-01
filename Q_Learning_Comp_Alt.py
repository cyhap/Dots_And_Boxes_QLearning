from enum import Enum
from itertools import permutations
import Dots 
import numpy as np
import NN_Regression_Fcn_Approx


class Q_Learning_Comp:
    def __init__(self, inpDict,  epsilon = .05, gamma = .5, seed = 1):   
        self.QTable = inpDict["QTable"]
        self.gamma = gamma
        self.epsilon = epsilon
        self.owner = inpDict["Player"]
        self.boardSize = inpDict["boardSize"] 
        self.numSq = (inpDict["boardSize"] * inpDict["boardSize"])
        self.model = inpDict["model"]
        self.useFcnApprox = inpDict["useFcnApprox"]
        self.GamesPlayed = 0
        self.savedPair = [] #FIXME REMOVE
        if seed:
            np.random.seed(seed)

    def updateQValues(self, aGame): 
        # Get Q'
        reward = aGame.reward
        newState = getState(aGame)
        possibleActions = getActions(aGame)
        tQvalsList = []
        for aAct in possibleActions:
            tStActPair = (newState, aAct)
            # Unseen values will have Q value of 0
            tQvalsList.append(self.QTable.get(tStActPair, 0))
        QPrime = 0
        if tQvalsList:
            QPrime = max(tQvalsList)
        beta = 1
        #beta = -1
        #if self.owner == aGame.turn: # Determine if its their turn again
        #    beta = 1
        self.QTable[self.currentSA] = reward + beta*QPrime*self.gamma
        #print(f"Dict is {len(self.QTable)} long")
        #print("This is the state action pair being updated")
        #print(self.currentSA)
        #input(self.QTable[self.currentSA])
        
    def reset(self, numGamesPerUpdate):
        self.currentSA = None
        self.GamesPlayed = self.GamesPlayed + 1
        if (self.GamesPlayed % numGamesPerUpdate == 0 and self.useFcnApprox):
            #Update Model using the dictionary that has been built up
            #input("I think its working?")
            (inp, labels) = NN_Regression_Fcn_Approx.getDataFromQTable(self.QTable, self.boardSize)
            self.model.fit(inp, labels, epochs = 200, batch_size=len(self.QTable), verbose = 0)
            #600 for 2x2
            #200 for 3x3
            
        
    def genMove(self, aGame):
        currentState = getState(aGame)
        possibleActions = getActions(aGame)
        numActions = len(possibleActions)
        numSquares = self.numSq
        numPossibleMoves = 2*self.boardSize*(self.boardSize+1)
        inpDatLen = (numSquares * 4) + numPossibleMoves
        # Get all possible resulting states from the actions
        #possibleNewStates = getNextState(aGame, possibleActions)
        #input(f"There are {numActions} Actions")
        tQvalsList = []
        if self.useFcnApprox: tVals2Predict = np.zeros((numActions,inpDatLen))
        cnt = 0
        for aAct in possibleActions:
            tStActPair = (currentState, aAct)    
            if self.useFcnApprox:
                tVal2Pred = NN_Regression_Fcn_Approx.getInp(tStActPair, self.boardSize)
                tVals2Predict[cnt][:] = tVal2Pred
                cnt = cnt + 1
            else:
                # Unseen values will have Q value of 0
                tQvalsList.append(self.QTable.get(tStActPair,0))
        if self.useFcnApprox: tQvalsList = self.model.predict(tVals2Predict)
        #input(tQvalsList)
        #input(f"These are the Possible Actions: {possibleActions}")
        tQvals = np.asarray(tQvalsList)
        #Assign probabilities
        maxIdx = np.argmax(tQvals)
        probMaxVal = (1-self.epsilon) + (self.epsilon/numActions)
        probNonMax = self.epsilon / numActions
        probVals = [probNonMax]*numActions
        probVals[maxIdx] = probMaxVal
        #print(probVals)
        #input(tQvals)
        actionChoice = np.random.choice(a = numActions, size = 1,  p = probVals)
        #print(f"This is the BEST choice: {maxIdx}")
        #input(f"The Action Choice was: {actionChoice}")
        # Save the State and Action Selected
        self.currentSA = (currentState, possibleActions[int(actionChoice)])
        #print("This is the state action pair that was chosen:")
        #input(self.currentSA)
        return aGame.allSides[possibleActions[int(actionChoice)]]
    
    def saveModel(self):
        self.model.save('QComp_Learned.h5')        

    #return allStates
def getState(aGame, stateMethod = 2):
    if stateMethod == 1:
        return convGame2State(aGame)
    else :
        return convGame2AltState(aGame)

def getActions(aGame):
    unownedSides = [] 
    for aSideIdx in range(len(aGame.allSides)):
        if aGame.allSides[aSideIdx].owner == Dots.Owner.NeitherPlayer:
            unownedSides.append(aSideIdx)
    # Shuffled the possible actions because taking the
    # actions in this order was biasing the Q table data
    np.random.shuffle(unownedSides)
    return unownedSides

def getNextState(aGame, possibleActions):
    nextStates = []
    for aWall in possibleActions:
        aWall.owner = Dots.Owner.Player1 # Change the Owner to assess the state
        nextStates.append(getState(aGame))
        aWall.owner = Dots.Owner.NeitherPlayer # Change the owner back to neither
    return nextStates
   
def convGame2State(aGame):
    tReturnStateList = []
    for aSq in aGame.allSquares:
        unownedSides = [x for x in aSq.sideList if x.owner == Dots.Owner.NeitherPlayer]
        numSides = 4-len(unownedSides)
        tReturnStateList.append(numSides)
        #tReturnStateList.sort()
        tReturnStateTuple = tuple(tReturnStateList)
    return tReturnStateTuple

def convGame2AltState(aGame):
    tReturnStateList = []
    for aSq in aGame.allSquares:
        sqStateList = []
        for aSide in aSq.sideList:
            if aSide.owner == Dots.Owner.NeitherPlayer:
                sqStateList.append(False)
            else :
                sqStateList.append(True)
        tReturnStateList.append(tuple(sqStateList))
    return tuple(tReturnStateList)
        
def convStActPair4model(stActPair):
        action = stActPair[1]
        action1Hot = np.zeros((1,12))
        action1Hot[np.arange(1), action] = 1
        state  = stActPair[0]
        stateFC = []
        for onOff in state:
            for wall in onOff:
                stateFC.append(int(wall))
        fcStAct = np.concatenate((action1Hot,stateFC), axis = None )
        return fcStAct
