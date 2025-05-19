import shapely
from shapely import Point, Polygon, LineString
from shapely.ops import split


class Plane:

    @staticmethod
    def side(pointX, pointY, lineStart, lineEnd):
        """

        Return a value indicating if the given point x,y is LEFT, RIGHT, or ON a
        line intersecting a plane bounded by 0,1 with both X and Y origins in
        upper left.

        -1 = point is LEFT of line
         0 = point is ON of line
         1 = point is RIGHT of line

         If the point is not contained in the playfield at all (that is, if it's
         not in a plane bounded by 0,1) then the return result is unreliable

        """
        lineStartX, lineStartY = lineStart
        lineEndX, lineEndY = lineEnd
        playfield = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        line = LineString([(lineStartX, lineStartY), (lineEndX, lineEndY)])
        # split the playfield on the line, returning two polygons (or one if line doesn't intersect playfield)
        split_result = split(playfield, line)
        # print("            point           " + str(Point(pointX, pointY)))
        # print("            split result    " + str(split_result))
        # print("            len(split_result.geoms) " + str(len(split_result.geoms)))

        left_poly_contains_point = shapely.contains(
            split_result.geoms[0], Point(pointX, pointY)
        )

        right_poly_contains_point = False
        if len(split_result.geoms) > 1:
            right_poly_contains_point = shapely.contains(
                split_result.geoms[1], Point(pointX, pointY)
            )

        if left_poly_contains_point:
            # print("            point is LEFT of the line")
            return -1
        elif right_poly_contains_point:
            # print("            point is RIGHT of the line")
            return 1
        else:
            # print("            point is ON the line")
            return 0

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
