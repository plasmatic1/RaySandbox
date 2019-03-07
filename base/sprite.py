from math import atan2, sqrt, pi, cos, sin

from errors import StateError


class Sprite:
    def __init__(self, parent, box_width_radius, box_height_radius, *shapes):
        """
        :type box_height_radius: The height of the bounding box.  The bounds will be x +- box_height / 2
        :type box_width_radius: The width of the bounding box.  The bounds will be x +- box_width / 2
        :param parent: The parent canvas
        :param shapes: A list of shapes that comprise the Sprite object, note that their centres should all be set
        to (0, 0) for it to work properly.  Note that the shapes are drawn in list order
        :param rotation: The rotation, in degrees
        """

        self.x = 0
        self.y = 0
        self.rotation = 0

        self.box_width_radius = box_width_radius
        self.box_height_radius = box_height_radius

        self.parent = parent
        self.shapes = shapes

    def contains(self, x, y):
        """
        Checks if a coordinate pair (x, y) is within the bounds of this sprite
        :param x: The x coordinate
        :param y: The y coordinate
        :return: Whether the coordinate is within the bounding box of the sprite
        """

        x1 = self.x - self.box_width_radius
        x2 = self.x + self.box_width_radius
        y1 = self.y - self.box_height_radius
        y2 = self.y + self.box_height_radius

        return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)

    def _update_pos(self):
        """
        Updates the positions of all the shapes of the
        :return: Nothing
        """

        for shape in self.shapes:
            shape.centre_x = self.x
            shape.centre_y = self.y
            shape.rotation = self.rotation

    def draw(self):
        """
        Draws all the shapes in this sprite
        :return: Nothing
        """

        for shape in self.shapes:
            shape.draw()

    def update(self):
        """
        Updates all the shapes in this sprite
        :return: Nothing
        """

        self._update_pos()
        for shape in self.shapes:
            shape.update()

    def delete(self):
        """
        Deletes all the shapes in this sprite
        :return: Nothing
        """

        for shape in self.shapes:
            shape.delete()

    def change_rotation(self, change):
        """
        Changes rotation by a specified amount
        :param change: The change delta
        :return: Nothing
        """

        self.rotation -= change


class Shape:
    def __init__(self, parent, offsets, **options):
        """
        :param parent: Parent canvas object
        :param offsets: The offset of each point relative to the centre, represented as a list of (x, y)
        :param rotation: The rotation of the shape, in radians
        :param options: Any other options for the shape
        """

        self.options = options
        self.centre_x = 0
        self.centre_y = 0
        self.rotation = 0
        self.parent = parent
        self._id = None

        """
        Calculating the coordinates of the shape depending on rotation would mean a lot of work if the 
        coordinates had to be computed each time.  Precomputing them at the start saves on a lot of time.
        
        radii: The radii of the circles that each point makes
        angles: The angle of each point along the circle
        """

        self.radii = []
        self.angles = []

        for x_offset, y_offset in offsets:
            self.angles.append(atan2(y_offset, x_offset))
            self.radii.append(sqrt(x_offset * x_offset + y_offset * y_offset))

    def _convert_pos(self, pos):
        """
        Converts cartesian plane coordinates to screen coordinates.  This is because y=0 on the screen is actually
        the top, not the bottom
        :param pos: A list of (x, y) tuples containing the coordinates
        :return: Another list of (x, y) tuples that contain the transformed coordinates
        """

        height = float(self.parent['height'])
        return [height - x if i % 2 else x for i, x in enumerate(pos)]

    @property
    def _pos(self):
        """
        Calculates the current coordinates of the shape
        :return: A list of (x, y) tuples containing the coordinates of the polygon
        """

        rotation_radians = self.rotation * pi / 180.
        pos = []

        for angle, radius in zip(self.angles, self.radii):
            pos.append(cos(angle + rotation_radians) * radius + self.centre_x)
            pos.append(sin(angle + rotation_radians) * radius + self.centre_y)

        return self._convert_pos(pos)

    def update(self):
        """
        Updates the position and rotation of the shape on the canvas
        :return: Nothing
        """

        if not self._id:
            raise StateError('Shape not initialized!')
        self.parent.coords(self._id, *self._pos)

    def draw(self):
        """
        Draws the shape onto the canvas, or raises an error if it's already been drawn.
        :return: Nothing
        """

        if self._id:
            raise StateError('Shape already initialized')
        self._id = self.parent.create_polygon(*self._pos, **self.options)
        self.parent.tag_raise(self._id)

    def delete(self):
        """
        Deletes the shape from the canvas, or raises an error if it hasn't been drawn yet.
        :return: Nothing
        """

        if not self._id:
            raise StateError('Shape not initialized!')
        self.parent.delete(self._id)
        self._id = None
