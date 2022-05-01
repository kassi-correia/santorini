
from Exception import InvalidBuild, InvalidMove, InvalidRedo, InvalidUndo, InvalidWorker, WrongBuild, WrongMove, WrongWorker
import copy
from Players import Player, Random, Heuristic

class Game():
    #robby sucks
    def __init__(self, p1, p2):
        
        #Change debug to FALSE before submitting, it will print out info when an exception is raised
        self.debug = True
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


    def _wrong_move(self, worker, move, board, pos):
        x = pos[0]
        y = pos[1]
        players = ['A', 'B', 'Y', 'Z']
        players.remove(worker)
        new = [0,0]
        for i in range(2):
            new[i] = pos[i] + self.locs[move][i]
        if board[new[0]][new[1]][0] - board[pos[0]][pos[1]][0] > 1:
            return True
        elif move == 'n':
            if board[x-1][y][1] in players or board[x-1][y][0] == 4:
                return True
        elif move == 'ne':
            if board[x-1][y+1][1] in players or board[x-1][y+1][0] == 4:
                return True
        elif move == 'e':
            if board[x][y+1][1] in players or board[x][y+1][0] == 4:
                return True
        elif move == 'se':
            if board[x+1][y+1][1] in players or board[x+1][y+1][0] == 4:
                return True
        elif move == 's':
            if board[x+1][y][1] in players or board[x+1][y][0] == 4:
                return True
        elif move == 'sw':
            if board[x+1][y-1][1] in players or board[x+1][y-1][0] == 4:
                return True
        elif move == 'w':
            if board[x][y-1][1] in players or board[x][y-1][0] == 4:
                return True
        elif move == 'nw':
            if board[x-1][y-1][1] in players or board[x-1][y-1][0] == 4:
                return True
        else:
            return False




    
    def make_move(self, worker, move = None, build = None):
        if worker not in self.workers:
            raise InvalidWorker()
        turn = self._position.turn
        if worker not in self._position.pieces[turn]:
            raise WrongWorker()
        if move == None:
            return
        if move not in self._position.dirs:
            self.log("bad move:", move, worker)
            raise InvalidMove()
        g = self._position.pos[worker]
        if (g[0] == 0 and (move == 'n' or move == 'nw' or move == 'ne')):
            self.log("bad move:", move, worker)
            raise WrongMove()
        if (g[0] == 4 and (move == 's' or move == 'sw' or move == 'se')):
            self.log("bad move:", move, worker)
            raise WrongMove()
        if (g[1] == 0 and (move == 'w' or move == 'nw' or move == 'sw')):
            self.log("bad move:", move, worker)
            raise WrongMove()
        if (g[1] == 4 and (move == 'e' or move == 'ne' or move == 'se')):
            self.log("bad move:", move, worker)
            raise WrongMove()
        #K: check if another player is there or if level 4
        board = self.git_board()
        if self._wrong_move(worker, move, board, g):
            self.log("bad move:", move, worker)
            raise WrongMove()
        
        
        if build == None:
            return
        if build not in self._position.dirs:
            self.log("bad build:", move, worker, build)
            raise InvalidBuild()


        # check if another player is there or if level 4 before build?
        temp = g.copy()
        n = self._new_pos(move, temp)

        if self._wrong_build(n, board, build, worker):
            self.log("bad build:", move, worker, build)
            raise WrongBuild()







        c = self._position.pos[worker]
        b = []
        dfd = c.copy()
        
        for i in range(2):
            b.append(c[i] + self.locs[move][i])
        
        bh = b.copy()
        if b[0] < 0 or b[0] > 4 or b[1] > 4 or b[1] < 0:
            self.log("bad move:", move, worker)
            raise WrongMove()
        
        for i in range(2):
            b[i] += self.locs[build][i]
        
        
        if b[0] < 0 or b[0] > 4 or b[1] > 4 or b[1] < 0:
            self.log("bad build:", move, worker, build)
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
        

    def _wrong_build(self, pos, board, build, worker):
        x = pos[0]
        y = pos[1]
        players = ['A', 'B', 'Y', 'Z']
        players.remove(worker)
        move = build
        if move == 'n':
            if board[x-1][y][1] in players or board[x-1][y][0] == 4:
                return True
        elif move == 'ne':
            if board[x-1][y+1][1] in players or board[x-1][y+1][0] == 4:
                return True
        elif move == 'e':
            if board[x][y+1][1] in players or board[x][y+1][0] == 4:
                return True
        elif move == 'se':
            if board[x+1][y+1][1] in players or board[x+1][y+1][0] == 4:
                return True
        elif move == 's':
            if board[x+1][y][1] in players or board[x+1][y][0] == 4:
                return True
        elif move == 'sw':
            if board[x+1][y-1][1] in players or board[x+1][y-1][0] == 4:
                return True
        elif move == 'w':
            if board[x][y-1][1] in players or board[x][y-1][0] == 4:
                return True
        elif move == 'nw':
            if board[x-1][y-1][1] in players or board[x-1][y-1][0] == 4:
                return True
        else:
            return False



    def _new_pos(self, move, pos):
        """Returns new pos after move (doesn't actually change board)"""
        p = pos.copy()
        for i in range(2):
            p[i] += self.locs[move][i]
        return p

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
            p1_moves = self.git_moves('A', board)
            p2_moves = self.git_moves('B', board)
        else:
            p1_moves = self.git_moves('Y', board)
            p2_moves = self.git_moves('Z', board)
        result = p.choose_move(board, self._position.pos, p1_moves, p2_moves)
        self.make_move(result[0], result[1], result[2])
        return result


    def git_moves(self, worker, board):
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
        # K: remove spot if it is occupied or if its level 4
        x = g[0]
        y = g[1]
        for move in moves:
            new = [0, 0]
            new[0] = g[0] + self.locs[move][0]
            new[1] =  g[1] + self.locs[move][1]
            if board[new[0]][new[1]][0] - board[g[0]][g[1]][0] > 1:
                moves.remove(move)
            elif move == 'n':
                if board[x-1][y][1] != ' ' or board[x-1][y][0] == 4:
                    moves.remove('n')
            elif move == 'ne':
                if board[x-1][y+1][1] != ' ' or board[x-1][y+1][0] == 4:
                    moves.remove('ne')
            elif move == 'e':
                if board[x][y+1][1] != ' ' or board[x][y+1][0] == 4:
                    moves.remove('e')
            elif move == 'se':
                if board[x+1][y+1][1] != ' ' or board[x+1][y+1][0] == 4:
                    moves.remove('se')
            elif move == 's':
                if board[x+1][y][1] != ' ' or board[x+1][y][0] == 4:
                    moves.remove('s')
            elif move == 'sw':
                if board[x+1][y-1][1] != ' ' or board[x+1][y-1][0] == 4:
                    moves.remove('sw')
            elif move == 'w':
                if board[x][y-1][1] != ' ' or board[x][y-1][0] == 4:
                    moves.remove('w')
            elif move == 'nw':
                if board[x-1][y-1][1] != ' ' or board[x-1][y-1][0] == 4:
                    moves.remove('nw')
        return moves

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
    
    def git_worker_pos(self, worker):
        
        if worker not in self._position.pos:
            raise InvalidWorker()
        return self._position.pos[worker]

    def log(self, message, *args):
        if self.debug:
            print(message)
            print(args)
     
     
            
        
            
    
    
        
        

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





            
