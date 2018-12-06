import logging
import sys
import os

# Constants

SCRIPT_DIR = os.path.dirname(sys.argv[0])

LOG_FORMAT = '%(obj_name)s %(asctime)-15s: %(message)s'
LOG_DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p'
CANVAS_MANAGER_NAME = 'canv-manager-%d'

# Global Variables

cur_id = 0


class SingleCanvasManager:
    def __init__(self, canvas):
        global cur_id

        self.canvas = canvas
        self.selected = None
        self.selected_type = None

        # Logging Initialization

        self.debug_name = CANVAS_MANAGER_NAME % cur_id

        self.logger = logging.getLogger(self.debug_name)
        self.change_log_level()

        stdout_handle = logging.StreamHandler(sys.stdout)
        file_handle = logging.FileHandler(os.path.join(SCRIPT_DIR, 'latest.log'))

        self.prepare_log_stream(stdout_handle)
        self.prepare_log_stream(file_handle)

        cur_id += 1

        # Event Handler Initialization

        canvas.bind('<ButtonPress-1>', self.on_begin_drag)
        canvas.bind('<B1-Motion>', self.on_move_drag)
        canvas.bind('<ButtonRelease-1>', self.on_end_drag)

    def change_log_level(self, level=logging.INFO):
        self.logger.setLevel(level)

    def prepare_log_stream(self, stream):
        stream.setFormatter(logging.Formatter(fmt=LOG_FORMAT))
        self.logger.addHandler(stream)

    def debug(self, msg, level=logging.INFO):
        self.logger.log(level, msg, extra={'obj_name': self.debug_name})

    def on_begin_drag(self, evt):
        self.debug('Mouse press at (%d, %d)' % (evt.x, evt.y))

    def on_move_drag(self, evt):
        pass

    def on_end_drag(self, evt):
        self.debug('Mouse release at (%d, %d)' % (evt.x, evt.y))
