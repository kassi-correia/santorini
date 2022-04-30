
from Exception import InvalidBuild, InvalidMove, InvalidRedo, InvalidUndo, InvalidWorker, WrongBuild, WrongMove, WrongWorker
import copy
from Players import Player, Random, Heuristic

class Game():
    #robby sucks
    def __init__(self, p1, p2):
        self._position = Position()
        self._hist = []
        self._fut= []
        self.p1 = p1
        self.p2 = p2
        self.workers = ['A', 'B', 'Y', 'Z']
        
        self.locs = dict()
        self.locs['n'] = [-1, 0]
        self.locs['ne'] = [-1, 1]
        self.locs['nw'] = [-1, -1]
        self.locs['w'] = [0, -1]
        self.locs['sw'] = [1, -1]
        self.locs['s'] = [1, 0]
        self.locs['se'] = [1, 1]
        self.locs['e'] = [0, 1]
        

        if p1 == 'r':
            self.white_player = Random('white')
        elif p1 == 'f':
            self.white_player = Heuristic('white')
        
        if p2 == 'r':
            self.blue_player = Random('blue')
        elif p2 == 'f':
            self.blue_player = Heuristic('blue')

    
    def git_board(self):
        return self._position.board

    def _check_if_winner(self):
        return self._position._check_if_winner()

    
    def make_move(self, worker, move = None, build = None):
        if worker not in self.workers:
            raise InvalidWorker()
        turn = self._position.turn
        if worker not in self._position.pieces[turn]:
            raise WrongWorker()
        if move == None:
            return
        if move not in self._position.dirs:
            raise InvalidMove()
        g = self._position.pos[worker]
        if (g[0] == 0 and (move == 'n' or move == 'nw' or move == 'ne')):
            raise WrongMove()
        if (g[0] == 4 and (move == 's' or move == 'sw' or move == 'se')):
            raise WrongMove()
        if (g[1] == 0 and (move == 'w' or move == 'nw' or move == 'sw')):
            raise WrongMove()
        if (g[1] == 4 and (move == 'e' or move == 'ne' or move == 'se')):
            raise WrongMove()
        
        
        if build == None:
            return
        if build not in self._position.dirs:
            raise InvalidBuild()
        c = self._position.pos[worker]
        b = []
        dfd = c.copy()
        
        for i in range(2):
            b.append(c[i] + self.locs[move][i])
        
        bh = b.copy()
        if b[0] < 0 or b[0] > 4 or b[1] > 4 or b[1] < 0:
            raise WrongMove()
        
        for i in range(2):
            b[i] += self.locs[build][i]
        
        
        if b[0] < 0 or b[0] > 4 or b[1] > 4 or b[1] < 0:
            raise WrongBuild()
        
        new = Position(self._position)
        new.update_pos(worker, dfd[0], dfd[1], bh)
        new.build(b[0], b[1])
        if new.turn == 'b':
            new.turn = 'w'
        else:
            new.turn = 'b'
        
        self._hist.append(self._position)
        self._position = new
        
    def git_curr_player(self):
        if self._position.turn == 'w':
            return 'white (AB)'
        return 'blue (YZ)'
    
    def git_type_player(self):
        if self._position.turn == 'w':
            return self.p1 
        return self.p2

    def git_player_obj(self):
        if self.git_curr_player() == 'white (AB)':
            return self.white_player
        else:
             return self.blue_player

    def ai_move(self):
        p = self.git_player_obj()
        board = self.git_board()
        # pass in position and possible moves for each worker
        if self._position.turn == 'w':
            p1_pos = self._position.pos['A']
            p1_moves = self.git_moves('A')
            p2_pos = self._position.pos['B']
            p2_moves = self.git_moves('B')
        else:
            p1_pos = self._position.pos['Y']
            p1_moves = self.git_moves('Y')
            p2_pos = self._position.pos['Z']
            p2_moves = self.git_moves('Z')

        result = p.choose_move(board, p1_pos, p1_moves, p2_pos, p2_moves)
        self.make_move(result[0], result[1], result[2])


    def git_moves(self, worker):
        moves = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        g = self._position.pos[worker]
        if g[0] == 0:
            moves.remove('n')
            moves.remove('nw')
            moves.remove('ne')
        if g[0] == 4:
            moves.remove('se')
            moves.remove('s')
            moves.remove('sw')
        if g[1] == 4:
            moves.remove('e')
            if 'ne' in moves:
                moves.remove('ne')
            if 'se' in moves:
                moves.remove('se')
        if g[1] == 0:
            moves.remove('w')
            if 'ne' in moves:
                moves.remove('nw')
            if 'se' in moves:
                moves.remove('sw')

    def git_build(self, worker):
        moves = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        g = self._position.pos[worker]
        if g[0] == 0:
            moves.remove('n')
            moves.remove('nw')
            moves.remove('ne')
        if g[0] == 4:
            moves.remove('se')
            moves.remove('s')
            moves.remove('sw')
        if g[1] == 4:
            moves.remove('e')
            if 'ne' in moves:
                moves.remove('ne')
            if 'se' in moves:
                moves.remove('se')
        if g[1] == 0:
            moves.remove('w')
            if 'ne' in moves:
                moves.remove('nw')
            if 'se' in moves:
                moves.remove('sw')

        return moves
            
        
            
    
    
        
        

class Position():
    
    def __init__(self, arg=None):
        if arg != None:
            self.board = copy.deepcopy(arg.board)
            self.turn = arg.turn[:]
            self.pieces = arg.pieces.copy()
            self.dirs = arg.dirs.copy()
            self.pos = arg.pos.copy()
        else:
            self.board = [[[0, ' '],[0, ' '],[0, ' '],[0, ' '],[0, ' ']],
						[[0, ' '],[0, 'Y'],[0, ' '],[0, 'B'],[0, ' ']],
						[[0, ' '],[0, ' '],[0, ' '],[0, ' '],[0, ' ']],
						[[0, ' '],[0, 'A'],[0, ' '],[0, 'Z'],[0, ' ']],
						[[0, ' '],[0, ' '],[0, ' '],[0, ' '],[0, ' ']]]
            self.turn = 'w'
            self.pieces = dict()
            self.pieces['w'] = ['A', 'B']
            self.pieces['b'] = ['Y', 'Z']
            self.dirs = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
            
            self.pos = dict()
            self.pos['Y'] = [1,1]
            self.pos['B'] = [1,3]
            self.pos['A'] = [3, 1]
            self.pos['Z'] = [3,3]

    def update_pos(self, worker, x, y, b):
        if worker == 'Z':
            self.board[x][y][1] = ' '
            self.board[b[0]][b[1]][1] = 'Z'
            self.pos['Z'] = b.copy()
        elif worker == 'Y':
            self.board[x][y][1] = ' '
            self.board[b[0]][b[1]][1] = 'Y'
            self.pos['Y'] = b.copy()
        elif worker == 'A':
            self.board[x][y][1] = ' '
            self.board[b[0]][b[1]][1] = 'A'
            self.pos['A'] = b.copy()
        elif worker == 'B':
            self.board[x][y][1] = ' '
            self.board[b[0]][b[1]][1] = 'B'
            self.pos['B'] = b.copy()

    def build(self, x, y):
        self.board[x][y][0] += 1

    def _check_if_winner(self):
        for row in self.board:
            for pos in row:
                if pos[0] == 3 and pos[1] != ' ':
                    if pos[1] == 'Y'or 'Z':
                        return 'blue'
                    else:
                        return 'white'
        return False





            
