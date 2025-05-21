from ...util.color import Color

class ExtraBossesLightShowHandler:

    def __init__(self, machine, lerp_interval):
        self.__machine = machine
        self.__extra_bosses_loop_count = 0
        self.__extra_bosses_lerp_interval = lerp_interval
        

    def extra_bosses_step_handler(self, **kwargs):

        for lerp_light in kwargs["lerp_lights"]:
            lerp = float(
                self.__extra_bosses_loop_count % self.__extra_bosses_lerp_interval
            )
            if lerp != 0:
                lerp = 1 / self.__extra_bosses_lerp_interval * lerp

            # the lerp_light parameter is an list containing first the light name followed
            # by any number of colors that serve as "stops" on the lerp
            # path. So pass a sliced array [1:] yielding all but the first element
            # to the multistop lerper
            lerp_color = Color.lerp_multistop(lerp_light[1:], lerp)

            self.__machine.lights[lerp_light[0]].color(lerp_color)

    def extra_bosses_loop_handler(self, **kwargs):
        self.__extra_bosses_loop_count += 1

    def extra_bosses_stop_handler(self, **kwargs):
        self.__extra_bosses_loop_count = 0
