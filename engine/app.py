import pygame as pg
import _thread as thread
import sys

class App:
    def __init__(self, window_dimensions):
        self.win = pg.display.set_mode(window_dimensions)
        self.clock = pg.time.Clock()
        self.fps = 60
        self.running = True

    def run(self):
        thread.start_new_thread(self._tick, () )
        while self.running:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.running = False
                self.handle_event(e)

            self.render()
            self.win.fill((255, 50, 50))
            pg.display.flip()
        sys.exit()

    def _tick(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            self.tick(dt)
        sys.exit()

    # Overridables
    def tick(self, dt):
        pass

    def handle_event(self, e):
        pass

    def render(self):
        pass

    def load_res(self):
        pass

