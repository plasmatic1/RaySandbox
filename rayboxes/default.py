from base.sprite import Sprite, Shape
from util import rectangular_offset, shifted_rectangular_offset

BODY_RADIUS = 20
LASER_RADIUS = 2


class DefaultRayBox(Sprite):
    def __init__(self, parent):
        """
        :param parent: Parent Canvas
        """

        self.body = Shape(parent, rectangular_offset(BODY_RADIUS, BODY_RADIUS), fill='black')
        self.laser = Shape(parent, shifted_rectangular_offset(BODY_RADIUS // 2, LASER_RADIUS, BODY_RADIUS // 2, 0), fill='red')

        super().__init__(parent, BODY_RADIUS, BODY_RADIUS, self.body, self.laser)
