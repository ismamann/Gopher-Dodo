#!/usr/bin/python3

import ast
import argparse
import os
from typing import Dict, Any
from gndclient import start, Action, Score, Player, State, Time, DODO_STR, GOPHER_STR

# Environment = Dict[str, Any]


import math
from random import randint
from API import *
from Grid import *


# Class Environment pour le jeu en réseau.
class Environment:
    def __init__(
        self,
        dictPosition,
        game: str,
        state: State,
        player: Player,
        hex_size: int,
        time: Time,
    ):
        self.premierCoup = True
        self.dictPosition = dictPosition
        self.game = game
        self.state = state
        self.player = player
        self.hex_size = hex_size
        self.time = time
        self.cache = {}


# Init notre Dictionnaire de positions sur les positon du State donné par la boucle de jeu.
def initGridTournois(grid: State):
    cpt = 0
    for element in grid:
        coordonnees, valeur = element
        dictPosition[Position(coordonnees[0], coordonnees[1])] = cpt
        cpt += 1


emptyGrid = None


def initialize(
    game: str, state: State, player: Player, hex_size: int, total_time: Time
) -> Environment:
    """Cette fonction est lancée au début du jeu. Elle dit à quel jeu on joue,
    le joueur que l'on est et renvoie l'environnement,
    c'est-à-dire la structure de donnée (objet, dictionnaire, etc.) que vous utiliserez pour jouer.
    """
    global emptyGrid
    emptyGrid = state
    if game == "dodo":
        print("Jouons à Dodo !\n")
        print(f"Vous êtes le joueur {player}")
        # initalize_dodo(state, player, hex_size,total_time)
        # initGrid(hex_size)
        initGridTournois(state)
        return Environment(dictPosition, game, state, player, hex_size, total_time)
    elif game == "gopher":
        print("Jouons à Gopher !\n")
        print(f"Vous êtes le joueur {player}")
        # initalize_gopher(state, player, hex_size, total_time)
        # initGrid(hex_size)
        initGridTournois(state)
        return Environment(dictPosition, game, state, player, hex_size, total_time)
    else:
        raise ValueError("Veuillez entrer : 'dodo' ou 'gopher'")


# choix de la fonction legals en fonction du jeu.
def legals(game: str, grid: State, player: Player) -> list[Action]:
    if game == "gopher":
        return legals_gopher(grid, player)
    return legals_dodo(grid, player)


def legals_gopher(grid: State, player: Player) -> list[ActionGopher]:
    resultat = []
    for cellule, value in dictPosition.items():
        if grid[value][1] == 0:
            directions = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]
            x = cellule.x
            y = cellule.y
            caseValide = False
            for dx, dy in directions:
                if Position(x + dx, y + dy) in dictPosition:
                    valeur = grid[dictPosition[Position(x + dx, y + dy)]][1]
                    if valeur == player:
                        caseValide = False
                        break
                    elif valeur != player and valeur != 0:
                        if caseValide == True:
                            caseValide = False
                            break
                        caseValide = True
            if caseValide:
                resultat.append((cellule.x, cellule.y))
    return resultat


def legals_dodo(grid: State, player: Player) -> list[ActionDodo]:
    actions: list[ActionDodo] = []
    if player == 1:  # le rouge ne peut que monter
        directions = [(0, 1), (1, 1), (1, 0)]
    elif player == 2:  # le bleu ne peut que descendre
        directions = [(0, -1), (-1, -1), (-1, 0)]
    else:
        raise ValueError("joueur non valide")
    for cellule, value in dictPosition.items():
        if grid[value][1] == player:
            for dx, dy in directions:
                if Position(cellule.x + dx, cellule.y + dy) in dictPosition:
                    for cellule_adj, value_adj in dictPosition.items():
                        if cellule_adj.x == (cellule.x + dx) and cellule_adj.y == (
                            cellule.y + dy
                        ):
                            if grid[value_adj][1] == 0:
                                action: list[Cell, Cell] = []
                                action.append((cellule.x, cellule.y))
                                action.append((cellule_adj.x, cellule_adj.y))
                                actions.append(tuple(action))
    return actions


def final_result_minmax(state: State, score: Score, player: Player):
    # resultat = legals(state, 0, player)
    # if len(resultat) == 0 :
    if player == 1:
        return 2, state, -1
    return 1, state, 1

# Fonction final pour la boucle de jeu.
def final_result(state: State, score: Score, player: Player):
    print(f"Ending: {player} wins with a score of {score}")


def final_resultMCTS(state: State, score: Score, player: Player):
    if player == 1:
        return 2, state, -1
    return 1, state, 1


def changeJoueur(auTourDe):
    if auTourDe == 1:
        return 2
    return 1


def final(game: str, node: State, player: Player):
    return len(legals(game, node, player)) == 0

# joue une action.
def play(game: str, grid: State, player: Player, action: ActionGopher) -> State:
    copyGrid = []
    for i in grid:
        copyGrid.append(i)
    if game == "gopher":
        copyGrid[dictPosition[Position(action[0], action[1])]] = (
            (action[0], action[1]),
            player,
        )
    else:
        copyGrid[dictPosition[Position(action[0][0], action[0][1])]] = (action[0], 0)
        copyGrid[dictPosition[Position(action[1][0], action[1][1])]] = (
            action[1],
            player,
        )
    return copyGrid


memory = {} #pour le cache
cpt = 0 # pour comparer les appels avec et sans symetries de min max.


def memoize_minmax_alpha_beta(func_min_max_alpha_beta):
    def intern_memoize(game: str, node: State, player: Player, alpha, beta):
        global cpt
        tupleNode = tuple(node)
        if tupleNode not in memory:
            res = func_min_max_alpha_beta(game, node, player, alpha, beta)
            memory[tupleNode] = res
            saveSymmetry(tupleNode, res)
        return memory[tupleNode]

    return intern_memoize


@memoize_minmax_alpha_beta
def minmax_alpha_beta(game: str, node: State, player: Player, alpha, beta) -> float:
    global cpt
    cpt += 1
    if final(game, node, player):
        score = final_result_minmax(node, 0, player)[2]
        return score

    if player == 1:
        bestVal = -math.inf
        for child in legals(game, node, player):
            value = minmax_alpha_beta(
                game, play(game, node, player, child), changeJoueur(player), alpha, beta
            )
            bestVal = max(bestVal, value)
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        return bestVal

    else:
        bestVal = math.inf
        for child in legals(game, node, player):
            value = minmax_alpha_beta(
                game, play(game, node, player, child), changeJoueur(player), alpha, beta
            )
            bestVal = min(bestVal, value)
            beta = min(beta, bestVal)
            if beta <= alpha:
                break
        return bestVal

# enregistre les 6 symetries en pivotant de 60°. 
def saveSymmetry(node: State, score: Score):
    for i in range(5):
        copyGrid = []
        for case in emptyGrid:
            copyGrid.append(case)
        for case in node:
            if case[1] != 0:
                x = case[0][0]
                y = case[0][1]
                copyGrid[dictPosition[Position(y, y - x)]] = ((y, y - x), case[1])
        node = copyGrid
        memory[tuple(copyGrid)] = score
    return copyGrid

# prend la meilleure action possible.
def minmax_alpha_beta_action(game: str, grid: State, player: Player, depth: int = 0):
    resultat = [-math.inf, []]
    if player == 2:
        resultat[0] = math.inf
    for child in legals(game, grid, player):
        score = minmax_alpha_beta(
            game,
            play(game, grid, player, child),
            changeJoueur(player),
            -math.inf,
            math.inf,
        )
        if player == 1 and score > resultat[0]:
            resultat[0] = score
            resultat[1] = [child]
        elif player == 2 and score < resultat[0]:
            resultat[0] = score
            resultat[1] = [child]
        
    return resultat[1]

# Joue avec min max pour des petite grilles. Sinon avec MCTS avec 
# le nombre d'itérations qui varie.
def strategy(
    env: Environment, state: State, player: Player, time_left: Time
) -> tuple[Environment, Action]:
    if env.game == "gopher":
        if env.player == 1 and env.premierCoup == True:
            env.premierCoup = False
            return env, (0, 0)
        if env.hex_size <= 5:
            return env, minmax_alpha_beta_action(env.game, state, player, 0)
    nmcts = NodeMCTS(env.game, state, 0, 0, None, player, None)
    nmcts.expansion()
    res = nmcts.mcts(285)  # à changer pour lancement de Dodo : 500
    print(res.action)
    return env, res.action

# Class utilisée pour l'implémentation de MCTS.
class NodeMCTS:

    def __init__(
        self,
        game: str,
        grid: State,
        scoreMCTS,
        nbIter,
        parent,
        player: Player,
        action: Action,
    ):
        self.game = game
        self.grid = grid
        self.scoreMCTS = scoreMCTS
        self.nbIter = nbIter
        self.parent = parent
        self.child = None
        self.player = player
        self.action = action

    #Simulation.
    def playRandom(self, node: State, player: Player):
        if final(self.game, node, player):
            if self.player == player:
                return -1
            return 1
        leg = legals(self.game, node, player)
        return self.playRandom(
            play(self.game, node, player, leg[randint(0, len(leg) - 1)]),
            changeJoueur(player),
        )

    # Calcul de UCT.
    def uct(self):
        if self.scoreMCTS == 0 and self.nbIter == 0:
            return math.inf
        return (self.scoreMCTS / self.nbIter) + (
            math.sqrt(2 * (math.log(self.parent.nbIter) / self.nbIter))
        )

    # Séléction.
    def bestChildNode(self):
        resultat = [-math.inf, None]
        for fils in self.child:
            score = fils.uct()
            if (fils.scoreMCTS == 0 and fils.nbIter == 0) or (
                float(score) > resultat[0]
            ):
                resultat[0] = score
                resultat[1] = fils
        if resultat[1] == None:
            return [0, self]
        if resultat[1].nbIter != 0:
            if resultat[1].child != None:
                return resultat[1].bestChildNode()
            else:
                resultat[1].expansion()
                return resultat[1].bestChildNode()
        return resultat

    # Backpropagation.
    def backpropagation(self, scoreMCTS):
        self.scoreMCTS += scoreMCTS
        self.nbIter += 1
        if self.parent != None:
            self.parent.backpropagation(scoreMCTS)

    # Expansion.
    def expansion(self):
        res = []
        player2 = changeJoueur(self.player)
        for fils in legals(self.game, self.grid, self.player):
            res.append(
                NodeMCTS(
                    self.game,
                    play(self.game, self.grid, self.player, fils),
                    0,
                    0,
                    self,
                    player2,
                    fils,
                )
            )
        self.child = res

    # Boucle MCTS. 
    def mcts(self, nbIterMCTS: int):
        for i in range(nbIterMCTS):
            best = self.bestChildNode()[1]
            best.backpropagation(self.playRandom(best.grid, best.player))
        resultat = [0, []]
        for fils in self.child:
            if fils.nbIter > resultat[0]:
                resultat[0] = fils.nbIter
                resultat[1] = fils

        return resultat[1]


# initGrid(4)
# emptyGrid = grid
# print(legals([((-1, -1), 0), ((-1, -2), 0), ((-1, -3), 0), ((-1, 0), 0), ((-1, 1), 0), ((-1, 2), 0), ((-2, -1), 1), ((-2, -2), 0), ((-2, -3), 0), ((-2, 0), 0), ((-2, 1), 0), ((-3, -1), 0), ((-3, -2), 0), ((-3, -3), 0), ((-3, 0), 0), ((0, -1), 0), ((0, -2), 0), ((0, -3), 0), ((0, 0), 0), ((0, 1), 0), ((0, 2), 0), ((0, 3), 0), ((1, -1), 0), ((1, -2), 0), ((1, 0), 0), ((1, 1), 0), ((1, 2), 0), ((1, 3), 0), ((2, -1), 0), ((2, 0), 0), ((2, 1), 0), ((2, 2), 0), ((2, 3), 0), ((3, 0), 0), ((3, 1), 0), ((3, 2), 0), ((3, 3), 0)]
# , 2, False))
# grid[dictPosition[Position(0,0)]] = ((0,0), 1)
# print(strategy(None, grid, 2, None))
# nmcts = NodeMCTS("gopher",grid, 0, 0, None, 2, None)
# print(grid)
# print(dictPosition)
# print("\n\n")
# print(legals(grid, 1, True))
# print(grid)
# print("\n\n\n\n\n")
# print(play(grid, 2, (4,4)))
# print("\n\n\n\n\n")
# print(grid)
# p = play(grid, 1, (-3,-1))
# p = play(p, 1, (3,-1))
# print(p)
# print("\n\n")
# grid[dictPosition[Position(2,3)]] = ((2,3), 1)
# nmcts.grid = grid
# nmcts.expansion()
# test = nmcts.mcts(10000)
# print(test)
# print(test[1].action)
# print(nmcts)
# for i in nmcts.child :
#       print(str(i.scoreMCTS)+" "+str(i.nbIter)+" "+str(i)+" "+str(i.uct()))
# print(test[1].grid)

# print(saveSymmetry(p, 1))
# grid[dictPosition[Position(1,2)]] = ((1,2), 1)
# print(grid)
# grid[dictPosition[Position(4,5)]] = ((4,5), 1)
# print(minmax_alpha_beta_action("gopher", grid, 2, 0))
# print(cpt)
# print(cpt)
# print(minmax_alpha_beta_actions(grid, 1, 0))
# print(minmax_alpha_beta(grid, 2, -math.inf, math.inf))
# print(legals(grid, 1, False))
# printInitGrid()
# print(memory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ClientTesting", description="Test the IA02 python client"
    )

    parser.add_argument("group_id")
    parser.add_argument("members")
    parser.add_argument("password")
    parser.add_argument("-s", "--server-url", default="http://localhost:8080/")
    parser.add_argument("-d", "--disable-dodo", action="store_true")
    parser.add_argument("-g", "--disable-gopher", action="store_true")
    args = parser.parse_args()

    available_games = [DODO_STR, GOPHER_STR]
    if args.disable_dodo:
        available_games.remove(DODO_STR)
    if args.disable_gopher:
        available_games.remove(GOPHER_STR)

    start(
        args.server_url,
        args.group_id,
        args.members,
        args.password,
        available_games,
        initialize,
        strategy,
        final_result,
        gui=True,
    )
