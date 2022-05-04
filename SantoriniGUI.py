import tkinter as tk
import sys
from Exception import InvalidMove, InvalidBuild, InvalidWorker, WrongMove, WrongBuild, WrongWorker
from Game import Game


class SantoriniGUI():
	def __init__(self, white='human', blue='human', undo='off', score='off'):
		self._white = white
		self._blue = blue
		self._undo = undo
		self._score = score
		self._turn_num = 1
		self._window = tk.Tk()
		self._window.title("Santorini")

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
					button=tk.Button(self._board, text='Y')
				elif col == 1 and row == 3: 
					button=tk.Button(self._board, text='B')
				elif col == 3 and row == 1:
					button=tk.Button(self._board, text='A')
				elif col == 3 and row == 3:
					button=tk.Button(self._board, text='Z')
				else:
					button=tk.Button(self._board)
				button.grid(row=row, column=col)
				self._buttons.append(button)

		self._board.grid(row=0, column=1)
		self._turn = tk.Frame(self._window)
		self._instruction = tk.Frame(self._window)
		self._instruction.grid(row=7, column = 0)



		if self._undo == 'on':
			self._undo = tk.Frame(self._window)
			undo=tk.Button(self._undo, text="Undo")
			undo.grid(row=0, column=0)
			redo=tk.Button(self._undo, text="Redo")
			redo.grid(row=0, column=1)
			next=tk.Button(self._undo, text="Next")
			next.grid(row=0, column=2)

			self._undo.grid(row=5, column =1)
		self._display_turn()
		self._run()
		self._window.mainloop()


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
	
		lab = tk.Label(self._instruction, text="Select Worker.")
		lab.pack()
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
