# Master list of MPF config sections 
Best I can tell as of May 20, 2025 using MPF .80

## Active *_Player configs
There are others that are deprecated, not listed here

* Player configs have properties that are EVENT NAMES
* The event names are followed by property names that have to be of a specific type that depends on the player type

|section|object type under Event|
|-|-|
|blinkenlight_player|blinkenlight|
|coil_player|coil|
|display_light_player|display|
|event_player|list of events to fire|
|flasher_player|light|
|light_player|light|
|queue_event_player|list of events to fire (and what queue to fire them to)|
|queue_relay_player	|
|random_event|player	list of events to select from and play one|
|segment_display_player|segment display and what to display|
|show_player|show to play and some specs for playing it|
|variable_player|variables and then what to set them to|

### (Deprecated *_Player configs)
|section|object type under Event|
|-|-|
|gi_player|use light_player instead|
|hardware_sound_player|not used with .80 / Godot|
|led_player|use light_player instead|
|playlist_player|not used with .80 / Godot|
|slide_player|not used with .80 / Godot|
|sound_Loop|player	not used with .80 / Godot|
|sound_player|not used with .80 / Godot|
|track_player|not used with .80 / Godot|
|widget_player|not used with .80 / Godot|


## uncategorized
auditor:
bcp_connection:
bcp_server:
bcp:
color_correction_profile:
config:
custom_code:
fadecandy:
fast:
game:
hardware:
high_score:
keyboard:
kivy_config:
lisy:
logging:
machine:
mc_custom_code:
mode:
mpf-mc:
mpf:
open_pixel_control:
opp:
osc:
p_roc:
pin2dmd:
pkone:
pololu_maestro:
pololu_tic:
raspberry_pi:
rpi_dmd:
smart_virtual:
smartmatrix:
snux:
sound_ducking:
sound_marker:
sound_system:
spi_bit_bang:
spike_node:
spike:
system11:
text_ui:
tilt:
trinamics_steprocker:
twitch_client:
virtual_segment_display_connector:
window:

|accruals||

## Component Groups
* have pre-definined names indicating what type of components they are defining, e.g., "flippers", "coils"
* the properties of the group are always NAMES of individual components of that group's implied type.

### Probably not used when using Godot, dig deeper to confirm
|Section Name|Implied component|
|-|-|
|assets||
|bitmap_fonts|||

|Section Name|Implied component|Component description|
|-|-|-|
|accelerometers|accelerometer||
|achievement_groups|achievement_group||
|achievements|achievement||
|animations|animation||
|autofire_coils|autofire_coil (consisting of a coil and a switch).| By including a coil in autofire_coils you tell the controller to fire the coil automatically on switch activation|
|ball_devices|ball_device|Any physical thing able to hold/capture a ball and then release it (either automatically or based on some action by the player). Usually contains one or more switches to count how many balls the device has and coils to eject a ball|
|ball_holds|ball_hold|A device used to temporarily hold a ball that has entered a Ball Devices while something else happens. (but not used for ball locks)|
|ball_locks|deprecated|replaced with ball_holds and multiball_locks|
|ball_routings|ball routing|not clear, docs mostly unwritten|
|ball_saves|ball_save|Used to automatically re-serve a ball that has drained. (Essentially this means the ball drain doesn't count.)|
|blinkenlights|blinkenlight|A light that flashes, but flashes colors in a cycle from a list of colors that change on the fly. It's a shared flashing light that might represent, for instance, a target being lit for multiple rewards simultaneously|
|coil_overwrites|coil_overwrite|A group of settings that can be applied to a coil to override its normal settings, presumably temporarily during a mode or something similar|
|coils|coil|A solenoid in the machine. Primarily serves to map a coil name to a driver board output, but also sets defaults for power, pulse times, etc.|
|combo_switches|combo_switch|Special combinations of switches that post events when they're hit together. Many uses including creating extra navigation control for menus, etc.|
|counter_control_events|||
|counters|||
|credits|||
|digital_outputs|||
|displays|||
|diverters|||
|dmds|||
|drop_target_banks|||
|drop_targets|||
|dual_wound_coils|||
|extra_ball_groups|||
|extra_balls|||
|fast_coils|||
|fast_switches|||
|flashers|||
|flippers|||
|gis|||
|hardware_sound_systems|||
|image_pools|||
|images|||
|info_lights|||
|kickbacks|||
|leds|||
|light_rings|||
|light_segment_displays|||
|light_settings|||
|light_stripes|||
|lights|||
|logic_blocks|||
|machine_vars|||
|magnets|||
|matrix_lights|||
|mc_scriptlets|||
|mode_settings (bonus)|||
|modes|||
|motors|||
|multiball_locks|||
|multiballs|||
|mypinballs|||
|named_colors|||
|opp_coils|||
|pd_led_boards|||
|player_vars|||
|playfield_transfers|||
|playfields|||
|playlists|||
|plugins|||
|psus|||
|rgb_dmds|||
|score_queues|||
|score_reel_groups|||
|score_reels|||
|scriptlets|||
|segment_displays|||
|sequence_shots|||
|sequences|||
|servo_controllers|||
|servos|||
|settings|||
|shot_control_events|||
|shot_groups|||
|shot_profiles|||
|shots|||
|show_pools|||
|shows|||
|slides|||
|sound_loop_sets|||
|sound_pools|||
|sound_system_tracks|||
|sounds|||
|speedometers|||
|spinners|||
|state_machines|||
|step_stick_stepper_settings|||
|steppers|stepper|A specialized device that accurately moves to multiple precise positions|
|switch_overwrites|||
|switches|||
|text_strings|||
|tic_stepper_settings|||
|timed_switches|||
|timers|||
|video_pools|||
|videos|||
|virtual_platform_start_active_switches|||
|widget_styles|||
|widgets|||

## Variables
* these are specifically-named groups containing well-known (and sometimes custom) properties that are treated as variable names and whose value is a set of properties describing initial value, data type, and so on

|Variable group name|Custom Properties allowed?|
|-|-|
|machine_vars|yes|
|player_vars|yes|
|game_vars|no|