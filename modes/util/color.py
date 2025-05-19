from mpf.core.rgb_color import RGBColor

class Color:

    @staticmethod
    def lerp(color1, color2, amount):
        """
        Interpolates linearly between two RGB colors.

        Args:
            color1: Tuple (R, G, B) representing the first color (0-255).
            color2: Tuple (R, G, B) representing the second color (0-255).
            amount: Float between 0 and 1 representing the interpolation factor.

        Returns:
            Tuple (R, G, B) representing the interpolated color.
        """
        r1, g1, b1 = color1
        r2, g2, b2 = color2

        r = int(r1 + (r2 - r1) * amount)
        g = int(g1 + (g2 - g1) * amount)
        b = int(b1 + (b2 - b1) * amount)

        return (r, g, b)

    @staticmethod
    def lerp_multistop(colors, amount):
        """
        Interpolates linearly along a path of colors, where the path
        is a set of colors. So if the path is [blue, green, red, purple]
        the path is the linear interpolation (lerp) from blue to green, followe
        by the lerp from green to red, followed by the lerp from red to purple.

        Args:
            colors: An array of two or more (R, G, B) tuples representing stops on the path
            amount: Float between 0 and 1 representing the interpolation scaled to the entire path, that is the
            percentage of travel from the first color to the last color.

        Returns:
            Tuple (R, G, B) representing the interpolated color.
        """
        stop_count = len(colors)

        if stop_count < 2:
            raise AssertionError("A multistop lerp requires at least 2 stops")

        if 0 == amount:
            return colors[0]

        if 1 == amount:
            return colors[-1]

        segment_size = 1 / float(stop_count - 1)  # how big is each segment of the path
        remainder = amount % segment_size
        # which segment of of the path are we in
        segment_index = int((amount - remainder) / segment_size)
        # scale the amount to the two end points of this segment
        scaled_amount = remainder / segment_size

        start_color = RGBColor.string_to_rgb(colors[segment_index])
        end_color = RGBColor.string_to_rgb(colors[segment_index + 1])

        return Color.lerp(start_color, end_color, scaled_amount)

