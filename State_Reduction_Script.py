# State Reductions Script
from itertools import product, compress
import Dots
import Q_Learning_Comp_Alt

#Explore all the possible moves for a 2x2
#Combinations the walls could be turned on for a 2x2
comb = product([False,True], repeat = 12)
#everyGame =  permutations(wallIdxes)
playerTypes2use = [Dots.PlayerType.QLearning, Dots.PlayerType.QLearning]
masterStateSet = set()
masterStateSet2 = set()
#print(f"There are {len(list(everyGame))} different Game permutaions")
QTable = {}
for aComb in comb:
    idxAct = list(range(12))
    myGame = Dots.Game(2, False)
    allSides = set(myGame.allSides)
    sidesOwned = set(compress(myGame.allSides, aComb))
    sidesUnOwned = allSides - sidesOwned
    for aSide in sidesOwned:
        aSide.changeOwner(Dots.Owner.Player1)
    for aSide in sidesUnOwned:
        aSide.changeOwner(Dots.Owner.NeitherPlayer)
    #print(aState)
    #for aSide in myGame.allSides:
    #    print(aSide.owner)
    aState = Q_Learning_Comp_Alt.convGame2State(myGame)
    aAltState = Q_Learning_Comp_Alt.convGame2AltState(myGame)
    #masterStateSet.add(aState)
    availActs = []
    for avail in aComb:
        availActs.append(not avail)

    availActsbyIdx = list(compress(idxAct, availActs))
    tStateActionPair = (aAltState, list(compress(idxAct, availActs)))
    #Initialize Table Values to 0
    for aAvailAct in availActsbyIdx:
        QTable[(aAltState, aAvailAct)] = 0
    masterStateSet2.add(aAltState)

    # Apply all applicable actions to each state
    #for aState in masterStateSet2:
    #sidesUnOwned       
    #input(aState)
    
#print(f"There are {len(masterStateSet)} states now")
print(f"There are {len(masterStateSet2)} alternate states now")
print(f"There are {len(QTable)} State Action Pairs now")
#print(masterStateSet)
#print(masterStateSet2)
with open("StateSet2x2.py", "w") as filePtr:
    #filePtr.write(f"if __name__ == \"__main__\":\n")
    filePtr.write(f"masterStateSet = {masterStateSet}\n")
    filePtr.write(f"masterStateSet2 = {masterStateSet2}\n")
    #filePtr.write(f"a = {[1 2 3]}\n")
    filePtr.write(f"QTable = {QTable}\n")
