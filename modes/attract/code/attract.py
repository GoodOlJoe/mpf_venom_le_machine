from mpf.core.mode import Mode

from ...util.plane import Plane
from ...util.color import Color

# https://missionpinball.org/latest/code/introduction/mode_code/
# https://colordesigner.io/gradient-generator
class Attract(Mode):

    def mode_init(self):
        self.__start_color = (255, 4, 217)
        self.__end_color = (81, 255, 0)  # blue
        self.__loop_count = 0
        self.__lerp_interval = 10

    def mode_start(self, **kwargs):

        # extra bosses light show
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
            lerp_color = Color.lerp_multistop(lerp_light[1:], lerp)

            self.machine.lights[lerp_light[0]].color(lerp_color)

    def loop_handler(self, **kwargs):
        self.__loop_count += 1

    def stop_handler(self, **kwargs):
        self.__loop_count = 0
