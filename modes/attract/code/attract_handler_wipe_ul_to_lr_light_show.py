from ...util.plane import Plane
from ...util.color import Color


class ULtoLRLightShowHandler:

    def __init__(self, machine, playfield_layout):
        self.__machine = machine
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
        self.__wipe_ul_to_lr_color_path = ["red", "green", "blue"]
        self.__playfield_layout = playfield_layout

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

            if "playfield_wipe" in self.__machine.lights[light_name].tags:

                result = Plane.side(light_pos["x"], light_pos["y"], (sx, sy), (ex, ey))
                if -1 == result:
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
                    self.__machine.lights[light_name].color(color)
            # else:
            #     self.machine.lights[light_name].off()

    def wipe_ul_to_lr_loop_handler(self, **kwargs):
        self.__wipe_ul_to_lr_loop_count += 1

    def wipe_ul_to_lr_stop_handler(self, **kwargs):
        self.__wipe_ul_to_lr_loop_count = 0
