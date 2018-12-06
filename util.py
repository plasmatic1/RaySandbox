import logging
import sys
import os

# Constants

SCRIPT_DIR = os.path.dirname(sys.argv[0])

LOG_FORMAT = '%(name)s %(asctime)-15s: %(message)s'
CANVAS_MANAGER_NAME = 'canv-manager-%d'

# Global Variables

logging.basicConfig(format=LOG_FORMAT)
cur_id = 0


class SingleCanvasManager:
    def __init__(self, canvas):
        global cur_id

        self.canvas = canvas
        self.selected = None

        self.debug_name = CANVAS_MANAGER_NAME % cur_id
        self.logger = logging.getLogger(self.debug_name)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.addHandler(logging.FileHandler(os.path.join(SCRIPT_DIR, 'latest.log')))
        cur_id += 1

        canvas.bind('<ButtonPress-1>', self.on_begin_drag)
        canvas.bind('<B1-Motion>', self.on_move_drag)
        canvas.bind('<ButtonRelease-1>', self.on_end_drag)

    def debug(self, msg, level=10):
        self.logger.log(level, msg, {'name': self.debug_name})

    def on_begin_drag(self, evt):
        print('magic')
        self.debug('Button press at (%d, %d)' % (evt.x, evt.y))

    def on_move_drag(self, evt):
        pass

    def on_end_drag(self, evt):
        pass
