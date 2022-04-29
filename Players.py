from random import choice

class Player():
	def __init__(self, color):
		if color == 'white':
			self._pieces= ['A','B']
		else:
			self._pieces= ['Y','Z']

	

class Random(Player):
	def __init__(self, color):
		if color == 'white':
			self._pieces= ['A','B']
		else:
			self._pieces= ['Y','Z']
	
	def choose_move(self, board, p1_pos, p1_moves, p2_pos, p2_moves):
		"""Returns list with worker, move, and build to be played"""
		# choice() randomly picks item from list
		worker = choice(self._pieces)
		if worker == 'A' or 'Y':
			move = choice(p1_moves)
			new_pos = self._update_pos(move, p1_pos)
		else:
			move = choice(p2_moves)
			new_pos = self._update_pos(move, p2_pos)
		valid_builds = self._get_valid_builds(new_pos)
		build = choice(valid_builds)
		result = []
		result.append(worker)
		result.append(move)
		result.append(build)
		return result



	def _update_pos(self, move, pos):
		if move == 'n':
			pos[0] -= 1
		elif move == 'ne':
			pos[0] -=1
			pos[1] += 1
		elif move == 'e':
			pos[1] += 1
		elif move == 'se':
			pos[0] +=1
			pos[1] += 1
		elif move == 's':
			pos[0] +=1
		elif move == 'sw':
			pos[0] += 1
			pos[1] -=1
		elif move == 'w':
			pos[1] -= 1
		elif move == 'nw':
			pos[0] -=1
			pos[1] -= 1
		return pos

	def _get_valid_builds(self, pos):
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
		return moves




		
		

class Heuristic(Player):
	def __init__(self):
		pass

	def choose_move(self, board):
		pass
