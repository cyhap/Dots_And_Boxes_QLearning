import numpy as np
from keras.models import Sequential
from keras.layers import Dense
#from keras.wrappers.scikit_learn import KerasRegressor
#from sklearn.model_selection import cross_val_score
#from sklearn.model_selection import KFold
#from sklearn.preprocessing import StandardScaler
#from sklearn.pipeline import Pipeline
# Use the following line to load the saved model
from keras.models import load_model
# Use to load Q Table Data 
import pickle

#Import Data for Training
def getDataFromQTable(tCompDict, boardSize):
    StActPairs = tCompDict.keys()
    numTrnPts = len(tCompDict)
    numPossibleMoves = 2*boardSize*(boardSize+1)
    numSquares = boardSize*boardSize
    inpDatLen = (numSquares * 4) + numPossibleMoves
    inputData = np.zeros((numTrnPts,inpDatLen))
    labelsData = np.zeros((numTrnPts,1))
    cnt = 0
    for stActPair in tCompDict:
        fcStAct = getInp(stActPair, boardSize)
        inputData[cnt][:] = fcStAct
        labelsData[cnt] = float(tCompDict[stActPair])
        cnt = cnt + 1
    return (inputData, labelsData)


def regressionModel(boardSize):
    # Create the Model Parameters
    numPossibleMoves = 2*boardSize*(boardSize+1)
    numSquares = boardSize*boardSize
    inpDatLen = (numSquares * 4) + numPossibleMoves
    layer1_Neurons = inpDatLen # FIXME Play with these numbers
    layer2_Neurons = 128
    layer3_Neurons = 64
    layer4_Neurons = 32
    layer5_Neurons = 16

    inputDim = inpDatLen
    # Create the Model
    model = Sequential()
    model.add(Dense(layer1_Neurons, input_dim=inputDim, kernel_initializer="normal", activation="relu"))
    model.add(Dense(layer2_Neurons, kernel_initializer="normal", activation="relu"))
    model.add(Dense(layer3_Neurons, kernel_initializer="normal", activation="relu"))
    model.add(Dense(layer4_Neurons, kernel_initializer="normal", activation="relu"))
    model.add(Dense(layer5_Neurons, kernel_initializer="normal", activation="relu"))
    # Want 1 value that will represent the Q Values as output
    model.add(Dense(1, kernel_initializer="normal"))

    model.compile(loss="mean_squared_error", optimizer='adam')
    return model

def getInp(stActPair, boardSize):
    numPossibleMoves = 2*boardSize*(boardSize+1)
    action = stActPair[1]
    action1Hot = np.zeros((1,numPossibleMoves))
    action1Hot[np.arange(1), action] = 1
    state  = stActPair[0]
    stateFC = []
    for onOff in state:
        for wall in onOff:
            stateFC.append(int(wall))
    fcStAct = np.concatenate((action1Hot,stateFC), axis = None )
    return fcStAct
        

if __name__ == "__main__":
    print("Libraries Loaded Properly")
    trainingSet = 10000
    boardSize = 2
    with open(f"comp{boardSize}x{boardSize}_QVals_{trainingSet}.pkl", "rb") as filePtr: 
        tCompDict = pickle.load(filePtr)    
    (inp, labels) = getDataFromQTable(tCompDict,boardSize)
    forPredictInp = inp[-1][:]
    forPredictCompare = labels[-1]

    #seed = 4321
    #np.random.seed(seed)
    #estimator = KerasRegressor(build_fn=regressionModel, epochs=3, batch_size=100, verbose=1)
    
    #kfold = KFold(n_splits=10, random_state=seed)
    #results = cross_val_score(estimator, inp, labels)#, cv=kfold)
    #print(f"Results MSE Mean: {results.mean()}, Std: {results.std()}")
    #print(f"All Results: {results}")
    model = regressionModel(boardSize)
    model.fit(inp, labels, epochs = 600, batch_size = len(inp)) #200 Epochs was used for 3x3 board
    #600 Epochs was used for the 2x2

    learnedOutput = model.predict(forPredictInp.reshape(len(forPredictInp),1).T)
    print(learnedOutput)
    print(forPredictCompare)
    #model.fit(forPredictInp.reshape(28,1).T, forPredictCompare, epochs = 10, batch_size=100)
    #learnedOutput = model.predict(forPredictInp.reshape(28,1).T)
    #print(learnedOutput)
    #print(forPredictCompare)
    
    model.save('QComp_Table_Seeded.h5')

