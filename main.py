import tkinter as tk
import util

WIDTH = 600
HEIGHT = 600
BACK_CLR = 'lemon chiffon'

root = tk.Tk()
canvas = tk.Canvas(master=root, width=WIDTH, height=HEIGHT)
canvas.pack()

manager = util.SingleCanvasManager(canvas)

tk.mainloop()
