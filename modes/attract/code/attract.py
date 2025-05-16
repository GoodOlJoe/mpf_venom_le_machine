from mpf.core.mode import Mode
from mpf.core.rgb_color import RGBColor

# https://missionpinball.org/latest/code/introduction/mode_code/
class Attract(Mode):

    def mode_init(self):
        self.__start_color = (255, 4, 217)
        self.__end_color = (81, 255, 0) # blue

    def mode_start(self, **kwargs):

        print("My custom mode code is starting")

        # what player are we?
        # print(self.player.number)

        # what's the player's score?
        # print('Score: {}'.format(self.player.score))

        self.add_mode_event_handler('timer_ndx1111_tick', self.ndx1111_tick_handler)
        self.add_mode_event_handler('timer_ndx1111_complete', self.ndx1111_complete_handler)

        # turn LED "led01" red
        # self.machine.leds.led01.color('red')        

    def lerp_color(self, color1, color2, amount):
        """
        Linearly interpolates between two RGB colors.

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
    
    # def rgb_to_hex(self,color):
    #     r, g, b = color
    #     return "{:02x}{:02x}{:02x}".format(r, g, b).upper()

    def ndx1111_tick_handler(self, **kwargs):
        # print("Inside tick handler")
        # n = str("x")
        # print("N is initialized to [" + n +"]")
        # n = self.machine.variables.get_machine_var("var_from_code")
        # if n is None:
        #     self.machine.variables.set_machine_var("var_from_code","Hello!")
        # else:
        # n = str(kwargs['ticks']) + " / " + str(kwargs['ticks_remaining'])
        interval = 1 / ( kwargs['ticks'] + kwargs['ticks_remaining'])
        current_color = self.lerp_color(self.__start_color, self.__end_color, interval * kwargs['ticks'])
        self.machine.variables.set_machine_var("lerped_color",RGBColor.rgb_to_hex(current_color))
        self.machine.lights['l_88_venomized_1'].color(RGBColor.rgb_to_hex(current_color))
        # self.machine.lights['l_88_venomized_1'].color('green')
        self.machine.lights['l_89_venomized_2'].color('purple')
        self.machine.lights['l_90_venomized_3'].color('purple')


    def ndx1111_complete_handler(self, **kwargs):
        self.machine.lights['l_88_venomized_1'].color(RGBColor.rgb_to_hex(self.__end_color))
        self.machine.variables.set_machine_var("lerped_color",RGBColor.rgb_to_hex(self.__end_color))
