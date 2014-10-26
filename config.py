# -*- coding: utf-8 -*-

from libqtile import bar, hook, layout, widget
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen
from Xlib import display
import subprocess
import re
import os

wmname = 'qtile'
modkey = 'mod1'
auto_fullscreen = True
bring_front_click = True
cursor_warp = False
follow_mouse_focus = False
dgroups_key_binder = None
dgroups_app_rules = []

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
    Key([modkey, 'control'], 'r', lazy.restart()),
    Key([modkey, 'control'], 'q', lazy.shutdown()),
    Key([modkey], 'r', lazy.spawncmd()),
    Key([modkey], 'Return', lazy.spawn(command.terminal)),
    Key([modkey], 'q', lazy.window.kill()),
    Key([modkey], 'p', lazy.spawncmd()),
    Key([modkey], 't', lazy.window.toggle_floating()),
    Key([modkey], 'space', lazy.nextlayout()),

    # Move Focus
    Key([modkey], 'Tab', lazy.layout.next()),
    Key([modkey, 'shift'], 'Tab', lazy.layout.previous()),
    Key([modkey], 'h', lazy.layout.left()),
    Key([modkey], 'j', lazy.layout.down()),
    Key([modkey], 'k', lazy.layout.up()),
    Key([modkey], 'l', lazy.layout.right()),
    Key([modkey], 'w', lazy.prev_screen()),
    Key([modkey], 'e', lazy.next_screen()),
    Key(['mod4'], '1', lazy.to_screen(0)),
    Key(['mod4'], '2', lazy.to_screen(1)),
    Key(['mod4'], '3', lazy.to_screen(2)),

    # Move Window
    Key([modkey, 'shift'], 'j', lazy.layout.shuffle_down()),
    Key([modkey, 'shift'], 'k', lazy.layout.shuffle_up()),

    # Alter Window Size
    Key([modkey, 'shift'], 'h', lazy.layout.shrink()),
    Key([modkey, 'shift'], 'l', lazy.layout.grow()),
    Key([modkey], 'm', lazy.layout.maximize()),
    Key([modkey], 'n', lazy.layout.normalize()),
    Key([modkey, 'shift'], 'n', lazy.layout.reset()),

    # Swap/Flip Windows
    Key([modkey, 'shift'], 'space', lazy.layout.flip()),
    Key([modkey], 'i', lazy.layout.swap_main()),

    # Lock and Powermangament
    Key([modkey, 'control'], 'l', lazy.spawn(command.lock)),
    Key([modkey, 'control'], 'p', lazy.spawn(command.suspend)),
    Key([modkey, 'control'], 'h', lazy.spawn(command.hibernate)),
]

# Mouse bindings and options
mouse = (
    Drag([modkey], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([modkey], 'Button3', lazy.window.set_size_floating(),
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
    keys.append(Key([modkey], i.name, lazy.group[i.name].toscreen()))
    keys.append(Key([modkey, 'shift'], i.name, lazy.window.togroup(i.name)))

# Layouts
layouts = [
    layout.MonadTall(
        name='Tall',
        margin=0,
        border_width=1,
        border_normal='#111111',
        border_focus='#215578'
    ),
    layout.Max(name='Full'),
]

floating_layout = layout.Floating(
    margin=0,
    border_width=1,
    border_normal='#111111',
    border_focus='#215578'
)

# Screens and widget options
screens = [
    Screen(
        top=bar.Bar(
            widgets=[
                widget.WindowName(padding=6),
                widget.TextBox('Cpu:'),
                widget.CPUGraph(
                    margin_y=4,
                    border_width=1,
                    line_width=1
                ),
                widget.TextBox('Mem:'),
                widget.MemoryGraph(
                    margin_y=4,
                    border_width=1,
                    line_width=1
                ),

                widget.TextBox('Net:'),
                widget.NetGraph(
                    margin_y=4,
                    border_width=1,
                    line_width=1
                ),
                widget.TextBox('Bat:'),
                widget.Battery(
                    energy_now_file='charge_now',
                    energy_full_file='charge_full',
                    power_now_file='current_now',
                    charge_char='↑',
                    discharge_char='↓',
                    foreground='#18BAEB'
                ),
                widget.TextBox('Vol:'),
                widget.Volume(
                    cardid=1,
                    foreground='#18BAEB'
                ),
                widget.Systray(icon_size=14),
                widget.Spacer(width=6),
            ],
            size=24,
            background='#000000',
            font='Monospace',
            padding=0,
        ),
        bottom=bar.Bar(
            widgets=[
                widget.GroupBox(
                    rouded=True,
                    borderwidth=2,
                    padding=2,
                ),
                widget.Sep(
                    foreground='#215578',
                    linewidth=2,
                    height_percent=55,
                    padding=14
                ),
                widget.CurrentLayout(padding=2),
                widget.Prompt(foreground='#ff0000', prompt=':'),
                widget.Spacer(width=bar.STRETCH),
                widget.Clock(
                    format='%a %d. %b kw%V %H:%M:%S',
                    padding=6,
                ),
            ],
            size=24,
            background='#000000',
            font='Monospace',
            padding=0,
        ),
    ),
]

widget_defaults = dict(
    font='Monospace',
    fontsize=12
)


@hook.subscribe.startup
def startup():
    execute(command.autostart)


@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    window_name = window.name.lower()

    if dialog or transient:
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
