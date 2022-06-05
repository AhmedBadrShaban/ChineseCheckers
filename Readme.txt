   
|Ahmed Badr Shaaban      ahmedbadrr417@gmail.com    |
  
 
Insturction:

I used a Python programming language.

the execuatble file is "ChinChecker.py".

In the code you must import numpy library and other libraries which are metioned in code and ready for running.
 implementiatio of  miniMax algorithm and AlphaBeta Algorithm.

Hurestic Description :

The Heuristic function is implemented to determine which move is the best move by testing all the avialable moves and calculate the player score if this move choosen  and return the move with best score value.

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
