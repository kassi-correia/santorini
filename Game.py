
from proj5.Exception import InvalidBuild, InvalidMove, InvalidRedo, InvalidUndo, InvalidWorker, WrongBuild, WrongMove, WrongWorker


class Game():
    #robby sucks
    def __init__(self, p1, p2):
        self._position = Position()
        self._hist = []
        self._fut= []
        self.p1 = p1
        self.p2 = p2
        self.workers = ['A', 'B', 'Y', 'Z']
    
    def get_board(self):
        return self._position.board
    
    def make_move(self, worker, move = None, build = None):
        
        if worker not in self.workers:
            raise InvalidWorker()
        if move == None:
            return
        turn = self._position.turn
        if worker not in self._position.pieces[turn]:
            raise WrongWorker()
        if move not in self._position.dirs:
            raise InvalidMove()
        if build == None:
            return
        if build not in self._position.dirs:
            raise InvalidBuild()
        
        if worker == 'Y':
            b = self._position.y
        elif worker == 'Z':
            b = self._position.z
        elif worker == 'A':
            b = self._position.a 
        elif worker == 'B':
            b = self._position.b
        dfd = b
        if move == 'n':
            b[0] += 1
        elif move == 'ne':
            b[0] +=1
            b[1] += 1
        elif move == 'e':
            b[1] += 1
        elif move == 'se':
            b[0] -=1
            b[1] += 1
        elif move == 's':
            b[0] -=1
        elif move == 'sw':
            b[0] -= 1
            b[1] -=1
        elif move == 'w':
            b[1] -= 1
        elif move == 'nw':
            b[0] +=1
            b[1] -= 1
        if b[0] < 0 or b[0] > 4 or b[1] > 4 or b[1] < 0:
            raise WrongMove()
        
        new = Position(self._position)
        new.update_pos(worker, dfd[0], dfd[1], b)
        if move == 'n':
            b[0] += 1
        elif move == 'ne':
            b[0] +=1
            b[1] += 1
        elif move == 'e':
            b[1] += 1
        elif move == 'se':
            b[0] -=1
            b[1] += 1
        elif move == 's':
            b[0] -=1
        elif move == 'sw':
            b[0] -= 1
            b[1] -=1
        elif move == 'w':
            b[1] -= 1
        elif move == 'nw':
            b[0] +=1
            b[1] -= 1
        if b[0] < 0 or b[0] > 4 or b[1] > 4 or b[1] < 0:
            raise WrongBuild()
        
        new.build(b[0], b[1])
        if new.turn == 'b':
            new.turn = 'w'
        else:
            new.turn = 'b'
        
        self._hist.append(self._position)
        self._position = new
        
    def get_curr_player(self):
        
        if self._position.turn == 'w':
            return 'white (AB)'
        return 'blue (YZ)'
    
    def get_type_player(self):
        if self._position.turn == 'w':
            return self.p1 
        return self.p2
    
    
        
        

class Position():
    
    def __init__(self, arg=None):
        
        if arg != None:
            self.board = arg.board
            self.turn = arg.turn
            self.pieces = arg.pieces
            self.dirs = arg.dirs
            self.y = arg.y
            self.b = arg.b
            self.z = arg.z
            self.a = arg.a
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
			self.y = [1,1]
			self.b = [1,3]
			self.a = [3, 1]
			self.z = [3,3]
	def update_pos(self, worker, x, y, b):   
		if worker == 'Y':
            new.board[x][y][1] = ' '
            new.board[b[0]][b[1]][1] = 'Y'
            new.y = b
            
        elif worker == 'Z':
            x = dfd[0]
            y = dfd[1]
            new.board[x][y][1] = ' '
            new.board[b[0]][b[1]][1] = 'Z'
            new.z = b
        elif worker == 'A':
            x = dfd[0]
            y = dfd[1]
            new.board[x][y][1] = ' '
            new.board[b[0]][b[1]][1] = 'a'
            new.a = b
        elif worker == 'B':
            x = dfd[0]
            y = dfd[1]
            new.board[x][y][1] = ' '
            new.board[b[0]][b[1]][1] = 'B'
            new.b = b

    def build(self, x, y):
        self.board[x][y][0] += 1
