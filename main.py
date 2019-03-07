import tkinter as tk
import time
from threading import Thread

from managers import SingleCanvasManager
from mirrors.default import DefaultMirror
from rayboxes.default import DefaultRayBox

WIDTH = 600
HEIGHT = 600
BACK_CLR = 'lemon chiffon'

root = tk.Tk()
canvas = tk.Canvas(master=root, width=WIDTH, height=HEIGHT)
canvas.pack()

manager = SingleCanvasManager(canvas, root)


def makespr(f=True, constructor=DefaultRayBox):
    sprite = constructor(canvas)
    manager.add_sprite(sprite, f)

    sprite.x = 200
    sprite.y = 200
    sprite.update()

    return sprite


sprite = makespr()
makespr()
makespr(0)

makespr(True, DefaultMirror)

tk.mainloop()
