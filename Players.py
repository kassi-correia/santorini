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
		if color == 'white':
			self._pieces= ['A','B']
			self._non = ['Y', 'Z']
		else:
			self._pieces= ['Y','Z']
			self._non= ['A','B']

	def _update_pos(self, move, pos):
		pos+= self.locs[move]
		return pos
	
	def _pick_build(self, pos):
		moves = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
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
		return choice(moves)

	

class Random(Player):
	
	def choose_move(self, board, p1_pos, p1_moves, p2_moves):
		"""Returns list with worker, move, and build to be played"""
		# choice() randomly picks item from list
		if choice([False,True]):
			worker = self._pieces[0]
			move = choice(p1_moves)
		else:
			move = choice(p2_moves)
			worker = self._pieces[1]
		new_pos = self._update_pos(move, p1_pos[worker].copy())
		build = self._pick_build(new_pos)
		return [worker, move, build]





		
		

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
        
        dist13 = min(max(pos1[0] - pos3[0], pos3[0]-pos1[0]), max(pos1[1] - pos3[1], pos3[1]-pos1[1]))
        dist14 = min(max(pos1[0] - pos4[0], pos4[0]-pos1[0]), max(pos1[1] - pos4[1], pos4[1]-pos1[1]))
        dist24 = min(max(pos2[0] - pos4[0], pos4[0]-pos2[0]), max(pos2[1] - pos4[1], pos4[1]-pos2[1]))
        dist23 = min(max(pos2[0] - pos3[0], pos3[0]-pos2[0]), max(pos2[1] - pos3[1], pos3[1]-pos2[1]))
        
        return 8 - (min(dist13, dist23) + min(dist14, dist24))
    
    def _calc_score(self, board, pos1, pos2, pos3, pos4):
        return self._height_score(board, pos1, pos2) + self._center_score(pos1, pos2) + self._dist_score(pos1, pos2, pos3, pos4)
    
    def choose_move(self, board, pos, moves1, moves2):
        pos1 = pos[self._pieces[0]].copy()
        pos2 = pos[self._pieces[1]].copy()
        pos3 = pos[self._non[0]].copy()
        pos4 = pos[self._non[1]].copy()
        
        maxM = None
        maxP = None
        maxS = 0
        for e in moves1:
            for i in range(2):
                pos1[i] += self.locs[e][i]
            score = self._calc_score(board, pos1, pos2, pos3, pos4)
            if score > maxS:
                maxS = score
                maxM = e
                maxP = self._pieces[0]
            for i in range(2):
                pos1[i] -= self.locs[e][i]
        for e in moves2:
            for i in range(2):
                pos2[i] += self.locs[e][i]
            score = self._calc_score(board, pos1, pos2, pos3, pos4)
            if score > maxS:
                maxS = score
                maxM = e
                maxP = self._pieces[1]
            for i in range(2):
                pos2[i] -= self.locs[e][i]
        pos = self._update_pos(maxM, pos[maxP].copy())
        build = self._pick_build(pos)
        return [maxP, maxM, build]
        
        
        
        
