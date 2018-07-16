#!/usr/bin/python3
import numpy as np
import random
import sys

def fill_array(a, pos):
    a[pos[0]] = 1       #fill horizontal
    a[:,pos[1]] = 1     #fill vertical
    a[pos] = 8          #queen position
    diag = get_diagonal(pos, [0,7])
    a[diag] = 1         #fill diagonal
    return a
    
def get_diagonal(pos, limits):
    pairs = []
    posY, posX = pos
    for way in [(1,1), (-1,-1), (1, -1), (-1, 1)]:
        while True:
            posY += way[0]
            posX += way[1]
            if limits[0] <= posX <= limits[1] and limits[0] <= posY <= limits[1]:
                pairs.append((posY, posX))
            else:
                posY, posX = pos
                break
    return list(zip(*pairs))
    
def nqueen_random(quiet=True):    
    board = np.zeros((8, 8))
    counter = 0
    positions = []
    for x in range(8):
        zeros = np.where(board == 0)
        zerosPoints = list(zip(list(zeros[0]), list(zeros[1])))
        if not zerosPoints:
            if not quiet:
                print("no place to put queen")
            break
        counter += 1
        pos = random.choice(zerosPoints)
        positions.append(pos)
        board = fill_array(board, pos)
        if not quiet:
            print("Number of Q: {}, current position: {}\n{}\n".format(counter, pos, board))
            input()
    return positions, board

def chess_positions(positions=[]):
    positions = list(zip(*positions))
    digits = dict(zip([str(x) for x in range(8)], [str(x) for x in range(1,9)]))
    alpha = dict(zip([str(x) for x in range(8)], list("abcdefgh")))
    new = list(zip([alpha[str(y)] for y in positions[1]], [digits[str(x)] for x in positions[0]]))
    new = ["".join(x) for x in new]
    return new
    
    
if __name__ == "__main__":
    for x in range(10):
        positions, board = nqueen_random(quiet=True)
        if len(positions) == 8:
            #print("Full number of queens. Positions:", positions)
            #print(board)
            break
    chess_pos = chess_positions(positions)            
    print(chess_pos)        
            
            