from base.sprite import Sprite, Shape
from util import rectangular_offset, shifted_rectangular_offset

BODY_WIDTH = 30
BODY_HEIGHT = 3


class DefaultMirror(Sprite):
    def __init__(self, parent):
        """
        :param parent: Parent Canvas
        """

        self.body = Shape(parent, rectangular_offset(BODY_WIDTH, BODY_HEIGHT), fill='cyan')

        super().__init__(parent, BODY_WIDTH, BODY_HEIGHT, self.body)

    @property
    def slope(self):
        f