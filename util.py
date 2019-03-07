class LineSegment:
    def __init__(self, x1, y1, x2, y2):
        """
        :param x1: X coordinate of the first point
        :param y1: Y coordinate of the first point
        :param x2: X coordinate of the second point
        :param y2: Y coordinate of the second point
        """

        if x1 == x2:
            self.vertical = True
            self.x_int = x1
        else:
            self.vertical = False
            self.slope = (y2 - y1) / (x2 - x1)
            self.y_int = y1 - self.slope * x1

        self.x1 = x1
        self.x2 = x2

    def calculate(self, x):
        """
        Calculates the y coordinate for a given x coordinate.  If the line is vertical, an error will be raised
        :param x: The given x coordinate
        :return: The y coordinate for that x coordinate
        """

        if self.vertical:
            raise ArithmeticError('Cannot calculate y value for vertical line!')

        return self.slope * x + self.y_int

    def intersects(self, other):
        """
        Finds the x coordinate of the intersection between this line and another line, or None if they do not intersect
        :param other: The other line
        :return: The intersection of the two lines, or None if they don't intersect
        """

        if self.vertical and other.vertical:
            if self.x_int != other.x_int:
                return None
        # TODO: FINISH METHOD


def rectangular_offset(width, height):
    """
    Creates offsets for a rectangular Shape object.  This is used in the shape constructor
    :param width: The width of the rectangle
    :param height: The height of the rectangle
    :return: The offsets for the rectangle
    """

    return [(-width, height), (width, height), (width, -height), (-width, -height)]


def shifted_rectangular_offset(width, height, xshift, yshift):
    """
    Creates offsets for a rectangular Shape object, but allows for shifting of the x and y values
    :param width: The width of the rectangle
    :param height: The height of the rectangle
    :param xshift: The x shift of the rectangle
    :param yshift: The y shift of the rectangle
    :return: The offsets for the rectangle
    """

    return [(x + xshift, y + yshift) for x, y in rectangular_offset(width, height)]
