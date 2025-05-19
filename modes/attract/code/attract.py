from mpf.core.mode import Mode

from ...util.plane import Plane
from ...util.color import Color


# https://missionpinball.org/latest/code/introduction/mode_code/
# https://colordesigner.io/gradient-generator
class Attract(Mode):

    def mode_init(self):
        # region extra bosses light show properties
        self.__extra_bosses_loop_count = 0
        self.__extra_bosses_lerp_interval = 10
        # endregion
        # region wipe ul to lr light show properties
        self.__wipe_ul_to_lr_loop_count = 1
        # how many steps to complete a wipe of the whole playfield
        self.__wipe_ul_to_lr_steps_per_wipe = 20.0
        # endregion

    def mode_start(self, **kwargs):
        # region extra bosses light show
        self.add_mode_event_handler(
            "attract_extra_bosses_light_show_settings",
            self.extra_bosses_settings_handler,
        )
        self.add_mode_event_handler(
            "attract_extra_bosses_light_show_auto_step", self.extra_bosses_step_handler
        )
        self.add_mode_event_handler(
            "attract_extra_bosses_light_show_looped", self.extra_bosses_loop_handler
        )
        self.add_mode_event_handler(
            "attract_extra_bosses_light_show_stopped", self.extra_bosses_stop_handler
        )
        # endregion
        # region Wipe UL to LR light show
        # self.add_mode_event_handler(
        #     "attract_wipe_ul_to_lr_light_show_settings",
        #     self.wipe_ul_to_lr_settings_handler,
        # )
        self.add_mode_event_handler(
            "attract_wipe_ul_to_lr_light_show_auto_step",
            self.wipe_ul_to_lr_step_handler,
        )
        self.add_mode_event_handler(
            "attract_wipe_ul_to_lr_light_show_looped", self.wipe_ul_to_lr_loop_handler
        )
        self.add_mode_event_handler(
            "attract_wipe_ul_to_lr_light_show_stopped", self.wipe_ul_to_lr_stop_handler
        )
        # endregion

    # region  Wipe UL to LR Light Show Handlers
    def wipe_ul_to_lr_step_handler(self, **kwargs):

        if self.__wipe_ul_to_lr_loop_count >= self.__wipe_ul_to_lr_steps_per_wipe + 1:
            self.__wipe_ul_to_lr_loop_count = 1

        # this wipe is simple linear so the line's endpoints will always be
        # n,0 and 0,n
        increment = 1 / (self.__wipe_ul_to_lr_steps_per_wipe / 2)
        # sx = sy = ex = ey = increment

        # for i in range( 1,int(self.__wipe_ul_to_lr_steps_per_wipe)+1 ):
        #     print ( f'{i:{0}>2}:   {round(sx,2):.1f}, {round(sy,2):.1f} ....   {round(ex,2):.1f}, {round(ey,2):.1f}')

        # set increment
        # sy and ex
        #     increment
        #     clamp to 1
        # sx and ey
        #     0 until sy >= 1
        #     then start incrementing

        ex = increment * self.__wipe_ul_to_lr_loop_count
        if ex > 1.0:
            ex = 1.0
        sy = ex

        if sy < 1:
            ey = 0
        else:
            ey = (increment * self.__wipe_ul_to_lr_loop_count) - 1
        sx = ey

        # this wipe is simple linear so the line's endpoints will always be
        # n,0 and 0,n
        # increment = 1 / self.__wipe_ul_to_lr_steps_per_wipe
        # endpoint = self.__wipe_ul_to_lr_loop_count * increment
        result = Plane.side(0.4, 0.4, (sx, sy), (ex, ey))
        # print("    wipe step")
        # print(f"        loop count {str(self.__wipe_ul_to_lr_loop_count)}")
        # print(f"        increment  {str(increment)}")
        # print(
        #     f"        line       ({round(sx,2):.1f}, {round(sy,2):.1f})    ({round(ex,2):.1f}, {round(ey,2):.1f})"
        # )
        # print(f"        side       {result}")
        # print(f"        is left of {str(-1 == result)}")

    # def wipe_ul_to_lr_settings_handler(self, **kwargs):
    #     self.__wipe_ul_to_lr_lerp_interval = kwargs["lerp_interval"]

    def wipe_ul_to_lr_loop_handler(self, **kwargs):
        self.__wipe_ul_to_lr_loop_count += 1

    def wipe_ul_to_lr_stop_handler(self, **kwargs):
        self.__wipe_ul_to_lr_loop_count = 0

    # endregion
    # region  Extra Bosses Light Show Handlers
    def extra_bosses_step_handler(self, **kwargs):

        for lerp_light in kwargs["lerp_lights"]:
            # print("    typeof(lerp_light) " + str(type(lerp_light)))

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

            self.machine.lights[lerp_light[0]].color(lerp_color)

    def extra_bosses_settings_handler(self, **kwargs):
        self.__extra_bosses_lerp_interval = kwargs["lerp_interval"]

    def extra_bosses_loop_handler(self, **kwargs):
        self.__extra_bosses_loop_count += 1

    def extra_bosses_stop_handler(self, **kwargs):
        self.__extra_bosses_loop_count = 0

    # endregion
