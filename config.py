# -*- coding: utf-8 -*-

from libqtile import bar, hook, layout, widget
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen
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
    Key([modkey], 'j', lazy.layout.down()),
    Key([modkey], 'k', lazy.layout.up()),

    # Move/Alter Window
    Key([modkey, 'shift'], 'j', lazy.layout.shuffle_down()),
    Key([modkey, 'shift'], 'k', lazy.layout.shuffle_up()),
    Key([modkey], 'l', lazy.layout.grow()),
    Key([modkey], 'h', lazy.layout.shrink()),
    Key([modkey], 'i', lazy.layout.maximize()),
    Key([modkey], 'm', lazy.layout.flip()),
    Key([modkey], 'n', lazy.layout.normalize()),
    Key([modkey], '0', lazy.layout.swap_left()),

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
                widget.WindowName(padding=0),
                widget.TextBox('Cpu:'),
                widget.CPUGraph(
                    border_width=1,
                    line_width=1
                ),
                widget.TextBox('Mem:'),
                widget.MemoryGraph(
                    border_width=1,
                    line_width=1
                ),

                widget.TextBox('Net:'),
                widget.NetGraph(
                    border_width=1,
                    line_width=1
                ),
                widget.TextBox('Bat:'),
                widget.Battery(
                    energy_now_file='charge_now',
                    energy_full_file='charge_full',
                    power_now_file='current_now',
                    charge_char='↑',
                    discharge_char='↓'
                ),
                widget.Systray(icon_size=14),
                widget.Spacer(width=5),
            ],
            size=20,
            background='#000000',
            font='Ubuntu',
            padding=0,
        ),
        bottom=bar.Bar(
            widgets=[
                widget.GroupBox(
                    rouded=False,
                    highlight_method='block',
                    padding=0,
                    margin=2
                ),
                widget.TextBox(':'),
                widget.CurrentLayout(),
                widget.Prompt(foreground='#ff0000'),
                widget.Spacer(width=bar.STRETCH),
                widget.Clock(
                    format='%a %d. %b kw%U %H:%M:%S',
                    padding=0,
                ),
            ],
            size=20,
            background='#000000',
            font='Ubuntu',
            padding=0,
        ),
    ),
]

widget_defaults = dict(
    font='Ubuntu',
    fontsize=14
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


def main(qtile):
    pass
