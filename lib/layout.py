from libqtile.layout.xmonad import MonadTall
from libqtile.layout.base import Layout
import math


class myMonadTall(MonadTall):
    def _maximize_secondary(self):
        n = len(self.clients) - 2
        collapsed_height = self._min_height * n
        nidx = self.focused - 1
        maxed_size = self.group.screen.dheight - collapsed_height

        if abs(
            self._get_absolute_size_from_relative(self.relative_sizes[nidx]) -
            maxed_size
        ) < self.change_size:
            if self.ratio > self._min_ratio:
                self.ratio = self._min_ratio
                self.group.layoutAll()
            else:
                self._shrink_secondary(
                    self._get_absolute_size_from_relative(
                        self.relative_sizes[nidx]
                    ) - self._min_height
                )
        else:
            self.ratio = self._min_ratio
            self._grow_secondary(maxed_size)

    def cmd_shrink(self):
        if len(self.clients) > 2:
            super(myMonadTall, self).cmd_shrink()
            return

        if self.focused == 0:
            super(myMonadTall, self).cmd_shrink()
        else:
            super(myMonadTall, self).cmd_grow()

    def cmd_grow(self):
        if len(self.clients) > 2:
            super(myMonadTall, self).cmd_grow()
            return

        if self.focused == 0:
            super(myMonadTall, self).cmd_grow()
        else:
            super(myMonadTall, self).cmd_shrink()


class VerticalTile(Layout):
    defaults = [
        ('border_focus', '#FF0000', 'Border color for the focused window.'),
        ('border_normal', '#FFFFFF', 'Border color for un-focused winows.'),
        ('border_width', 1, 'Border width.'),
        ('name', 'VerticalTile', 'Name of this layout.'),
        ('margin', 0, 'Margin of the layout'),
    ]

    windows = []
    focused = None
    maximized = None
    ratio = 0.75
    steps = 0.05

    def __init__(self, **config):
        Layout.__init__(self, **config)
        self.add_defaults(self.defaults)

    def add(self, window):
        if self.windows and self.focused:
            index = self.windows.index(self.focused)
            self.windows.insert(index + 1, window)
        else:
            self.windows.append(window)

        self.focus(window)

    def remove(self, window):
        if window not in self.windows:
            return

        index = self.windows.index(window)
        self.windows.remove(window)

        if not self.windows:
            self.focused = None
            self.maximized = None
            return

        if self.maximized is window:
            self.maximized = None

        if index == len(self.windows):
            index -= 1

        self.focus(self.windows[index])
        return self.focused

    def clone(self, group):
        c = Layout.clone(self, group)
        c.windows = []
        c.focused = None
        return c

    def configure(self, window, screen):
        if self.windows and window in self.windows:
            n = len(self.windows)
            index = self.windows.index(window)

            # border
            if n > 1:
                border_width = self.border_width
            else:
                border_width = 0

            if window is self.focused:
                border_color = self.group.qtile.colorPixel(self.border_focus)
            else:
                border_color = self.group.qtile.colorPixel(self.border_normal)

            # width
            if n > 1:
                width = screen.width - self.border_width * 2
            else:
                width = screen.width

            # height
            if n > 1:
                main_area_height = int(screen.height * self.ratio)
                sec_area_height = screen.height - main_area_height

                main_pane_height = main_area_height - border_width * 2
                sec_pane_height = sec_area_height / (n - 1) - border_width * 2
                normal_pane_height = (screen.height / n) - (border_width * 2)

                if self.maximized:
                    if window is self.maximized:
                        height = main_pane_height
                    else:
                        height = sec_pane_height
                else:
                    height = normal_pane_height
            else:
                height = screen.height

            # y
            if n > 1:
                if self.maximized:
                    y = screen.y + (index * sec_pane_height) +\
                        (border_width * 2 * index)
                else:
                    y = screen.y + (index * normal_pane_height) +\
                        (border_width * 2 * index)

                if self.maximized and window is not self.maximized:
                    if index > self.windows.index(self.maximized):
                        y = y - sec_pane_height + main_pane_height
            else:
                y = screen.y

            window.place(screen.x, y, width, height, border_width,
                         border_color)
            window.unhide()
        else:
            window.hide()

    def blur(self):
        self.focused = None

    def focus(self, window):
        self.focused = window

    def focus_first(self):
        try:
            self.focused = self.windows[0]
        except IndexError:
            self.focused = None

    def focus_last(self):
        try:
            self.focused = self.windows[:-1]
        except IndexError:
            self.focused = None

    def focus_next(self):
        try:
            index = self.windows.index(self.focused)
            self.focused = self.windows[index + 1]
        except IndexError:
            self.focus_first()

    def focus_previous(self):
        try:
            index = self.windows.index(self.focused)
            self.focused = self.windows[index - 1]
        except IndexError:
            self.focus_last()

    def grow(self):
        if self.ratio + self.steps < 1:
            self.ratio += self.steps
            self.group.layoutAll()

    def shrink(self):
        if self.ratio - self.steps > 0:
            self.ratio -= self.steps
            self.group.layoutAll()

    def cmd_next(self):
        self.focus_next()
        self.group.focus(self.focused, False)

    def cmd_previous(self):
        self.focus_previous()
        self.group.focus(self.focused, False)

    def cmd_down(self):
        self.focus_next()
        self.group.focus(self.focused, False)

    def cmd_up(self):
        self.focus_previous()
        self.group.focus(self.focused, False)

    def cmd_shuffle_up(self):
        index = self.windows.index(self.focused)

        try:
            self.windows[index], self.windows[index - 1] =\
                self.windows[index - 1], self.windows[index]
        except IndexError:
            self.windows[index], self.windows[:-1] =\
                self.windows[:-1], self.windows[index]

        self.group.layoutAll()

    def cmd_shuffle_down(self):
        index = self.windows.index(self.focused)

        try:
            self.windows[index], self.windows[index + 1] =\
                self.windows[index + 1], self.windows[index]
        except IndexError:
            self.windows[index], self.windows[0] =\
                self.windows[0], self.windows[index]

        self.group.layoutAll()

    def cmd_maximize(self):
        if self.windows:
            self.maximized = self.focused
            self.group.layoutAll()

    def cmd_normalize(self):
        self.maximized = None
        self.group.layoutAll()

    def cmd_grow(self):
        if not self.maximized:
            return

        if self.focused is self.maximized:
            self.grow()
        else:
            self.shrink()

    def cmd_shrink(self):
        if not self.maximized:
            return

        if self.focused is self.maximized:
            self.shrink()
        else:
            self.grow()
