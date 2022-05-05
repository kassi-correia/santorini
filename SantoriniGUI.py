import tkinter as tk
import sys
from Exception import InvalidMove, InvalidBuild, InvalidWorker, WrongMove, WrongBuild, WrongWorker
from Game import Game
from Players import Player, PlayerContext
from random import choice

class SantoriniGUI():
	def __init__(self, white='human', blue='human', undo='off', score='off'):
		self._white = white
		self._blue = blue
		self._setter = 0
		self.__undo = undo
		self._context = PlayerContext()
		self._score = score
		self._mover = []
		self._turn_num = 1
		self.dirs = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
		self._window = tk.Tk()
		self._window.title("Santorini")
		self.locs = dict()
		self.locs['n'] = [-1, 0]
		self.locs['ne'] = [-1, 1]
		self.locs['nw'] = [-1, -1]
		self.locs['w'] = [0, -1]
		self.locs['sw'] = [1, -1]
		self.locs['s'] = [1, 0]
		self.locs['se'] = [1, 1]
		self.locs['e'] = [0, 1]
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
		self._game = Game(self.white_type, self.blue_type, self._score)

		self._buttons = []
		self._board = tk.Frame(self._window)
		for row in range(5):
			for col in range(5):
				if col == 1 and row == 1:
					button=tk.Button(self._board, text='0Y', command= lambda row=row, col=col: self._press(row, col))
				elif col == 1 and row == 3: 
					button=tk.Button(self._board, text='0B', command= lambda row=row, col=col: self._press(row, col))
				elif col == 3 and row == 1:
					button=tk.Button(self._board, text='0A', command= lambda row=row, col=col: self._press(row, col))
				elif col == 3 and row == 3:
					button=tk.Button(self._board, text='0Z',command= lambda row=row, col=col: self._press(row, col))
				else:
					button=tk.Button(self._board, text='0 ', command= lambda row=row, col=col: self._press(row, col))
				button.grid(row=row, column=col)
				self._buttons.append(button)

		self._board.grid(row=0, column=1)
		self._instruction = tk.Frame(self._window)
		self._instruction.grid(row=7, column = 0)
		self._undo = tk.Frame(self._window)
		if white != 'human' or blue != 'human':
			self._aim = tk.Button(self._undo, text = 'AI move', command = self._ai_move)
			self._aim.grid(row=0, column=1)

		if self.__undo == 'on':
			self.undo=tk.Button(self._undo, text="Undo")
			self.undo.grid(row=1, column=0)
			self.redo=tk.Button(self._undo, text="Redo")
			self.redo.grid(row=1, column=1)
			self.next=tk.Button(self._undo, text="Next")
			self.next.grid(row=1, column=2)

		self._undo.grid(row=5, column =1)
		self._run()
		self._window.mainloop()

	def _press(self, row, col):
		if self._setter == 0 and ((self._turn_num %2 == 1 and self._white == 'human') or (self._turn_num % 2 == 0 and self._blue == 'human')):
			board = self._game.git_board()
			l = board[col][row][1]
			if l != ' ':
				if l not in self._game._position.pieces[self._game._position.turn]:
					return
				g = self._game.git_moves(l, board)
				for e in g:
					row += self.locs[e][1]
					col += self.locs[e][0]
					posd = (row *5) + col
					self._buttons[posd].configure(highlightbackground= 'green')
					row-=self.locs[e][1]
					col -= self.locs[e][0]
				self._mover.append(l)
				self.labe['text'] = 'Select a direction to move.'
				self._setter = 1
		elif self._setter == 1:
			self.labe['text'] = 'Select a direction to build.'
			board = self._game.git_board()
			l = board[col][row][1]
			g = self._game.git_worker_pos(self._mover[0])
			b = g.copy()
			b[0] = col - b[0]
			b[1] = row - b[1]
			dir = None
			for e in self.locs:
				if self.locs[e] == b:
					dir = e
			if dir == None:
				return
			posd = (row *5) + col
			if self._buttons[posd]['highlightbackground'] == 'green':
				self._mover.append(dir)
				self._setter = 2
				for e in self._buttons:
					e['highlightbackground'] = 'white'
				p = self._game.git_curr_player()[0]

				g = Player(p)
				z = g._pick_build([col, row], board, self._mover[0], True)
				for e in z:
					row += self.locs[e][1]
					col += self.locs[e][0]
					posd = (row *5) + col
					self._buttons[posd].configure(highlightbackground= 'green')
					row-=self.locs[e][1]
					col -= self.locs[e][0]
		elif self._setter == 2:
			board = self._game.git_board()
			l = board[col][row][1]
			g = self._game.git_worker_pos(self._mover[0])
			b = g.copy()
			for i in range(2):
				b[i] += self.locs[self._mover[1]][i]
			b[0] = col - b[0]
			b[1] = row - b[1]
			dir = None
			for e in self.locs:
				if self.locs[e] == b:
					dir = e
			if dir == None:
				return
			posd = (row *5) + col
			if self._buttons[posd]['highlightbackground'] == 'green':
				self._mover.append(dir)
				self._setter = 0
				for e in self._buttons:
					e['highlightbackground'] = 'white'
				self._game.make_move(self._mover[0], self._mover[1], dir)
				self._mover = []
				board = self._game.git_board()
				for i in range(25):
					e = self._buttons[i]
					cold = (i % 5)
					rowd = i // 5
					strb = str(board[cold][rowd][0])
					strb += board[cold][rowd][1]
					e.configure(text = strb[:])
				if self._game._check_if_winner():
					self.labe['text'] = self._game._check_if_winner() + " wins!"
					for e in self._buttons:
						e.destroy()
					if self.__undo == 'on':
						self.undo.destroy()
						self.redo.destroy()
						self.next.destroy()
					return
			self._turn_num += 1
			if self._game.git_type_player() != 'h':
				self.labe['text'] = 'Make AI move.'
			else:
				self.labe['text'] = 'Select a worker.'
			self._display_turn()
			self._highlight_workers()
			

	def _ai_move(self):
		if (self._turn_num %2 == 1 and self._white == 'human') or (self._turn_num % 2 == 0 and self._blue == 'human') or self._setter != 0:
			return 
		board = self._game.git_board()
		if self._white != 'human' and self._turn_num % 2 == 1:
			self._context.set_state(self._white, 'white')
			self._game.ai_move(self._context)
		elif self._blue != 'human' and self._turn_num %2 == 0:
			self._context.set_state(self._blue, 'blue')
			self._game.ai_move(self._context)
		board = self._game.git_board()
		for i in range(25):
			e = self._buttons[i]
			cold = (i % 5)
			rowd = i // 5
			strb = str(board[cold][rowd][0])
			strb += board[cold][rowd][1]
			e.configure(text = strb[:])
		if self._game._check_if_winner():
			self.labe['text'] = self._game._check_if_winner() + " wins!"
			for e in self._buttons:
				e.destroy()
			self._aim.destroy()
			if self.__undo == 'on':
				self.undo.destroy()
				self.redo.destroy()
				self.next.destroy()
			return
		self._turn_num += 1
		if self._game.git_type_player() != 'h':
			self.labe['text'] = 'Make AI move.'
		else:
			self.labe['text'] = 'Select a worker.'
		self._display_turn()
		self._highlight_workers()
				
	def _display_turn(self):
		if self._turn_num != 1:
			self._turn.destroy()
		self._turn = tk.Frame(self._window)
		
		z = self._game.git_curr_player()
        
        # print score
		if self._score == 'on':
			s = self._game.git_score()
			lab = tk.Label(self._turn, text="Turn:")
			lab1 = tk.Label(self._turn, textvariable=self._turn_num)
			lab2 = tk.Label(self._turn, text=z)
			lab3 = tk.Label(self._turn, text=s[0])
			lab4 = tk.Label(self._turn, text=s[1])
			lab5 = tk.Label(self._turn, text=s[2])
			lab.pack()
			lab1.pack()
			lab2.pack()
			lab3.pack()
			lab4.pack()
			lab5.pack()
			
		else:
			lab = tk.Label(self._turn, text="Turn:")
			lab1 = tk.Label(self._turn, text=self._turn_num)
			lab2 = tk.Label(self._turn, text=z)
			lab.pack()
			lab1.pack()
			lab2.pack()
		self._turn.grid(row=6, column =1)
		return


	def _run(self):
		if self._white == 'human':
			self.labe = tk.Label(self._instruction, text="Select Worker.")
		else:
			self.labe = tk.Label(self._instruction, text="Make AI move.")
     
		self.labe.pack()
		self._display_turn()
		self._highlight_workers()
		

	def _highlight_workers(self):
		z = self._game.git_curr_player()
		if z == "white (AB)":
			for b in self._buttons:
				if b['text'] == '0A' or b['text'] == '1A' or b['text'] == '2A':
					x = b.config(fg='red')
				elif b['text'] == '0B' or b['text'] == '1B' or b['text'] == '2B':
					y = b.config(fg='red')
				elif b['text'] == '3Y' or b['text'] == '3Z':
					self._win = tk.Frame(self._window)
					self.labe = tk.Label(self._win, text="Blue has won.")
					self.labe.pack()
				else:
					k = b.config(fg='black')
		else:
			for b in self._buttons:
				if b['text'] == '0Y' or ['text'] == '1Y' or b['text'] == '2Y':
					x = b.config(fg='red')
				elif b['text'] == '0Z' or b['text'] == '1Z' or b['text'] == '2Z':
					y = b.config(fg='red')
				elif b['text'] == '3A' or b['text'] == '3B':
					self._win = tk.Frame(self._window)
					self.labe = tk.Label(self._win, text="White has won.")
					self.labe.pack()
				else:
					k = b.config(fg='black')	
		return
					
	def _check_if_winner(self):
		return self._game._check_if_winner()
