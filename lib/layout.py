from libqtile.layout.xmonad import MonadTall
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


class VerticalTall(MonadTall):
    def cmd_normalize(self, redraw=True):
        "Evenly distribute screen-space among secondary clients"
        n = len(self.clients)  # exclude main client, 0

        # if secondary clients exist
        if n > 0 and self.group.screen is not None:
            self.relative_sizes = [1.0 / n] * n

        # reset main pane ratio
        if redraw:
            self.group.layoutAll()
        self.do_normalize = False

    def cmd_maximize(self):
        self._maximize_secondary()
        self.group.layoutAll()

    def cmd_grow(self):
        self._grow_secondary(self.change_size)
        self.group.layoutAll()

    def cmd_shrink(self):
        if len(self.clients) == 2:
            self._shrink_solo_secondary(self.change_ratio)
        else:
            self._shrink_secondary(self.change_size)

    def configure(self, client, screen):
        "Position client based on order and sizes"

        # if no sizes or normalize flag is set, normalize
        if not self.relative_sizes or self.do_normalize:
            self.cmd_normalize(False)

        # if client not in this layout
        if not self.clients or client not in self.clients:
            client.hide()
            return

        # single client - fullscreen
        if len(self.clients) == 1:
            px = self.group.qtile.colorPixel(self.border_focus)
            client.place(
                self.group.screen.dx,
                self.group.screen.dy,
                self.group.screen.dwidth,
                self.group.screen.dheight,
                0,
                px,
                margin=self.margin,
            )
            client.unhide()
            return

        cidx = self.clients.index(client)

        # determine focus border-color
        if cidx == self.focused:
            px = self.group.qtile.colorPixel(self.border_focus)
        else:
            px = self.group.qtile.colorPixel(self.border_normal)

        width = self.group.screen.dwidth
        xpos = self.group.screen.dx

        # calculate client height and place
        # secondary client
        # ypos is the sum of all clients above it
        ypos = self.group.screen.dy + \
            self._get_absolute_size_from_relative(
                sum(self.relative_sizes[:cidx - 1])
            )
        # get height from precalculated height list
        height = self._get_absolute_size_from_relative(
            self.relative_sizes[cidx - 1]
        )
        # place client based on calculated dimensions
        client.place(
            xpos,
            ypos,
            width - 2 * self.border_width,
            height - 2 * self.border_width,
            self.border_width,
            px,
            margin=self.margin,
        )
        client.unhide()
