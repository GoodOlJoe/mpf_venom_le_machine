from mpf.core.mode import Mode
from mpf.core.rgb_color import RGBColor

# https://missionpinball.org/latest/code/introduction/mode_code/
# https://colordesigner.io/gradient-generator
class Attract(Mode):

    def mode_init(self):
        self.__start_color = (255, 4, 217)
        self.__end_color = (81, 255, 0)  # blue
        self.__loop_count = 0
        self.__lerp_interval = 10

    def mode_start(self, **kwargs):

        print("My custom mode code is starting")

        # what player are we?
        # print(self.player.number)

        # what's the player's score?
        # print('Score: {}'.format(self.player.score))

        self.add_mode_event_handler(
            "attract_extra_bosses_light_show_settings", self.settings_handler
        )
        self.add_mode_event_handler(
            "attract_extra_bosses_light_show_auto_step", self.step_handler
        )
        self.add_mode_event_handler(
            "attract_extra_bosses_light_show_looped", self.loop_handler
        )
        self.add_mode_event_handler(
            "attract_extra_bosses_light_show_stopped", self.stop_handler
        )

    @staticmethod
    def lerp_color(color1, color2, amount):
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
    def lerp_color_multistop(colors, amount):
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

        return Attract.lerp_color(start_color, end_color, scaled_amount)

    def settings_handler(self, **kwargs):
        self.__lerp_interval = kwargs["lerp_interval"]

    def step_handler(self, **kwargs):

        for lerp_light in kwargs["lerp_lights"]:
            # print("    typeof(lerp_light) " + str(type(lerp_light)))

            lerp = float(self.__loop_count % self.__lerp_interval)
            if lerp != 0:
                lerp = 1 / self.__lerp_interval * lerp

            # the lerp_light parameter is an list containing first the light name followed
            # by any number of colors that serve as "stops" on the lerp
            # path. So pass a sliced array [1:] yielding all but the first element
            # to the multistop lerper
            lerp_color = Attract.lerp_color_multistop(lerp_light[1:], lerp)

            self.machine.lights[lerp_light[0]].color(lerp_color)

    def loop_handler(self, **kwargs):
        self.__loop_count += 1

    def stop_handler(self, **kwargs):
        self.__loop_count = 0
