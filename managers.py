import logging
import sys
import os

# Constants

SCRIPT_DIR = os.path.dirname(sys.argv[0])

LOG_FORMAT = '%(obj_name)s %(asctime)-15s: %(message)s'
LOG_DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p'
CANVAS_MANAGER_NAME = 'canv-manager-%d'

DEBUG_ON = False

# Global Variables

cur_id = 0


class SingleCanvasManager:
    def __init__(self, canvas, root):
        """
        :param canvas: The canvas that's being managed
        :param root: The root (Tk object) that the canvas is on
        """

        global cur_id

        self.canvas = canvas
        self.root = root
        self.selected = None
        self.selected_type = None

        # Sizes

        self.height = float(canvas['height'])

        # Sprite List

        self.sprites = {}
        self.draggable = set()
        self.curr_sprite = None  # Current Sprite being moved

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

        self.canvas.bind('<ButtonPress-1>', self.on_begin_drag)
        self.canvas.bind('<B1-Motion>', self.on_move_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_end_drag)
        self.root.bind('<Key>', self.on_key)

    # =======================[ UTILITY FUNCTIONS ]=======================

    def add_sprite(self, sprite, draggable=True):
        """
        Adds a sprite into the screen
        :param sprite: The sprite
        :param draggable: Whether it is draggable or not
        :return: Nothing
        """

        sprite_id = id(sprite)

        self.sprites[sprite_id] = sprite
        if draggable:
            self.draggable.add(sprite_id)
        sprite.draw()

    def remove_sprite(self, sprite):
        """
        Removes a sprite from the screen
        :param sprite: The sprite
        :return: Nothing
        """

        sprite_id = id(sprite)

        del self.sprites[sprite_id]
        self.draggable.discard(sprite_id)
        sprite.delete()

    # =======================[ DEBUGGING ]===============================

    def change_log_level(self, level=logging.INFO):
        """
        Changes log level
        :param level: The logging level
        :return: Nothing
        """

        self.logger.setLevel(level)

    def prepare_log_stream(self, stream):
        """
        Prepares log stream (Sets formatting and adds it as a handler to the logger)
        :param stream: The logging stream to prepare
        :return: Nothing
        """

        stream.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
        self.logger.addHandler(stream)

    def debug(self, msg, level=logging.INFO):
        """
        Logs the message onto the debug stream
        :param msg: The message to log
        :param level: The logging level of the message, defaults to logging.INFO
        :return: Nothing
        """

        if DEBUG_ON:
            self.logger.log(level, msg, extra={'obj_name': self.debug_name})

    # =======================[ EVENT LISTENERS ]=========================

    def on_begin_drag(self, evt):
        """
        On begin drag event
        :param evt: The event object
        :return: Nothing
        """

        evt.y = self.height - evt.y
        self.debug('Mouse press at (%d, %d)' % (evt.x, evt.y))

        assert self.curr_sprite is None

        for sprite_id in self.draggable:
            sprite = self.sprites[sprite_id]
            if sprite.contains(evt.x, evt.y):
                self.curr_sprite = sprite
                break

    def on_move_drag(self, evt):
        """
        On move drag event
        :param evt: The event object
        :return: Nothing
        """

        evt.y = self.height - evt.y
        if self.curr_sprite:
            self.curr_sprite.x = evt.x
            self.curr_sprite.y = evt.y
            self.curr_sprite.update()

    def on_end_drag(self, evt):
        """
        On end drag event
        :param evt: The event object
        :return: Nothing
        """

        evt.y = self.height - evt.y
        self.debug('Mouse release at (%d, %d)' % (evt.x, evt.y))

        if self.curr_sprite:
            self.curr_sprite.x = evt.x
            self.curr_sprite.y = evt.y
            self.curr_sprite.update()
            self.curr_sprite = None

    def on_key(self, evt):
        """
        On key event
        :param evt: The event object
        :return: Nothing
        """

        self.debug('Key event (%s)' % evt)

        if self.curr_sprite:
            if evt.char == 'a':
                self.curr_sprite.change_rotation(-5)
                self.curr_sprite.update()
            elif evt.char == 'd':
                self.curr_sprite.change_rotation(5)
                self.curr_sprite.update()
