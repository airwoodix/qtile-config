from libqtile.layout.xmonad import MonadTall as BaseMonadTall
from libqtile.layout.base import Layout
import math


class MonadTall(BaseMonadTall):
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
