import random
import copy

class Stack:
    def __init__(self, nb_cards: int):
        self.stack = [i + 1 for i in range(nb_cards)]

    def shuffle(self):
        random.shuffle(self.stack)

    def pick(self, nb_to_pick: int):
        popped = []
        for _ in range(nb_to_pick):
            popped.append(self.stack.pop())

        return popped

def findSuitesInList(l: list[int]) -> list[list[int]]:
    suites = []
    last_suite = []
    last_number = 0

    for i, number in enumerate(l):
        if i == 0 or number == last_number + 1:
            last_suite.append(number)
        else:
            suites.append(copy.deepcopy(last_suite))
            last_suite = [number]

        last_number = number

    suites.append(copy.deepcopy(last_suite))
    last_suite = [number]

    return suites

def getPointsForSuite (suite: list[int]) -> int:
    match len(suite):
        case 2: return 1
        case 3: return 4
        case 4: return 16
        case 5: return 64
        case _: return 0


class Player:
    def __init__(self, id):
        self.id = id
        self.stack = Stack(10) # TODO
        self.stack.shuffle()

    def pickCards(self):
        picked_cards = self.stack.pick(5)
        picked_cards.sort()
        suites = findSuitesInList(picked_cards)
        return sum(map(getPointsForSuite, suites))


def jouerUnePartie(player: Player):
    points = player.pickCards()
    print(player.id, "=>", points) # Not definitive

    return points

def jouerParties(nb_players: int = 9):

    # Create a list of players with an id based on their index
    players = [Player("player:" + str(i+1)) for i in range(nb_players)]

    winningPlayers = []
    maxEarnedPoints = 0


    # Play a round for each player
    for player in players:
        points = jouerUnePartie(player)

        if points > maxEarnedPoints:
            winningPlayers = [ player.id ]
            maxEarnedPoints = points
        elif points == maxEarnedPoints:
            winningPlayers.append(player.id)

    print("winningPlayers", winningPlayers)

try:
    nb_players = int(input("Combien de joueurs vont jouer ?"))
    jouerParties(nb_players)
except:
    jouerParties()
