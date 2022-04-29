import sys
from Exception import InvalidMove, InvalidBuild, InvalidWorker
from Game import Game


class SantoriniCLI():

    def __init__(self, white='human', blue='human', undo='off', score='off'):
        self._white = white
        self._blue = blue
        self._undo = off
        self._score = off
        self._turn_num = 0

        #need to pass in h or a not whole word
        if self._white == 'human':
            self.white_type = 'h'
        else:
            self.white_type = 'a'

        if self._blue == 'human':
            self.blue_type = 'h'
        else:
            self.blue_type = 'a'

        self._game = Game(self.white_type, self.blue_type)



    def _display_board(self):
        """Prints current board standing."""
        board = Game.git_board()
        printf("""
+--+--+--+--+--+
|{board[0][0][0]}{board[0][0][1]}|{board[0][1][0]}{board[0][1][1]}|{board[0][2][0]}{board[0][2][1]}|{board[0][3][0]}{board[0][3][1]}|{board[0][4][0]}{board[0][4][1]}|
+--+--+--+--+--+
|{board[1][0][0]}{board[1][0][1]}|{board[1][1][0]}{board[1][1][1]}|{board[1][2][0]}{board[1][2][1]}|{board[1][3][0]}{board[1][3][1]}|{board[1][4][0]}{board[1][4][1]}|
+--+--+--+--+--+
|{board[2][0][0]}{board[2][0][1]}|{board[2][1][0]}{board[2][1][1]}|{board[2][2][0]}{board[2][2][1]}|{board[2][3][0]}{board[2][3][1]}|{board[2][4][0]}{board[2][4][1]}|
+--+--+--+--+--+
|{board[3][0][0]}{board[3][0][1]}|{board[3][1][0]}{board[3][1][1]}|{board[3][2][0]}{board[3][2][1]}|{board[3][3][0]}{board[3][3][1]}|{board[3][4][0]}{board[3][4][1]}|
+--+--+--+--+--+
|{board[4][0][0]}{board[4][0][1]}|{board[4][1][0]}{board[4][1][1]}|{board[4][2][0]}{board[4][2][1]}|{board[4][3][0]}{board[4][3][1]}|{board[4][4][0]}{board[4][4][1]}|
+--+--+--+--+--+
        """)
        pass


        def _display_turn(self):
            printf("Turn {self._turn_num} {Game.git_curr_player})
    
    def run(self):      
        """Initialize game"""
        #while not win
        while True:
            self._display_board()
            self._display_turn()
                #make move takes worker, direction
            worker = None
            move = None
            build = None
            if (self._game.git_type_player) == 'h':
                while not worker:
                    try:
                        print("Select a worker to move")
                        worker = input("")
                        self._game.make_move(worker, move, build)
                    except InvalidWorker: 
                        worker = None
                        print("Not a valid worker")
                    except WrongWorker:
                        worker = None
                        print("That is not your worker")

                while not move:
                    try:
                        print("Select a direction to move (n, ne, e, se, s, sw, w, nw)")
                        move = input("")
                        self._game.make_move(worker, move, build)
                    except InvalidMove:
                        move = None
                        print("Not a valid direction")
                    except WrongMove:
                        move = None
                        print("Cannot move {move}")
                
                while not build:
                    try:
                        print("Select a direction to build (n, ne, e, se, s, sw, w, nw)")
                        build = input("")
                        self._game.make_move(worker, move, build)
                    except InvalidMove:
                        build = none
                        print("Not a valid build")
                    except WrongBuild:
                        build = none
                        print("Cannot build {build}")

            else:
                # pass in move for AI
                # feeding move into game
                
            self._turn_num = self._turn_num + 1
            self._display_move

#AI player: select move--pass in position
