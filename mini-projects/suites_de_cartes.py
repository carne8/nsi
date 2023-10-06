import random
import copy

class Stack:
    def __init__(self, nb_cards: int):
        self.stack = [i + 1 for i in range(nb_cards)]

    def print(self):
        print(self.stack)

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

    print(l)
    print(suites)

    return suites

def getPointsForSuite (suite: list[int]) -> int:
    match len(suite):
        case 2: return 1
        case 3: return 4
        case 4: return 16
        case 5: return 64
        case _: return 0


class Player:
    def __init__(self):
        self.stack = Stack(32)
        self.stack.shuffle()

    def pickCards(self):
        picked_cards = self.stack.pick(5)
        picked_cards.sort()
        suites = findSuitesInList(picked_cards)
        return sum(map(getPointsForSuite, suites))

# nb_players = int(input("Combien de joueurs vont jouer ?"))
# nb_parties = int(input("Combien de parties allons nous jouer ?"))

def playAParty(nb_players: int = 9):
    players = [("player:" + str(i+1), Player()) for i in range(nb_players)]

    for (playerId, player) in players:
        print(player.pickCards())

        # Play round
        # round_results[player_id] = player.pickCards

    # print(round_results)


playAParty()
# print(findSuitesInList([0,1,2,3,6,7,8,12]))
