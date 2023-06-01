import pygame as pg
import _thread as thread
import sys
import moderngl as mgl

import shader

class App:
    def __init__(self, window_dimensions):
        self.win = pg.display.set_mode(window_dimensions, pg.OPENGL | pg.DOUBLEBUF)
        self.display = pg.Surface(window_dimensions)
        self.clock = pg.time.Clock()
        self.rclock = pg.time.Clock()
        self.fps = 60
        self.running = True

        self.shader = shader.Shader()

    def run(self):
        thread.start_new_thread(self._tick, () )
        while self.running:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    self.running = False
                self.handle_event(e)

            self.display.fill((255, 0, 0))
            self.render()

            # Moderngl stuff
            display_tex = shader.surf2tex(self.display, self.shader)
            display_tex.use(0)
            self.shader.program['tex'] = 0
            self.shader.renderer.render(mode=mgl.TRIANGLE_STRIP)
            self.after_render()

            # Switch buffers
            pg.display.flip()
            
            display_tex.release()

            self.rclock.tick(60)

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

    def after_render(self):
        pass

    def load_res(self):
        pass

