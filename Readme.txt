Team members:
	Names			IDs             Emails
 
|1- Ahmed Badr Shaaban     | 20190019 |   ahmedbadrr417@gmail.com    |
|2- Mariam Mohamed Gharieb | 20190522 |	  mariamgharieb24@gmail.com  |
|3- Mohamed Amr Kamal 	   | 20190468 |   mohamed.kamal.ru@gmail.com |
|4- Adham Mohamed Gomaa    | 20190788 |   adhamgoma5050@gmail.com    |
|5- Mohamed Adel Abdallah  | 20190452 |   costamohamed105@gmail.com  |

---------------------------------------------------------------------|

Insturction:

we used a Python programming language.

the execuatble file is "ChinChecker.py".

In our code we must import numpy library and other libraries which are metioned in code and ready for running(there are in venv file and ready to use), 
we implement a miniMax algorithm and AlphaBeta Algorithm.

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