from cmath import sqrt
from collections import namedtuple
from API import *

dictPosition = {}
Position = namedtuple('Position', 'x y')
affichage = ''
# def printInitGrid(dimension) :
#     Position = namedtuple('Position', 'x y')
#     grid = []
#     millieu = dimension - 1
#     dimension2D = (dimension*2) - 1
#     for ligne in range(dimension2D) :
#         affichage = ''
#         tmp = []
#         for colonne in range(dimension2D) :
#             if ligne <= millieu and colonne <= millieu :
#                 if (millieu - 1 - colonne) < ligne :  
#                    if colonne == millieu : 
#                       affichage += str(millieu - colonne)+','+str(millieu - ligne)+'|'
#                       tmp.append(Position(millieu - colonne, millieu - ligne))
#                       dictPosition[Position(millieu - colonne, millieu - ligne)] = Position(ligne,colonne)
#                    else : 
#                        affichage += str(colonne - millieu)+','+str(millieu - ligne)+'|'
#                        tmp.append(Position(colonne - millieu, millieu - ligne))
#                        dictPosition[Position(colonne - millieu, millieu - ligne)] = Position(ligne,colonne)

#                 else :  
#                     affichage += 'None|'
#                     tmp.append(None)

#             elif ligne <= millieu and colonne > millieu :
#                 affichage += str(colonne - millieu)+','+str(millieu-ligne)+'|'
#                 tmp.append(Position(colonne - millieu, millieu - ligne))
#                 dictPosition[Position(colonne - millieu, millieu - ligne)] = Position(ligne,colonne)

#             elif ligne > millieu and colonne <= millieu :
#                 affichage += str(colonne - millieu)+','+str(millieu - ligne)+'|'
#                 tmp.append(Position(colonne - millieu, millieu - ligne))
#                 dictPosition[Position(colonne - millieu, millieu - ligne)] = Position(ligne,colonne)
#             else :
#                 if (dimension2D - colonne) > ligne - millieu : 
#                     affichage += str(colonne - millieu)+','+str(millieu - ligne)+'|'
#                     tmp.append(Position(colonne - millieu, millieu - ligne))
#                     dictPosition[Position(colonne - millieu, millieu - ligne)] = Position(ligne,colonne)
#                 else :  
#                     affichage += 'None|'
#                     tmp.append(None)
#         grid.append(tmp)

#         print(affichage)
#     return grid


grid = []
gridDrawHexa = []
def initGrid(dimension) :
    global affichage
    #grid = []
    #gridDrawHexa = []
    millieu = dimension - 1
    dimension2D = (dimension*2) - 1
    cpt = 0
    for ligne in range(dimension2D) :
        tmp = []
        for colonne in range(dimension2D) :
            if ligne <= millieu and colonne <= millieu :
                if (millieu - 1 - colonne) < ligne :  
                   if colonne == millieu : 
                      affichage += str(millieu - colonne)+','+str(millieu - ligne)+'|'
                      grid.append(((millieu - colonne, millieu - ligne), 0))
                      dictPosition[Position(millieu - colonne, millieu - ligne)] = cpt
                      tmp.append((millieu - colonne, millieu - ligne))
                   else : 
                       affichage += str(colonne - millieu)+','+str(millieu - ligne)+'|'
                       grid.append(((colonne - millieu, millieu - ligne), 0))
                       dictPosition[Position(colonne - millieu, millieu - ligne)] = cpt
                       tmp.append((colonne - millieu, millieu - ligne))

                else :  
                    affichage += 'None|'
                    tmp.append(None)
                    cpt -= 1

            elif (ligne <= millieu and colonne > millieu) or (ligne > millieu and colonne <= millieu) or ((dimension2D - colonne) > ligne - millieu):
                affichage += str(colonne - millieu)+','+str(millieu-ligne)+'|'
                grid.append(((colonne - millieu, millieu - ligne), 0))
                dictPosition[Position(colonne - millieu, millieu - ligne)] = cpt
                tmp.append((colonne - millieu, millieu - ligne))
            
            else :  
                affichage += 'None|'
                tmp.append(None)
                cpt -= 1
            cpt += 1
        gridDrawHexa.append(tmp)
        affichage += '\n'

    return grid

def printInitGrid() :
    print(affichage)


def estAdjacent(x1, y1, x2, y2) -> bool :
    directions = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]
    
    for dx, dy in directions:
        if (x2 == x1 + dx) and (y2 == y1 + dy):
            return True
    return False    

def trouveAdjacence(x, y) :
    directions = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]
    res = []
    for dx, dy in directions:
        if Position(x + dx, y + dy) in dictPosition :
            res.append(Position(x + dx, y + dy))
    return res    


def coorDrawHexa(ligneDraw : int, colonneDraw : int) :
    stop = ligneDraw
    res = []
    for i in range(colonneDraw, stop-1, -1) :
        res.append(gridDrawHexa[ligneDraw][i])
        ligneDraw += 1
    return res

def tabDrawHexa(dimension) :
    res = []
    for i in range(dimension-1, (dimension*2) -1) :
        res.append(coorDrawHexa(0, i))
    
    for i in range(dimension - 1) :
        res.append(coorDrawHexa(i+1, (dimension*2) -2))
    return res

# p = initGrid(4)
# #print(p)
# printInitGrid()
# print(tabDrawHexa(4))
#print(coorDrawHexa(4, 6))
# printInitGrid()
# print(dictPosition[Position(0,6)])
# print(dictPosition[Position(-4,-3)])
# print(dictPosition[Position(6,6)])
# print(p[95])
# print(estAdjacent(4,4,3,2))
# print(trouveAdjacence(4,4))