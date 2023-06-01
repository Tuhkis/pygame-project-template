import moderngl as mgl
import pygame as pg
import array
import random

import shader

class ParticleSystem:
    def __init__(self):
        self.surf = pg.Surface((32, 32), pg.SRCALPHA)
        pg.draw.circle(self.surf, (255, 255, 255), (16, 16), 16)
        self.s = shader.Shader(quad=[
            0.0, 0.0, 0.0, 0.0,
            32.0, 0.0, 1.0, 0.0,
            0.0, 32.0, 0.0, -1.0,
            32.0, 32.0, 1.0, -1.0
        ], vs='res/shader/particle-vert.glsl', fs='res/shader/particle-frag.glsl')
        self.s.ctx.enable(mgl.BLEND)
        self.s.ctx.blend_func = mgl.SRC_ALPHA, mgl.ONE_MINUS_SRC_ALPHA
        tex = shader.surf2tex(self.surf, self.s)
        tex.use(1)
        self.s.program['tex'] = 1
        self.s.program['colour'] = (1.0, 0.5, 0.2)
        self.c = 64

        self.particles = []

        self.quad_buffer = self.s.ctx.buffer(reserve=4096000)
        self.s.renderer = self.s.ctx.vertex_array(self.s.program, [(self.quad_buffer, '2f 2f', 'vert', 'texCoord')])

    def gpu_add_particle(self, x, y, size):
        self.quad_buffer.write(array.array('f', [
            x, y, 0.0, 0.0,
            size + x, y, 1.0, 0.0,
            x, y + size, 0.0, -1.0,
            x + size, y + size, 1.0, -1.0
        ]), offset=self.c)
        self.c += 64

    def tick(self, dt):
        self.particles.append( [500.0, 300.0, 0, random.randrange(-64, 64), -100 - random.randrange(0, 64), random.randrange(8, 14)] )
        self.particles.append( [300.0, 450.0, 0, random.randrange(-64, 64), -100 - random.randrange(0, 64), random.randrange(30, 42)] )
        for p in self.particles:
            p[0] += p[3] * dt
            p[1] += p[4] * dt
            p[4] += 64 * dt
            p[2] += dt
            p[5] -= dt
            if p[2] > 10:
                self.particles.remove(p)

    def render(self):
        self.c = 0
        for p in self.particles:
            self.gpu_add_particle(p[0], p[1], p[5])
        for i in range(int(self.c / 64)):
            self.s.renderer.render(mode=mgl.TRIANGLE_STRIP, first=i*4, vertices=4)

