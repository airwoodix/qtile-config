from libqtile.layout.xmonad import MonadTall as BaseMonadTall
from libqtile.layout.verticaltile import VerticalTile as BaseVerticalTile
import math


def warp_pointer(window):
    window.window.warp_pointer(window.width / 2, window.height / 2)


class MonadTall(BaseMonadTall):
    _min_ratio = 0.2

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
            super(MonadTall, self).cmd_shrink()
            return

        if self.focused == 0:
            super(MonadTall, self).cmd_shrink()
        else:
            super(MonadTall, self).cmd_grow()

        warp_pointer(self.clients[self._focus])

    def cmd_grow(self):
        if len(self.clients) > 2:
            super(MonadTall, self).cmd_grow()
            return

        if self.focused == 0:
            super(MonadTall, self).cmd_grow()
        else:
            super(MonadTall, self).cmd_shrink()

        warp_pointer(self.clients[self._focus])

    def cmd_maximize(self):
        super(MonadTall, self).cmd_maximize()
        warp_pointer(self.clients[self._focus])

    def cmd_normalize(self, redraw=True):
        super(MonadTall, self).cmd_normalize(redraw=redraw)
        warp_pointer(self.clients[self._focus])

    def cmd_next(self):
        super(MonadTall, self).cmd_next()
        warp_pointer(self.clients[self._focus])

    def cmd_previous(self):
        super(MonadTall, self).cmd_previous()
        warp_pointer(self.clients[self._focus])

    def cmd_left(self):
        super(MonadTall, self).cmd_left()
        warp_pointer(self.clients[self._focus])

    def cmd_down(self):
        super(MonadTall, self).cmd_down()
        warp_pointer(self.clients[self._focus])

    def cmd_up(self):
        super(MonadTall, self).cmd_up()
        warp_pointer(self.clients[self._focus])

    def cmd_right(self):
        super(MonadTall, self).cmd_right()
        warp_pointer(self.clients[self._focus])

    def cmd_shuffle_up(self):
        super(MonadTall, self).cmd_shuffle_up()
        warp_pointer(self.clients[self._focus])

    def cmd_shuffle_down(self):
        super(MonadTall, self).cmd_shuffle_down()
        warp_pointer(self.clients[self._focus])

    def cmd_swap_main(self):
        super(MonadTall, self).cmd_swap_main()
        warp_pointer(self.clients[self._focus])


class VerticalTile(BaseVerticalTile):
    def cmd_next(self):
        super(VerticalTile, self).cmd_next()
        warp_pointer(self.focused)

    def cmd_previous(self):
        super(VerticalTile, self).cmd_previous()
        warp_pointer(self.focused)

    def cmd_down(self):
        super(VerticalTile, self).cmd_down()
        warp_pointer(self.focused)

    def cmd_up(self):
        super(VerticalTile, self).cmd_up()
        warp_pointer(self.focused)

    def cmd_maximize(self):
        super(VerticalTile, self).cmd_maximize()
        warp_pointer(self.focused)

    def cmd_normalize(self):
        super(VerticalTile, self).cmd_normalize()
        warp_pointer(self.focused)

    def cmd_grow(self):
        super(VerticalTile, self).cmd_grow()
        warp_pointer(self.focused)

    def cmd_shrink(self):
        super(VerticalTile, self).cmd_shrink()
        warp_pointer(self.focused)

    def cmd_shuffle_up(self):
        super(VerticalTile, self).cmd_shuffle_up()
        warp_pointer(self.focused)

    def cmd_shuffle_down(self):
        super(VerticalTile, self).cmd_shuffle_down()
        warp_pointer(self.focused)
