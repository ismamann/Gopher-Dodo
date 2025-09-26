# Types de base utilisés par l'arbitre
from typing import Union
from Grid import *


#Environment =  str # Ensemble des données utiles (cache, état de jeu...) pour
                  # que votre IA puisse jouer (objet, dictionnaire, autre...)

Cell = tuple[int, int]
ActionGopher = Cell
ActionDodo = tuple[Cell, Cell] # case de départ -> case d'arrivée
Action = Union[ActionGopher, ActionDodo]
Player = int # 1 ou 2
State = list[tuple[Cell, Player]] # État du jeu pour la boucle de jeu
Score = int
Time = int

# class Environment:
#     def __init__(self, dictPosition, game:str, state: State, player:Player, hex_size: int, time:Time, nmcts : NodeMCTS):
#         self.dictPosition = dictPosition
#         self.game=game
#         self.state=state
#         self.player=player
#         self.hex_size=hex_size
#         self.time=time
#         self.cache={}
#         self.nmcts = nmcts
