import numpy as np
import random
import pygame
import sys
import math
import random
from tkinter import *
import io
import sys
from tkinter import Tk
import time
import matplotlib.pyplot as plt

## Boards Coordinates
Count_Of_Row = 6
Count_Of_Column = 7

## colors Of Board
Blue = (0, 0, 255)
Black = (0, 0, 0)
Red_Color = (255, 0, 0)
Yellow_color = (255, 255, 0)

## Computer & AI agent
Computer_Player = 0
AI_Agent = 1

## Pices OF Players
EMPTY = 0
Piece_Of_Computer = 1
Piece_Of_AI = 2

Length_Of_Window = 4


###################


def Verify_Game_Over(Board, P):
    # Check horizontal locations for win
    for Column in range(Count_Of_Column - 3):
        for Row in range(Count_Of_Row):
            if Board[Row][Column] == P and Board[Row][Column + 1] == P and Board[Row][Column + 2] == P and Board[Row][
                Column + 3] == P:
                return True

    # Check vertical locations for win
    for Column in range(Count_Of_Column):
        for Row in range(Count_Of_Row - 3):
            if Board[Row][Column] == P and Board[Row + 1][Column] == P and Board[Row + 2][Column] == P and \
                    Board[Row + 3][Column] == P:
                return True

    # Check positively sloped diaganols
    for Column in range(Count_Of_Column - 3):
        for Row in range(Count_Of_Row - 3):
            if Board[Row][Column] == P and Board[Row + 1][Column + 1] == P and Board[Row + 2][Column + 2] == P and \
                    Board[Row + 3][Column + 3] == P:
                return True

    # Check negatively sloped diaganols
    for Column in range(Count_Of_Column - 3):
        for Row in range(3, Count_Of_Row):
            if Board[Row][Column] == P and Board[Row - 1][Column + 1] == P and Board[Row - 2][Column + 2] == P and \
                    Board[Row - 3][Column + 3] == P:
                return True


def removePiece(Board, Row, Column, P):
    Board[Row][Column] = P


def score_position(GameBoard, bit):
    totalPoint = 0

    ## Score center column
    array = [int(i) for i in list(GameBoard[:, Count_Of_Column // 2])]
    count = array.count(bit)
    totalPoint += count * 3

    ## Score Horizontal
    for r in range(Count_Of_Row):
        array_row = [int(i) for i in list(GameBoard[r, :])]
        for c in range(Count_Of_Column - 3):
            Screen = array_row[c:c + Length_Of_Window]
            totalPoint += Assess_Value_Window(Screen, bit)

    ## Score Vertical
    for c in range(Count_Of_Column):
        array_column = [int(i) for i in list(GameBoard[:, c])]
        for r in range(Count_Of_Row - 3):
            Screen = array_column[r:r + Length_Of_Window]
            totalPoint += Assess_Value_Window(Screen, bit)

    ## Score posiive sloped diagonal
    for r in range(Count_Of_Row - 3):
        for c in range(Count_Of_Column - 3):
            Screen = [GameBoard[r + i][c + i] for i in range(Length_Of_Window)]
            totalPoint += Assess_Value_Window(Screen, bit)

    for r in range(Count_Of_Row - 3):
        for c in range(Count_Of_Column - 3):
            Screen = [GameBoard[r + 3 - i][c + i] for i in range(Length_Of_Window)]
            totalPoint += Assess_Value_Window(Screen, bit)

    return totalPoint


def getNextRow(Board, Column):
    for Row in range(Count_Of_Row):
        if Board[Row][Column] == 0:
            return Row


def MakeBoard():
    Board = np.zeros((Count_Of_Row, Count_Of_Column))
    return Board


def displayBoard(Board):
    print(np.flip(Board, 0))


def isAvailablePlace(Board, Column):
    return Board[Count_Of_Row - 1][Column] == 0

################################################################################################################
