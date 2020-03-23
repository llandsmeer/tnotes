import curses
import curses.textpad

from terminal import Terminal

class BlockTerminal:
    def __init__(self, header, argv, width, height):
        self.header = header
        self.terminal = Terminal(width, height, argv)
        self.focus = False
        self.scr = curses.newpad(1, self.width())
        self._width = width
        self._height = height

    def render(self):
        if self.height() > self.scr.getmaxyx()[0] - 1:
            self.scr = curses.newpad(self.height()+1, self.width())
        self.scr.clear()
        self.scr.addstr(0, 1, f'{self.header}', curses.A_BOLD)
        for y in range(self.terminal.screen.height):
            for x in range(self.terminal.screen.width):
                c = self.terminal.screen.chars[y][x]
                try:
                    self.scr.addstr(y+2, x+1, c)
                except:
                    pass
        if self.focus:
            curses.textpad.rectangle(self.scr,
                    1, 0,
                    self.height() - 1,
                    min(curses.COLS-1, self.width()-1))

    def handle_input(self, key):
        self.terminal.send(key)

    def width(self):
        return curses.COLS

    def height(self):
        return self._height + 3