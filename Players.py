from random import choice

INFINITY = 300

class Player():
	def __init__(self, color):
		self.locs = dict()
		self.locs['n'] = [-1, 0]
		self.locs['ne'] = [-1, 1]
		self.locs['nw'] = [-1, -1]
		self.locs['w'] = [0, -1]
		self.locs['sw'] = [1, -1]
		self.locs['s'] = [1, 0]
		self.locs['se'] = [1, 1]
		self.locs['e'] = [0, 1]
		self._curr_piece = None
		if color == 'white':
			self._pieces= ['A','B']
			self._non = ['Y', 'Z']
		else:
			self._pieces= ['Y','Z']
			self._non= ['A','B']

	def _update_pos(self, move, pos):

		for i in range(2):
			pos[i] += self.locs[move][i]
		return pos
	
	def _pick_build(self, pos, board):
		moves = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
		players = ['A', 'B', 'Y', 'Z']
		print(self._curr_piece)
		players.remove(self._curr_piece)
		g = pos
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
		x = g[0]
		y = g[1]
		i = 0
		while i < len(moves):
			remo = False
			move = moves[i]
			new = [0, 0]
			new[0] = g[0] + self.locs[move][0]
			new[1] =  g[1] + self.locs[move][1]
			# if board[new[0]][new[1]][0] - board[g[0]][g[1]][0] > 1:
			# 	moves.remove(move)
			# 	remo = True
			if move == 'n':
				if board[x-1][y][1] in players or board[x-1][y][0] == 4:
					moves.remove('n')
					remo = True
			elif move == 'ne':
				if board[x-1][y+1][1] in players or board[x-1][y+1][0] == 4:
					moves.remove('ne')
					remo = True
			elif move == 'e':
				if board[x][y+1][1] in players or board[x][y+1][0] == 4:
					moves.remove('e')
					remo = True
			elif move == 'se':
				if board[x+1][y+1][1] in players or board[x+1][y+1][0] == 4:
					moves.remove('se')
					remo = True
			elif move == 's':
				if board[x+1][y][1] in players or board[x+1][y][0] == 4:
					moves.remove('s')
					remo = True
			elif move == 'sw':
				if board[x+1][y-1][1] in players or board[x+1][y-1][0] == 4:
					moves.remove('sw')
					remo = True
			elif move == 'w':
				if board[x][y-1][1] in players or board[x][y-1][0] == 4:
					moves.remove('w')
					remo = True
			elif move == 'nw':
				if board[x-1][y-1][1] in players or board[x-1][y-1][0] == 4:
					moves.remove('nw')
					remo = True
			if not remo:
				i+= 1
		return choice(moves)

	

class Random(Player):
	
	def choose_move(self, board, p1_pos, p1_moves, p2_moves):
		"""Returns list with worker, move, and build to be played"""
		if p1_moves == []:
			worker = self._pieces[1]
			move = choice(p2_moves)
		elif p2_moves == []:
			worker = self._pieces[0]
			move = choice(p1_moves)
		else:
			if choice([False,True]):
				worker = self._pieces[0]
				move = choice(p1_moves)
			else:
				move = choice(p2_moves)
				worker = self._pieces[1]
		self._curr_piece = worker
		new_pos = self._update_pos(move, p1_pos[worker].copy())
		build = self._pick_build(new_pos, board)
		return [[worker, move, build]]





		
		

class Heuristic(Player):
    
    
    def _height_score(self, board, pos1, pos2):
        
        if board[pos1[0]][pos1[1]][0]  == 3 or board[pos2[0]][pos2[1]][0] == 3:
            return INFINITY
        return board[pos1[0]][pos1[1]][0] + board[pos2[0]][pos2[1]][0]
    
    def _center_score(self, pos1, pos2):
        ret = 0
        if pos1 == [2,2]:
            ret = 2
        elif 0 in pos1 or 4 in pos1:
            ret += 0
        else:
            ret += 1
        if pos2 == [2,2]:
            ret += 2
        elif 0 in pos2 or 4 in pos2:
            ret += 0
        else:
            ret += 1
        return ret
    
    def _dist_score(self, pos1, pos2, pos3, pos4):
        
        dist13 = max(max(pos1[0] - pos3[0], pos3[0]-pos1[0]), max(pos1[1] - pos3[1], pos3[1]-pos1[1]))
        dist14 = max(max(pos1[0] - pos4[0], pos4[0]-pos1[0]), max(pos1[1] - pos4[1], pos4[1]-pos1[1]))
        dist24 = max(max(pos2[0] - pos4[0], pos4[0]-pos2[0]), max(pos2[1] - pos4[1], pos4[1]-pos2[1]))
        dist23 = max(max(pos2[0] - pos3[0], pos3[0]-pos2[0]), max(pos2[1] - pos3[1], pos3[1]-pos2[1]))
        
        return 8 - (min(dist13, dist23) + min(dist14, dist24))
    
    def _calc_score(self, board, pos1, pos2, pos3, pos4):
        return [self._height_score(board, pos1, pos2), self._center_score(pos1, pos2), self._dist_score(pos1, pos2, pos3, pos4)]
    
    def choose_move(self, board, pos, moves1, moves2):
        pos1 = pos[self._pieces[0]].copy()
        pos2 = pos[self._pieces[1]].copy()
        pos3 = pos[self._non[0]].copy()
        pos4 = pos[self._non[1]].copy()
        
        maxM = None
        maxP = None
        maxS = 0
        maxLs = None
        for e in moves1:
            for i in range(2):
                pos1[i] += self.locs[e][i]
            ls = self._calc_score(board, pos1, pos2, pos3, pos4)
            score = sum(ls)
            if score > maxS:
                maxLs = ls
                maxS = score
                maxM = e
                maxP = self._pieces[0]
            for i in range(2):
                pos1[i] -= self.locs[e][i]
        for e in moves2:
            for i in range(2):
                pos2[i] += self.locs[e][i]
            ls = self._calc_score(board, pos1, pos2, pos3, pos4)
            score = sum(ls)
            if score > maxS:
                maxLs = ls
                maxS = score
                maxM = e
                maxP = self._pieces[1]
            for i in range(2):
                pos2[i] -= self.locs[e][i]
        pos = self._update_pos(maxM, pos[maxP].copy())
        self._curr_piece = maxP
        build = self._pick_build(pos, board)
        return [[maxP, maxM, build], maxLs]
        
        
        
        
