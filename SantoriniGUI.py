import tkinter as tk
import sys
from Exception import InvalidMove, InvalidBuild, InvalidWorker, WrongMove, WrongBuild, WrongWorker
from Game import Game
from Players import Player
from random import choice

class SantoriniGUI():
	def __init__(self, white='human', blue='human', undo='off', score='off'):
		self._white = white
		self._blue = blue
		self._setter = False
		self._undo = undo
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
		self._turn = tk.Frame(self._window)
		self._instruction = tk.Frame(self._window)
		self._instruction.grid(row=7, column = 0)



		if self._undo == 'on':
			self._undo = tk.Frame(self._window)
			self.undo=tk.Button(self._undo, text="Undo")
			self.undo.grid(row=0, column=0)
			self.redo=tk.Button(self._undo, text="Redo")
			self.redo.grid(row=0, column=1)
			self.next=tk.Button(self._undo, text="Next")
			self.next.grid(row=0, column=2)

			self._undo.grid(row=5, column =1)
		self._display_turn()
		self._run()
		self._window.mainloop()

	def _press(self, row, col):
		if self._setter == False:
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
				self.labe['text'] = 'Select a direction to move (n, ne, e, se, s, sw, w, nw)'
				self._setter = True
		else:
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
				self._setter = False
				for e in self._buttons:
					e['highlightbackground'] = 'white'
				p = self._game.git_curr_player()[0]

				g = Player(p)
				z = g._pick_build([col, row], board, self._mover[0])
				self._game.make_move(self._mover[0], self._mover[1], z)
				self._setter = False
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
				if self._undo == 'on':
					self.undo.destroy()
					self.redo.destroy()
					self.next.destroy()

				
				
	def _display_turn(self):
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


	def _run(self):
		# while not self._check_if_winner():
		# 	worker = None
		# 	move = None
		# 	build = None	
		# 	if self._game.git_type_player() == 'h':
				# while not worker:
                    #add method to check if either worker can move
					# if self._game.cant_move == True:
					# 	pass
	
		self.labe = tk.Label(self._instruction, text="Select Worker.")
		self.labe.pack()
		self._highlight_workers()

	def _highlight_workers(self):
		z = self._game.git_curr_player()
		if z == "white (AB)":
			for b in self._buttons:
				if b['text'] == 'A':
					x = b.config(fg='red')
				if b['text'] == 'B':
					x = b.config(fg='red')
		else:
			for b in self._buttons:
				if b['text'] == 'Y':
					x = b.config(fg='red')
				if b['text'] == 'Z':
					x = b.config(fg='red')
					
	def _check_if_winner(self):
		return self._game._check_if_winner()
