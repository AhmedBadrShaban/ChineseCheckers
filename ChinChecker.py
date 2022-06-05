# https://www.redblobgames.com/grids/hexagons/
import cProfile
import functools
import time
import numpy as np

import GameBoard

class Player:
    def __init__(self, id,goal ):
        self.id = id
        self.goal = goal

    def __str__(self):
        return str(self.id)


class Game:
    def do(self, move, board):
        board.move(*move[0], *move[1])

    def undo(self, move, board):
        board.move(*move[1], *move[0])

    def allAvailableMoves(self, board , player):
        for (colm, row) in board.iterate():
            cell = board.getCell(colm, row)
            if cell == player.id:
                adjecents = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
                for i in adjecents:
                    toColm, toRow = colm + i[0] , row + i[1]  # TODO
                    dest_cell = board.getCell(toColm, toRow)
                    if dest_cell is not None and dest_cell == 0:
                        yield ((colm, row), (toColm, toRow))

    def CalcScore(self, board, player):
        def dist(a):
            win, _ = np.where(a == player.id)
            win = np.abs(player.goal[1] - win)
            return np.sum(win)

        return 1.0 / board.run(dist)


class Heuristic:
    def __init__(self):
        pass

    def FindBestMove(self, game , board , Mplayer):
        Bestscore = 0
        Bestmove = ()
        AllMoves = game.allAvailableMoves(board, Mplayer)
        for move in AllMoves:
            game.do(move, board)
            score = game.CalcScore(board , Mplayer)
            game.undo(move, board)

            if score > Bestscore:
                Bestmove = move
                Bestscore = score

        return Bestmove

class Minimax:
    def __init__(self):
        pass

    def FindBestMove(self, game, board, Maxplayer, Minplayer , depth):
        def minimax(game, board, Maxplayer, Minplayer, depth, maximize):
            if depth == 0:
                return game.CalcScore(board, Maxplayer), (None, None)

            AllMoves = game.allAvailableMoves(board, Maxplayer if maximize else Minplayer)

            BestValue = float('-inf') if maximize else float('inf')
            count = 0  # TODO:
            for move in AllMoves:
                game.do(move, board)
                value, __ = minimax(game, board, Maxplayer, Minplayer, depth - 1, not maximize)
                game.undo(move, board)

                if maximize:
                    if value > BestValue:
                        BestValue= value
                        BestMove = move
                else:
                    if value < BestValue:
                        BestValue = value
                        BestMove = move

                count += 1

            if count == 0:
                return game.get_score(board, Maxplayer), (None, None)
            return BestValue, BestMove
        return minimax(game, board, Maxplayer, Minplayer, depth , True)[1]

class Alphabeta:
    def __init__(self):
        pass

    def get_optimal_move(self, game_logic, grid, max_player, min_player):
        def alphabeta(game_logic, grid, max_player, min_player, depth, alpha, beta, maximize):

            if depth == 0:
                return game_logic.get_score(grid, max_player), (None, None)

            gen = game_logic.generate_all_valid_moves(grid, max_player if maximize else min_player)

            best_value = float('-inf') if maximize else float('inf')

            count = 0  # TODO:
            for move in gen:
                count += 1

                game_logic.do(move, grid)
                v, __ = alphabeta(game_logic, grid, max_player, min_player, depth - 1, alpha, beta, not maximize)
                game_logic.undo(move, grid)

                if maximize:
                    if v > best_value:
                        best_value = v
                        best_move = move
                    alpha = max(alpha, v)
                else:
                    if v < best_value:
                        best_value = v
                        best_move = move
                    beta = min(beta, v)
                if beta <= alpha:
                    break

            if count == 0:
                return game_logic.get_score(grid, max_player), (None, None)

            return best_value, best_move

        return alphabeta(game_logic, grid, max_player, min_player, 4, float('-inf'), float('inf'), True)[1]


def generate_star(hg):
    def set_valid(q, r):
        hg.setCell(q, r, 0)

    for r in range(9):
        q_range = range(6 - r, 7) if r < 4 else range(hg.fColum(4), 11 - r + 4)
        for q in q_range:
            set_valid(q, r)
            set_valid(q + hg.fColum(16) + r, 16 - r)
            if r < 4:
                hg.setCell(q, r, 1)
                hg.setCell(q + hg.fColum(16) + r, 16 - r, 2)
    return hg


start = """\
            2             
           2 2             
          2 2 2           
         2 2 2 2           
o o o o o o o o o o o o o 
 o o o o o o o o o o o o   
  o o o o o o o o o o o   
   o o o o o o o o o o     
    o o o o o o o o o     
   o o o o o o o o o o     
  o o o o o o o o o o o   
 o o o o o o o o o o o o   
o o o o o o o o o o o o o 
         1 1 1 1           
          1 1 1           
           1 1             
            1            
"""


def load(hg, string):
    def set_cell(q, r, value):
        hg.set_cell(q, r, value)

    string = string.replace('o', '0')
    tokens = string.split()
    string2 = ''.join(reversed(string.splitlines()))
    tokens2 = string2.split()
    print(tokens2)
    assert len(tokens) == 121
    index = 0

    for r in range(9):
        q_range = range(6 - r, 7) if r < 4 else range(hg.first_column(4), 11 - r + 4)
        for q in q_range:
            set_cell(q, r, int(tokens[index]))
            set_cell(q + hg.first_column(16) + r, 16 - r, int(tokens2[index]))
            index += 1

    return hg


if __name__ == '__main__':
    hg = GameBoard.Shape(17, 13, -1)   #StarBoard
    print("Choose level of Difficulty\n 1- Easy \n 2-Medium \n 3- Hard")
    depth = int(input())
    Computer = Player(1, (6 + hg.fColum(16), 16))
    Human = Player(2 , (6, 0))

    Board = generate_star(hg)
    print(Board)

    game = Game()
    print("Which Ai Algorithm Do You want To test \n 1- MiniMax \n 2- AlphaBeta(Bouns) ")
    Choice = int(input())
    if(Choice == 1) :     Ai = Minimax()
    else : Ai = Minimax()

    for i in range(1000):
        bestMove = Ai.FindBestMove(game, Board, Computer, Human , depth )
        game.do(bestMove, Board)
        print(Board)
        AvalliableMoves = game.allAvailableMoves(Board, Human)
        myMoves = list(AvalliableMoves)
        if i >= 0:
            print("All Valid Moves : ")
            print(myMoves)
            length = len(myMoves)-1
            print("Choose Move: from 0 to " + str(length))
            i=0
            while(True) :
                i = int(input())
                if(i<=length):
                    break
                else: print("Invalid Move!")
            PlayerMove = myMoves[i]
            game.do(PlayerMove, Board)
            print(Board)

