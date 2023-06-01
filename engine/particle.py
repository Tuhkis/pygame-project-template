import moderngl as mgl
import pygame as pg
import array

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
        self.s.program['colour'] = (1.0, 0.5, 1.0)
        self.c = 64

        self.particles = []

        self.quad_buffer = self.s.ctx.buffer(reserve=409600*10)
        self.s.renderer = self.s.ctx.vertex_array(self.s.program, [(self.quad_buffer, '2f 2f', 'vert', 'texCoord')])
        for x in range(50):
            for y in range(50):
                self.particles.append([x*32, y*32, 0])
                self.gpu_add_particle(float(x*32), float(y*32))

    def gpu_add_particle(self, x, y):
        self.quad_buffer.write(array.array('f', [
            x, y, 0.0, 0.0,
            32.0 + x, y, 1.0, 0.0,
            x, y + 32.0, 0.0, -1.0,
            x + 32.0, y + 32.0, 1.0, -1.0
        ]), offset=self.c)
        self.c += 64

    def tick(self, dt):
        for p in self.particles:
            p[0] += 16.0 * dt
            p[2] += dt
            if p[2] > 4:
                self.particles.remove(p)

    def render(self):
        self.c = 0
        for p in self.particles:
            self.gpu_add_particle(p[0], p[1])
        for i in range(int(self.c / 64)):
            self.s.renderer.render(mode=mgl.TRIANGLE_STRIP, first=i*4, vertices=4)

