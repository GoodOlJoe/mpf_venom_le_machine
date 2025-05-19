import shapely
from shapely import Point, Polygon, LineString
from shapely.ops import split


class Plane:

    @staticmethod
    def left_of(pointX, pointY, lineStart, lineEnd):
        """

        Return true if the given point x,y is LEFT OF or ON a line intersecting
        a plane bounded by 0,1 with both X and Y origins in upper left.
        Otherwise return false

        """
        lineStartX, lineStartY = lineStart
        lineEndX, lineEndY = lineEnd
        playfield = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        line = LineString([(lineStartX, lineStartY), (lineEndX, lineEndY)])
        result = split(playfield, line) # split the playfield on the line, returning two polygons
        return shapely.contains(playfield, Point(pointX, pointY))


    @staticmethod
    def bounded(box_ulX, box_ulY, box_lrX, box_lrY, x, y):
        """

        Return -1, 0, 1 indicating the position of a given point x,y relative to
        a bounding box within a plane bounded by 0,1 with both X and Y origins
        in upper left.

        -1 - the point is outside of the bounding box
         0 - the point is on the bounding box
         1 - the point is inside the bounding box

        """

        if x < box_ulX or x > box_lrX or y < box_ulY or y > box_lrY:
            return -1
        elif x > box_ulX and x < box_lrX and y > box_ulY and y < box_lrY:
            return 1
        else:
            return 0
