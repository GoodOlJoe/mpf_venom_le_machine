import os
import pathlib

from mpf.core.mode import Mode

from ruamel import yaml

from ...util.plane import Plane
from ...util.color import Color
from ...util.playfield_layout import PlayfieldLayout


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
        self.__wipe_ul_to_lr_steps_per_wipe = 70
        # how many wipes to complete the color path
        self.__wipe_ul_to_lr_color_cycles_per_wipe = 0.5
        # amount to advance color path during each step
        # self.__wipe_ul_to_lr_lerp_increment = (
        #     self.__wipe_ul_to_lr_steps_per_wipe
        #     / self.__wipe_ul_to_lr_color_cycles_per_wipe
        # )
        # print ( f"!!!!!!!!!!self.__wipe_ul_to_lr_lerp_increment: {self.__wipe_ul_to_lr_lerp_increment}")
        # self.__wipe_ul_to_lr_color_path = ["FF0000", "00FF00", "FF00FF"]
        self.__wipe_ul_to_lr_color_path = ["red", "green", "blue"]
        # self.__wipe_ul_to_lr_color_path = ["red", "green", "purple", "blue", "green"]
        # endregion
        # region wipe r to l light show properties
        self.__wipe_r_to_l_loop_count = 1
        # how many steps to complete a wipe of the whole playfield
        self.__wipe_r_to_l_steps_per_wipe = 40
        # how many wipes to complete the color path
        self.__wipe_r_to_l_color_cycles_per_wipe = 0.5
        self.__wipe_r_to_l_color_path = ["purple", "red", "green"]
        # self.__wipe_r_to_l_color_path = ["red", "green", "purple", "blue", "green"]
        # endregion
        self.__machine_path = pathlib.Path().resolve()
        self.__playfield_layout = PlayfieldLayout(self.__machine_path)

    def mode_start(self, **kwargs):

        # print(f"Machine path (from pathlib.Path().resolve()) is {self.__machine_path}")

        # we need a list of all lights so we can do geometry-based wipe effects in light shows
        self.__playfield_layout = PlayfieldLayout(self.__machine_path)
        # print (self.__playfield_layout.lights().keys())

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
        # region Wipe R to L light show
        self.add_mode_event_handler(
            "attract_wipe_r_to_l_light_show_auto_step",
            self.wipe_r_to_l_step_handler,
        )
        self.add_mode_event_handler(
            "attract_wipe_r_to_l_light_show_looped", self.wipe_r_to_l_loop_handler
        )
        self.add_mode_event_handler(
            "attract_wipe_r_to_l_light_show_stopped", self.wipe_r_to_l_stop_handler
        )
        # endregion

    # region  Wipe R to L Light Show Handlers
    def wipe_r_to_l_step_handler(self, **kwargs):

        if self.__wipe_r_to_l_loop_count >= self.__wipe_r_to_l_steps_per_wipe + 1:
            self.__wipe_r_to_l_loop_count = 1

        # this wipe is simple linear so the line's endpoints will always be
        # n,0 and 0,n
        increment = 1 / (self.__wipe_r_to_l_steps_per_wipe)
        # sx = sy = ex = ey = increment

        # set start (sx,sy) and end (ex,ey) points for a slicing line for this iteration of the wipe
        ex = 1 - (increment * self.__wipe_r_to_l_loop_count)
        if ex < 0.0:
            ex = 1.0
        sx = ex

        sy = 0.0
        ey = 1.0

        # now check each light, turn it on if it's left of the line
        # else turn it off
        lights = self.__playfield_layout.lights()
        # print (f"!!!!! type(lights), lights is {type(lights)}, {lights}")
        for light in lights.items():
            # print (f"type(light), light is {type(light)}, {light}")
            light_name, light_pos = light
            # print (f"type(light_pos), light is {type(light_pos)}, {light_pos}")
            # print (f"{light_name}: x:{light_pos['x']} y:{light_pos['y']}")

            if "playfield_wipe" in self.machine.lights[light_name].tags:

                result = Plane.side(light_pos["x"], light_pos["y"], (sx, sy), (ex, ey))
                if 1 == result:

                    lerp_amount = (
                        1
                        / self.__wipe_r_to_l_steps_per_wipe
                        * self.__wipe_r_to_l_loop_count
                        * 0.8  # if this is >1 we crash somewhere, probably in the lerper, think about it
                    )
                    color = Color.lerp_multistop(
                        self.__wipe_r_to_l_color_path, lerp_amount
                    )
                    # print(f"!!!!!!! lerp_amount:{lerp_amount} color:{color}")
                    self.machine.lights[light_name].color(color)
            # else:
            #     self.machine.lights[light_name].off()

        # is_left_of =
        # print("    wipe step")
        # print(f"        loop count {str(self.__wipe_r_to_l_loop_count)}")
        # print(f"        increment  {str(increment)}")
        # print(
        #     f"        line       ({round(sx,2):.1f}, {round(sy,2):.1f})    ({round(ex,2):.1f}, {round(ey,2):.1f})"
        # )
        # print(f"        side       {result}")
        # print(f"        is left of {str(-1 == result)}")

    # def wipe_r_to_l_settings_handler(self, **kwargs):
    #     self.__wipe_r_to_l_lerp_interval = kwargs["lerp_interval"]

    def wipe_r_to_l_loop_handler(self, **kwargs):
        self.__wipe_r_to_l_loop_count += 1

    def wipe_r_to_l_stop_handler(self, **kwargs):
        self.__wipe_r_to_l_loop_count = 0

    # endregion
    # region  Wipe UL to LR Light Show Handlers
    def wipe_ul_to_lr_step_handler(self, **kwargs):

        if self.__wipe_ul_to_lr_loop_count >= self.__wipe_ul_to_lr_steps_per_wipe + 1:
            self.__wipe_ul_to_lr_loop_count = 1

        # this wipe is simple linear so the line's endpoints will always be
        # n,0 and 0,n
        increment = 1 / (self.__wipe_ul_to_lr_steps_per_wipe / 2)
        # sx = sy = ex = ey = increment

        # set start (sx,sy) and end (ex,ey) points for a slicing line for this iteration of the wipe
        ex = increment * self.__wipe_ul_to_lr_loop_count
        if ex > 1.0:
            ex = 1.0
        sy = ex

        if sy < 1:
            ey = 0
        else:
            ey = (increment * self.__wipe_ul_to_lr_loop_count) - 1
        sx = ey

        # now check each light, turn it on if it's left of the line
        # else turn it off
        lights = self.__playfield_layout.lights()
        # print (f"!!!!! type(lights), lights is {type(lights)}, {lights}")
        for light in lights.items():
            # print (f"type(light), light is {type(light)}, {light}")
            light_name, light_pos = light
            # print (f"type(light_pos), light is {type(light_pos)}, {light_pos}")
            # print (f"{light_name}: x:{light_pos['x']} y:{light_pos['y']}")

            if "playfield_wipe" in self.machine.lights[light_name].tags:

                result = Plane.side(light_pos["x"], light_pos["y"], (sx, sy), (ex, ey))
                if -1 == result:
                    # lerp_amount = (
                    #     self.__wipe_ul_to_lr_lerp_increment
                    #     * self.__wipe_ul_to_lr_loop_count
                    # )

                    lerp_amount = (
                        1
                        / self.__wipe_ul_to_lr_steps_per_wipe
                        * self.__wipe_ul_to_lr_loop_count
                        * 0.8  # if this is >1 we crash somewhere, probably in the lerper, think about it
                    )
                    color = Color.lerp_multistop(
                        self.__wipe_ul_to_lr_color_path, lerp_amount
                    )
                    # print(f"!!!!!!! lerp_amount:{lerp_amount} color:{color}")
                    self.machine.lights[light_name].color(color)
            # else:
            #     self.machine.lights[light_name].off()

        # is_left_of =
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
