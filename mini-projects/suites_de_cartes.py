import random
import copy

# Cette classe représente une pile de cartes
class Stack:
    def __init__(self, nb_cards: int):
        # Créer une liste de de 0 à nb_cards
        self.stack = [i + 1 for i in range(nb_cards)]

    def shuffle(self):
        random.shuffle(self.stack)

    def pick(self, nb_to_pick: int):
        """Retourne nb_to_pick cartes au hasard (ne les enlèves pas de la pile de cartes)."""
        return self.stack[-nb_to_pick:]

def findSuitesInList(l: list[int]) -> list[list[int]]:
    suites = []     # Suites trouvées
    last_suite = [] # Dernière suite trouvé (sera changé lors de l'iteration sur l)
    last_number = 0 # Dernier nombre sur lequel on a itéré

    # i est l'index du nombre actuel et number est le nombre
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
    """Retourne le nombre de point en fonction de la longueur de la suite donnée en paramètre."""
    match len(suite):
        case 2: return 1
        case 3: return 4
        case 4: return 16
        case 5: return 64
        case _: return 0

# Cette classe représente un joueur
class Player:
    def __init__(self, id):
        self.id = id           # Identifiant du joueur
        self.stack = Stack(32) # La pile de carte de ce joueur
        self.stack.shuffle()
        self.points = 0        # Les points gagnés au fil des parties

    def pickCards(self):
        return self.stack.pick(5)


def suites_to_str(suites: list[(list[int], int)]):

    def suite_to_str(suite: list[int]):
        """Converti une suite de nombre en une chaîne de caractères."""
        if len(suite) <= 1: return ""
        return f"suite de {len(suite)} cartes"

    # Liste de toutes les suites sous forme de chaîne de caractère (sauf les chaînes vides)
    suites_as_str = list(filter(None, list(map(lambda x: suite_to_str(x[0]), suites))))

    match len(suites_as_str):
        case 0: return "--> pas de suite => 0"
        case _: return "--> " + " et ".join(suites_as_str) + f" => {sum(map(lambda x: x[1], suites))}"


def jouerUnePartie(player: Player):
    picked_cards = player.pickCards()       # Cartes piochées par le joueur
    sorted_cards = sorted(picked_cards)     # Cartes piochées et triées
    suites = findSuitesInList(sorted_cards) # Liste des suites présentes dans les cartes piochées


    # Créer une suite de tuple. La première valeur tu tuple est la suite et la seconde valeur est le nombre de points que rapporte cette suite.
    suites_with_earned_points = []
    total_earned_points = 0

    for suite in suites:
        earned_points = getPointsForSuite(suite)
        suites_with_earned_points.append((suite, earned_points))
        total_earned_points += earned_points


    # Display
    print(f"{player.id}    Cartes={str(picked_cards) : <25} {str(sorted_cards) : <25} {suites_to_str(suites_with_earned_points)} points")

    return total_earned_points


def getWinningPlayer(players: list[Player]):
    winning_players = []
    max_earned_points = 0

    for player in players:
        if player.points > max_earned_points:
            winning_players = [ player.id ]
            max_earned_points = player.points
        elif player.points == max_earned_points:
            winning_players.append(player.id)

    return winning_players

def jouerParties(players: list[Player]):

    # Play a round for each player
    for player in players:
        player.points += jouerUnePartie(player)

    # Demande à l'utilisateur si il veut rejouer
    print("\n   ------------------------   ")
    replay = str(input("Voulez-vous rejouer ? : "))
    print("   ------------------------   \n")

    if replay.lower() == "oui":
        return jouerParties(players) # Rejoue

    # Affiche les points de tous les joueurs
    for player in sorted(players, key = lambda x: x.points):
        print(f"{player.id}: {player.points} points")

    # Affiche le ou les joueurs gagnants
    winning_players = getWinningPlayer(players)
    print("Le joueur gagnant est :", " et ".join(winning_players))


# Le programme commence ici
try:
    nb_players = int(input("Combien de joueurs vont jouer ?: "))
except:
    nb_players = 9

# Create a list of players with an id based on their index
players = [Player("Joueur " + str(i+1)) for i in range(nb_players)]

jouerParties(players)
