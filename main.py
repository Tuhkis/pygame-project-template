import pygame as pg
pg.init()

# import moderngl as mgl

import sys
sys.path.append('./engine')
import engine.app as app
# import engine.shader as shader
import engine.particle as particle

class Game (app.App):
    def __init__(self):
        pg.display.set_caption('Game Window')
        app.App.__init__(self, (1024, 600))
        self.x = 0

        self.particles = particle.ParticleSystem()

    def render(self):
        pg.draw.rect(self.display, (255, 255, 255), (self.x, 32, 63, 100))

    def after_render(self):
        self.particles.render()

    def tick(self, dt):
        self.x += 64 * dt
        self.particles.tick(dt)

if __name__ == '__main__':
    a = Game()
    a.run()
    sys.exit()

