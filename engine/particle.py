import moderngl as mgl
import pygame as pg

import shader

class ParticleSystem:
    def __init__(self):
        self.surf = pg.Surface((32, 32), pg.SRCALPHA)
        self.surf.fill(pg.Color(0, 0, 0, 0))
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
        self.s.program['colour'] = (1.0, 0.5, 0.0)

        self.particles = []
        for i in range(1000):
            self.add_particle(i * 34, 200)

    def add_particle(self, x, y):
        self.particles.append([x, y, 32, -64])

    def tick(self, dt):
        for p in self.particles:
            p[0] += p[2] * dt
            p[1] += p[3] * dt
            p[3] += 128 * dt

    def render(self):
        for p in self.particles:
            self.s.program['particlePos'] = (p[0], p[1])
            self.s.renderer.render(mode=mgl.TRIANGLE_STRIP)

