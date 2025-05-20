import os
import pathlib

from mpf.core.mode import Mode
from ruamel import yaml

from ...util.plane import Plane
from ...util.color import Color
from ...util.playfield_layout import PlayfieldLayout

from .attract_handler_extra_bosses_light_show import ExtraBossesLightShowHandler
from .attract_handler_wipe_ul_to_lr_light_show import ULtoLRLightShowHandler
from .attract_handler_wipe_r_to_l_light_show import RtoLLightShowHandler

# https://missionpinball.org/latest/code/introduction/mode_code/
# https://colordesigner.io/gradient-generator
class Attract(Mode):

    def mode_init(self):

        self.__machine_path = pathlib.Path().resolve()
        # we need a list of all lights so we can do geometry-based wipe effects in light shows
        self.__playfield_layout = PlayfieldLayout(self.__machine_path)

        self.extra_bosses_light_show_handler = ExtraBossesLightShowHandler(self.machine)
        self.wipe_ul_to_lr_light_show_handler = ULtoLRLightShowHandler(self.machine,self.__playfield_layout)
        self.wipe_r_to_l_light_show_handler = RtoLLightShowHandler(self.machine,self.__playfield_layout)

    def mode_start(self, **kwargs):

        # region extra bosses light show
        self.add_mode_event_handler(
            "attract_extra_bosses_light_show_settings",
            self.extra_bosses_light_show_handler.extra_bosses_settings_handler,
        )
        self.add_mode_event_handler(
            "attract_extra_bosses_light_show_auto_step", 
            self.extra_bosses_light_show_handler.extra_bosses_step_handler
        )
        self.add_mode_event_handler(
            "attract_extra_bosses_light_show_looped", 
            self.extra_bosses_light_show_handler.extra_bosses_loop_handler
        )
        self.add_mode_event_handler(
            "attract_extra_bosses_light_show_stopped", 
            self.extra_bosses_light_show_handler.extra_bosses_stop_handler
        )
        # endregion
        # region Wipe UL to LR light show
        self.add_mode_event_handler(
            "attract_wipe_ul_to_lr_light_show_auto_step",
            self.wipe_ul_to_lr_light_show_handler.wipe_ul_to_lr_step_handler,
        )
        self.add_mode_event_handler(
            "attract_wipe_ul_to_lr_light_show_looped", 
            self.wipe_ul_to_lr_light_show_handler.wipe_ul_to_lr_loop_handler
        )
        self.add_mode_event_handler(
            "attract_wipe_ul_to_lr_light_show_stopped", 
            self.wipe_ul_to_lr_light_show_handler.wipe_ul_to_lr_stop_handler
        )
        # endregion
        # region Wipe R to L light show
        self.add_mode_event_handler(
            "attract_wipe_r_to_l_light_show_auto_step",
            self.wipe_r_to_l_light_show_handler.wipe_r_to_l_step_handler,
        )
        self.add_mode_event_handler(
            "attract_wipe_r_to_l_light_show_looped", 
            self.wipe_r_to_l_light_show_handler.wipe_r_to_l_loop_handler
        )
        self.add_mode_event_handler(
            "attract_wipe_r_to_l_light_show_stopped",
            self.wipe_r_to_l_light_show_handler.wipe_r_to_l_stop_handler
        )
        # endregion

