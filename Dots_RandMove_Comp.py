#Dots Random Moves Computer
import Dots, random
#Given a Game, a random wall is selected from the list of available walls

def gen_RandMove(aGame):
    aWall = []
    possibleMoves = [aSide for aSide in aGame.allSides if aSide.owner == Dots.Owner.NeitherPlayer]
    if possibleMoves:    
        aWall = random.choice(possibleMoves)
    
    return aWall
