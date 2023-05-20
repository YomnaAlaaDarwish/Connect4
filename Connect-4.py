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



def Assess_Value_Window(screen, bit):
    total = 0
    turnBit = Piece_Of_Computer
    if bit == Piece_Of_Computer:
        turnBit = Piece_Of_AI

    if screen.count(bit) == 4:
        total += 100
    elif screen.count(bit) == 3 \
            and screen.count(EMPTY) == 1:
        total += 5
    elif screen.count(bit) == 2 \
            and screen.count(EMPTY) == 2:
        total += 2

    if screen.count(turnBit) == 3 \
            and screen.count(EMPTY) == 1:
        total -= 4

    return total


def getAvailablePlaces(Board):
    avilablePlaces = []
    for Column in range(Count_Of_Column):
        if isAvailablePlace(Board, Column):
            avilablePlaces.append(Column)
    return avilablePlaces


def Check_Terminal_Node(GameBoard):
    return Verify_Game_Over(GameBoard, Piece_Of_Computer) or Verify_Game_Over(GameBoard, Piece_Of_AI) or len(
        getAvailablePlaces(GameBoard)) == 0


def selectMove(Board, P):
    availPlaces = getAvailablePlaces(Board)
    BScore = -10000  # best score
    BColumn = random.choice(availPlaces)
    for Column in availPlaces:
        Row = getNextRow(Board, Column)
        copyBoard = Board.copy()
        removePiece(copyBoard, Row, Column, P)
        Score = score_position(copyBoard, P)
        if Score > BScore:
            BScore = Score
            BColumn = Column

    return BColumn


def Minimax_Algo(GameBoard, difficulty_Level, isMax):
    avail = getAvailablePlaces(GameBoard)
    finallNode = Check_Terminal_Node(GameBoard)

    if finallNode or difficulty_Level == 0:
        if finallNode:
            if Verify_Game_Over(GameBoard, Piece_Of_AI):
                return (None, 100000000000000)
            elif Verify_Game_Over(GameBoard, Piece_Of_Computer):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(GameBoard, Piece_Of_AI))

    if isMax:
        intial = -math.inf
        randcolumn = random.choice(avail)
        for colmn in avail:
            Row = getNextRow(GameBoard, colmn)
            GameBoardCopy = GameBoard.copy()
            removePiece(GameBoardCopy, Row, colmn, Piece_Of_AI)
            score = Minimax_Algo(GameBoardCopy, difficulty_Level - 1, False)[1]
            if score > intial:
                intial = score
                randcolumn = colmn
        return randcolumn, intial

    else:  # Minimizing player
        intial = math.inf
        randcolumn = random.choice(avail)
        for colmn in avail:
            Row = getNextRow(GameBoard, colmn)
            GameBoardCopy = GameBoard.copy()
            removePiece(GameBoardCopy, Row, colmn, Piece_Of_Computer)
            score = Minimax_Algo(GameBoardCopy, difficulty_Level - 1, True)[1]
            if score < intial:
                intial = score
                randcolumn = colmn
        return randcolumn, intial


def AlphaBeta_Algo(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = getAvailablePlaces(board)
    is_terminal = Check_Terminal_Node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if Verify_Game_Over(board, Piece_Of_AI):
                return (None, 100000000000000)
            elif Verify_Game_Over(board, Piece_Of_Computer):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, Piece_Of_AI))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextRow(board, col)
            b_copy = board.copy()
            removePiece(b_copy, row, col, Piece_Of_AI)
            new_score = AlphaBeta_Algo(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextRow(board, col)
            b_copy = board.copy()
            removePiece(b_copy, row, col, Piece_Of_Computer)
            new_score = AlphaBeta_Algo(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def draw_board(board):
    for c in range(Count_Of_Column):
        for r in range(Count_Of_Row):
            pygame.draw.rect(screen, Blue, (c * S_SIZE, r * S_SIZE + S_SIZE, S_SIZE, S_SIZE))
            pygame.draw.circle(screen, Black, (
                int(c * S_SIZE + S_SIZE / 2), int(r * S_SIZE + S_SIZE + S_SIZE / 2)), RAD)

    for c in range(Count_Of_Column):
        for r in range(Count_Of_Row):
            if board[r][c] == Piece_Of_Computer:
                pygame.draw.circle(screen, Red_Color, (
                    int(c * S_SIZE + S_SIZE / 2), height - int(r * S_SIZE + S_SIZE / 2)), RAD)
            elif board[r][c] == Piece_Of_AI:
                pygame.draw.circle(screen, Yellow_color, (
                    int(c * S_SIZE + S_SIZE / 2), height - int(r * S_SIZE + S_SIZE / 2)), RAD)
    pygame.display.update()

#main#

board = MakeBoard()
displayBoard(board)

pygame.init()

S_SIZE = 100
myfont = pygame.font.SysFont("monospace", 75)
width = Count_Of_Column * S_SIZE
height = (Count_Of_Row + 1) * S_SIZE

size = (width, height)

RAD = int(S_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

MiniMax_Exec_time = []
AlphaBeta_Exec_time = []


def start(level, m):
    game_over = False
    turn = random.randint(Computer_Player, AI_Agent)
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, Black, (0, 0, width, S_SIZE))
                posx = event.pos[0]
                if turn == Computer_Player:
                    pygame.draw.circle(screen, Red_Color, (posx, int(S_SIZE / 2)), RAD)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, Black, (0, 0, width, S_SIZE))

            ### Performance
            if turn == Computer_Player:
                ST = time.time()
                col = random.choice(getAvailablePlaces(board))
                row = getNextRow(board, col)
                removePiece(board, row, col, Piece_Of_Computer)
                ET = time.time() - ST
                MiniMax_Exec_time.append(ET)

                if Verify_Game_Over(board, Piece_Of_Computer):
                    label = myfont.render("Computer wins!!", 1, Yellow_color)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn += 1
                turn = turn % 2

                displayBoard(board)
                draw_board(board)
            # # Ask for Player 2 Input
            if turn == AI_Agent and not game_over:
                if (m == 1):
                    startMinimax = time.time()
                    col, minimax_score = Minimax_Algo(board, level, True)
                    ET1 = time.time() - startMinimax
                    MiniMax_Exec_time.append(ET1)
                else:
                    startAlpha = time.time()
                    col, minimax_score = AlphaBeta_Algo(board, level, -math.inf, math.inf, True)
                    ET2 = time.time() - startAlpha
                    AlphaBeta_Exec_time.append(ET2)
                if isAvailablePlace(board, col):
                    # pygame.time.wait(500)
                    row = getNextRow(board, col)
                    removePiece(board, row, col, Piece_Of_AI)

                    if Verify_Game_Over(board, Piece_Of_AI):
                        label = myfont.render("Player 2 wins!!", 1, Yellow_color)
                        screen.blit(label, (40, 10))
                        game_over = True

                    displayBoard(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2

        if game_over:
            pygame.time.wait(3000)

        plt.plot(range(1, len(MiniMax_Exec_time) + 1), MiniMax_Exec_time, label='Minimax')
        plt.plot(range(1, len(AlphaBeta_Exec_time) + 1), AlphaBeta_Exec_time, label='Alpha-Beta')
        plt.xlabel('Move')
        plt.ylabel('Execution Time (seconds)')
        plt.title('Performance Mesaures')
        plt.legend()
        plt.show()


#####gui #####

def fun1():
    rect_output.config(text="applying minimax ")
    m = int(m_entry.get())
    start(m, 1)


def fun2():
    rect_output.config(text="applying alpha beta")
    m = int(m_entry.get())
    start(m, 2)


def fun3():
    rect_output.config(text="Minimax & alpha beta")
    m = int(m_entry.get())
    start(m, 1)
    start(m, 2)


root = Tk()
root.title('project')

# labels
m_label = Label(root, text='Enter difficulty level of the game:')
m_entry = Entry(root)

rect_output_label = Label(root, text='result:')

# output label
rect_output = Label(root, text="")
# button

create_board_btn = Button(root, text='minimax', command=fun1)
create_board_btn2 = Button(root, text='alpha-beta', command=fun2)
create_board_btn3 = Button(root, text='Minimax & alpha beta', command=fun3)

# grid
m_label.grid(row=0, column=0)
m_entry.grid(row=0, column=1)
create_board_btn.grid(row=6, column=0, columnspan=2)
create_board_btn2.grid(row=6, column=1, columnspan=1)
rect_output_label.grid(row=7, column=0)
rect_output.grid(row=8, column=1)

root.mainloop()