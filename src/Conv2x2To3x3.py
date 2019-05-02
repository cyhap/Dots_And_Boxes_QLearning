# Script to take saved 2x2 Table and modify it to seed a 3x3 Q Table
import pickle
import numpy as np


#Retrieve the Q Tables
boardSize = 2
trainingSet = 10000
with open(f"comp{boardSize}x{boardSize}_QVals_{trainingSet}.pkl", "rb") as filePtr: 
    tCompDict = pickle.load(filePtr)
tNewDict = {}
for stActPair in tCompDict:
    #Modify the key to be for a 3x3 instead of a 2x2
    action = stActPair[1]
    if action > 6:
        action = action+3
    state  = stActPair[0]
    newState = []
    #Copy right side of top right square in 2x2 to left side of top right square in 3x3
    aSq = state[1]
    aSqTopRight = aSq[2]
    #Similarly for Mid right
    aSq = state[3]
    aSqMidRight = aSq[2]
    aSqMidBot = aSq[3]
    #Same for mid left
    aSq = state[2]
    aSqMidLeftBot = aSq[3]
    #Start Filling New State Representation
    newState.append(state[0])
    newState.append(state[1])
    sqState = (aSqTopRight, False, False, False)
    newState.append(sqState)
    newState.append(state[2])
    newState.append(state[3])
    sqState = (aSqMidRight, False, False, False)
    newState.append(sqState)
    sqState = (False, aSqMidLeftBot, False, False)
    newState.append(sqState)
    sqState = (False, aSqMidBot, False, False)
    newState.append(sqState)
    sqState = (False, False, False, False)
    newState.append(sqState)
    newState = tuple(newState)
    newStActPair = (newState, action)
    tNewDict[newStActPair] = tCompDict[stActPair]
    
# Write out dictionary    
outFile = f"comp3x3_QVals_Converted.pkl"
print(f"Writing results to {outFile}")
with open(outFile, "wb") as filePtr:
    pickle.dump(tNewDict, filePtr)
    
