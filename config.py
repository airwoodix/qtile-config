# -*- coding: utf-8 -*-

from libqtile import bar, hook, layout, widget
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen
from lib.layout import MonadTall
from lib.default import style, layout_defaults, floating_layout_defaults,\
    bar_defaults, widget_defaults, widget_graph_defaults, widget_sep_defaults
from lib.utils import get_alternatives, execute
from Xlib import display
import os

wmname = 'qtile'
auto_fullscreen = True
bring_front_click = True
cursor_warp = True
follow_mouse_focus = False
dgroups_key_binder = None
dgroups_app_rules = []
floating_windows = ['feh ']

# key macros
ALT = 'mod1'
WIN = 'mod4'
TAB = 'Tab'
CTRL = 'control'
SHIFT = 'shift'
RETURN = 'Return'
SPACE = 'space'
MODKEY = ALT

last_window_id = None
x_display = display.Display()
x_screen = x_display.screen()


class command:
    terminal = get_alternatives(['terminator', 'gnome-terminal', 'xterm'])
    autostart = os.path.join(os.path.dirname(__file__), 'bin/autostart')
    lock = os.path.join(os.path.dirname(__file__), 'bin/lock')
    suspend = os.path.join(os.path.dirname(__file__), 'bin/suspend')
    hibernate = os.path.join(os.path.dirname(__file__), 'bin/hibernate')

# Key bindings
keys = [
    # Window manager controls
    Key([MODKEY, CTRL], 'r', lazy.restart()),
    Key([MODKEY, CTRL], 'q', lazy.shutdown()),
    Key([MODKEY, SHIFT], SPACE, lazy.layout.flip()),
    Key([MODKEY], RETURN, lazy.spawn(command.terminal)),
    Key([MODKEY], SPACE, lazy.nextlayout()),
    Key([MODKEY], 'q', lazy.window.kill()),
    Key([MODKEY], 'p', lazy.spawncmd()),
    Key([MODKEY], 't', lazy.window.toggle_floating()),
    Key([MODKEY], 'f', lazy.window.toggle_fullscreen()),

    # Move Focus
    Key([MODKEY], TAB, lazy.layout.next()),
    Key([MODKEY, SHIFT], TAB, lazy.layout.previous()),
    Key([MODKEY], 'h', lazy.layout.left()),
    Key([MODKEY], 'j', lazy.layout.down()),
    Key([MODKEY], 'k', lazy.layout.up()),
    Key([MODKEY], 'l', lazy.layout.right()),
    Key([MODKEY], 'w', lazy.prev_screen()),
    Key([MODKEY], 'e', lazy.next_screen()),
    Key([WIN], '1', lazy.to_screen(0)),
    Key([WIN], '2', lazy.to_screen(1)),
    Key([WIN], '3', lazy.to_screen(2)),

    # Move Window
    Key([MODKEY, SHIFT], 'j', lazy.layout.shuffle_down()),
    Key([MODKEY, SHIFT], 'k', lazy.layout.shuffle_up()),
    Key([MODKEY], 'i', lazy.layout.swap_main()),

    # Alter Window Size
    Key([MODKEY, SHIFT], 'h', lazy.layout.shrink()),
    Key([MODKEY, SHIFT], 'l', lazy.layout.grow()),
    Key([MODKEY, SHIFT], 'n', lazy.layout.reset()),
    Key([MODKEY], 'm', lazy.layout.maximize()),
    Key([MODKEY], 'n', lazy.layout.normalize()),

    # Lock and Powermangament
    Key([MODKEY, CTRL], 'l', lazy.spawn(command.lock)),
    Key([MODKEY, CTRL], 'p', lazy.spawn(command.suspend)),
    Key([MODKEY, CTRL], 'h', lazy.spawn(command.hibernate)),
]

# Mouse bindings and options
mouse = (
    Drag([MODKEY], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([MODKEY], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
)

# Groups
groups = [
    Group('1'),
    Group('2'),
    Group('3'),
    Group('4'),
    Group('5'),
    Group('6'),
    Group('7'),
    Group('8'),
    Group('9'),
    Group('0'),
]

for i in groups:
    keys.append(Key([MODKEY], i.name, lazy.group[i.name].toscreen()))
    keys.append(Key([MODKEY, SHIFT], i.name, lazy.window.togroup(i.name)))

# Layouts
layouts = [
    MonadTall(name='Tall', **layout_defaults),
    layout.VerticalTile(name='VerticalTile', **layout_defaults),
    layout.Max(name='Full'),
]

floating_layout = layout.Floating(**floating_layout_defaults)

# Screens and widget options
screens = [
    Screen(
        top=bar.Bar(
            widgets=[
                widget.WindowName(padding=6),
                widget.TextBox('Cpu:'),
                widget.CPUGraph(**widget_graph_defaults),

                widget.TextBox('Mem:'),
                widget.MemoryGraph(**widget_graph_defaults),

                widget.TextBox('Net:'),
                widget.NetGraph(**widget_graph_defaults),

                widget.TextBox('Bat:'),
                widget.Battery(
                    energy_now_file='charge_now',
                    energy_full_file='charge_full',
                    power_now_file='current_now',
                    charge_char='↑',
                    discharge_char='↓',
                    foreground=style.color.bright_blue
                ),
                widget.TextBox('Vol:'),
                widget.Volume(foreground=style.color.bright_blue),
                widget.Systray(icon_size=style.icon_size),
                widget.Spacer(width=6),
            ],
            **bar_defaults
        ),
        bottom=bar.Bar(
            widgets=[
                widget.GroupBox(rouded=True, borderwidth=2, padding=2),
                widget.Sep(**widget_sep_defaults),
                widget.CurrentLayout(padding=2),
                widget.Prompt(foreground=style.color.red, prompt=':'),
                widget.Spacer(width=bar.STRETCH),
                widget.Clock(format=style.clock_format, padding=6),
            ],
            **bar_defaults
        ),
    ),
]


@hook.subscribe.startup
def startup():
    execute(command.autostart)


@hook.subscribe.client_new
def floating_dialogs(window):
    global floating_windows
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    window_name = window.name.lower()

    if dialog or transient:
        window.floating = True

    for i in floating_windows:
        if i in window_name:
            window.floating = True


def main(qtile):
    pass
