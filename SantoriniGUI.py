import tkinter as tk


class SantoriniGUI():
	def __init__(self, white='human', blue='human', undo='off', score='off'):
		self._white = white
		self._blue = blue
		self._undo = undo
		self._score = score
		self._window = tk.Tk()
		self._window.title("Santorini")
		# c = tk.Canvas(self._window, width=500, height=500)
		# for x in range(5):
		# 	for y in range(5):
		# 		x_top_left = x * 100
		# 		y_top_left = y * 100
		# 		x_bottom_right = x_top_left + 100
		# 		y_bottom_right = y_top_left + 100

		# 		c.create_rectangle(x_top_left, y_top_left, x_bottom_right, y_bottom_right, fill="white", outline = 'black')
		# c.pack()
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

		if self._undo == 'on':
			self._undo = tk.Frame(self._window)
			undo=tk.Button(self._undo, text="Undo")
			undo.grid(row=0, column=0)
			redo=tk.Button(self._undo, text="Redo")
			redo.grid(row=0, column=1)
			next=tk.Button(self._undo, text="Next")
			next.grid(row=0, column=2)

			self._undo.grid(row=5, column =1)
			
		self._window.mainloop()

