# -*- coding: utf-8 -*-

from libqtile import bar, hook, layout, widget
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen
from lib.layout import myMonadTall
from lib.default import style, layout_defaults, floating_layout_defaults,\
    bar_defaults, widget_defaults, widget_graph_defaults, widget_sep_defaults

from Xlib import display
import subprocess
import os

wmname = 'qtile'
auto_fullscreen = True
bring_front_click = True
cursor_warp = False
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

last_window_id = None
x_display = display.Display()
x_screen = x_display.screen()


def execute(command):
    return subprocess.Popen(command.split())


class command:
    terminal = 'terminator'
    autostart = os.path.join(os.path.dirname(__file__), 'bin/autostart')
    lock = os.path.join(os.path.dirname(__file__), 'bin/lock')
    suspend = os.path.join(os.path.dirname(__file__), 'bin/suspend')
    hibernate = os.path.join(os.path.dirname(__file__), 'bin/hibernate')

# Key bindings
keys = [
    # Window manager controls
    Key([ALT, CTRL], 'r', lazy.restart()),
    Key([ALT, CTRL], 'q', lazy.shutdown()),
    Key([ALT, SHIFT], SPACE, lazy.layout.flip()),
    Key([ALT], RETURN, lazy.spawn(command.terminal)),
    Key([ALT], SPACE, lazy.nextlayout()),
    Key([ALT], 'q', lazy.window.kill()),
    Key([ALT], 'p', lazy.spawncmd()),
    Key([ALT], 't', lazy.window.toggle_floating()),
    Key([ALT], 'f', lazy.window.toggle_fullscreen()),

    # Move Focus
    Key([ALT], TAB, lazy.layout.next()),
    Key([ALT, SHIFT], TAB, lazy.layout.previous()),
    Key([ALT], 'h', lazy.layout.left()),
    Key([ALT], 'j', lazy.layout.down()),
    Key([ALT], 'k', lazy.layout.up()),
    Key([ALT], 'l', lazy.layout.right()),
    Key([ALT], 'w', lazy.prev_screen()),
    Key([ALT], 'e', lazy.next_screen()),
    Key([WIN], '1', lazy.to_screen(0)),
    Key([WIN], '2', lazy.to_screen(1)),
    Key([WIN], '3', lazy.to_screen(2)),

    # Move Window
    Key([ALT, SHIFT], 'j', lazy.layout.shuffle_down()),
    Key([ALT, SHIFT], 'k', lazy.layout.shuffle_up()),
    Key([ALT], 'i', lazy.layout.swap_main()),

    # Alter Window Size
    Key([ALT, SHIFT], 'h', lazy.layout.shrink()),
    Key([ALT, SHIFT], 'l', lazy.layout.grow()),
    Key([ALT, SHIFT], 'n', lazy.layout.reset()),
    Key([ALT], 'm', lazy.layout.maximize()),
    Key([ALT], 'n', lazy.layout.normalize()),

    # Lock and Powermangament
    Key([ALT, CTRL], 'l', lazy.spawn(command.lock)),
    Key([ALT, CTRL], 'p', lazy.spawn(command.suspend)),
    Key([ALT, CTRL], 'h', lazy.spawn(command.hibernate)),
]

# Mouse bindings and options
mouse = (
    Drag([ALT], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([ALT], 'Button3', lazy.window.set_size_floating(),
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
    keys.append(Key([ALT], i.name, lazy.group[i.name].toscreen()))
    keys.append(Key([ALT, SHIFT], i.name, lazy.window.togroup(i.name)))

# Layouts
layouts = [
    myMonadTall(name='Tall', **layout_defaults),
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


@hook.subscribe.client_focus
def update_pointer(window):
    global last_window_id, x_screen, x_display
    window_id = window.info()['id']

    if window_id == last_window_id:
        return False

    last_window_id = window_id
    pos_x, pos_y = window.getposition()
    width, height = window.getsize()

    x_screen.root.warp_pointer(int(width / 2) + pos_x,
                               int(height / 2) + pos_y)
    x_display.sync()


def main(qtile):
    pass
