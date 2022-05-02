import sys
from Exception import InvalidMove, InvalidBuild, InvalidWorker, WrongMove, WrongBuild, WrongWorker
from Game import Game

class SantoriniCLI():

    def __init__(self, white='human', blue='human', undo='off', score='off'):
        self._white = white
        self._blue = blue
        self._undo = undo
        self._score = score
        self._turn_num = 1

        if self._white == 'human':
            self.white_type = 'h'
        elif self._white == 'random':
            self.white_type = 'r'
        else:
             self.white_type = 'f'

        if self._blue == 'human':
            self.blue_type = 'h'
        elif self._blue == 'random':
            self.blue_type = 'r'
        else:
             self.blue_type = 'f'

        self._game = Game(self.white_type, self.blue_type)



    def _display_board(self):
        """Prints current board standing."""
        board = self._game.git_board()
        print(f"""+--+--+--+--+--+
|{board[0][0][0]}{board[0][0][1]}|{board[0][1][0]}{board[0][1][1]}|{board[0][2][0]}{board[0][2][1]}|{board[0][3][0]}{board[0][3][1]}|{board[0][4][0]}{board[0][4][1]}|
+--+--+--+--+--+
|{board[1][0][0]}{board[1][0][1]}|{board[1][1][0]}{board[1][1][1]}|{board[1][2][0]}{board[1][2][1]}|{board[1][3][0]}{board[1][3][1]}|{board[1][4][0]}{board[1][4][1]}|
+--+--+--+--+--+
|{board[2][0][0]}{board[2][0][1]}|{board[2][1][0]}{board[2][1][1]}|{board[2][2][0]}{board[2][2][1]}|{board[2][3][0]}{board[2][3][1]}|{board[2][4][0]}{board[2][4][1]}|
+--+--+--+--+--+
|{board[3][0][0]}{board[3][0][1]}|{board[3][1][0]}{board[3][1][1]}|{board[3][2][0]}{board[3][2][1]}|{board[3][3][0]}{board[3][3][1]}|{board[3][4][0]}{board[3][4][1]}|
+--+--+--+--+--+
|{board[4][0][0]}{board[4][0][1]}|{board[4][1][0]}{board[4][1][1]}|{board[4][2][0]}{board[4][2][1]}|{board[4][3][0]}{board[4][3][1]}|{board[4][4][0]}{board[4][4][1]}|
+--+--+--+--+--+""")
        pass


    def _display_turn(self):
        z = self._game.git_curr_player()
        
        # print score
        if self._score == 'on':
            s = self._game.git_score()
            print(f"Turn: {self._turn_num}, {z}, ({s[0]}, {s[1]}, {s[2]})")
        else:
            print(f"Turn: {self._turn_num}, {z}")


    def _check_if_winner(self):
        """Returns false if no winner, or returns 'blue' or 'white' if one
        has won."""
        return self._game._check_if_winner()
    
    def run(self):      
        """Initialize game"""
        while not self._check_if_winner():
            self._display_board()
            self._display_turn()
            if self._undo == 'on':
                next = None
                while not next:
                    print("undo, redo, or next")
                    reply = input("")
                    if reply == 'next':
                        #break
                        next = 'next'
                    elif reply == 'undo':
                        u = self._game.undo()
                        self._turn_num -= u
                        self._display_board()
                        self._display_turn()
                    elif reply == 'redo':
                        u = self._game.redo()
                        self._turn_num += u
                        self._display_board()
                        self._display_turn()

            worker = None
            move = None
            build = None
            
            if self._game.git_type_player() == 'h':
                while not worker:
                    try:
                        #add method to check if either worker can move
                        print("Select a worker to move")
                        worker = input("")
                        self._game.make_move(worker)
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
                        self._game.make_move(worker, move)
                    except InvalidMove:
                        move = None
                        print("Not a valid direction")
                    except WrongMove:
                        print(f"Cannot move {move}")
                        move = None
                
                while not build:
                    try:
                        print("Select a direction to build (n, ne, e, se, s, sw, w, nw)")
                        build = input("")
                        self._game.make_move(worker, move, build)
                    except WrongMove:
                        print(f"Cannot move {move}")
                        move = None
                    except InvalidBuild:
                        build = None
                        print("Not a valid build")
                    except WrongBuild:
                        print(f"Cannot build {build}")
                        build = None
            else:
                result = self._game.ai_move()
                if result != ['L', 'L', 'L']:
                    print(f"{result[0][0]},{result[0][1]},{result[0][2]}")

            self._turn_num += 1
        self._display_board()
        self._display_turn()
        print(f"""{self._check_if_winner()} has won""")
        sys.exit()



