import moderngl as mgl
import pygame as pg
import array

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

        self.quad=[
            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, -1.0,
            0.0, 0.0, 1.0, -1.0,
        ]
        self.quad_buffer = self.s.ctx.buffer(data=array.array('f', self.quad))
        self.s.renderer = self.s.ctx.vertex_array(self.s.program, [(self.quad_buffer, '2f 2f', 'vert', 'texCoord')])
        for x in range(1):
            for y in range(100):
                self.add_particle(x*32, y*32)

    def add_particle(self, x, y):
        for i in [
            x, y, 0.0, 0.0,
            x + 32.0, y, 1.0, 0.0,
            x, y + 32.0, 0.0, -1.0,
            x + 32.0, y + 32.0, 1.0, -1.0,
            ]:
            self.quad.append(i)
        self.quad_buffer = self.s.ctx.buffer(data=array.array('f', self.quad))
        self.s.renderer = self.s.ctx.vertex_array(self.s.program, [(self.quad_buffer, '2f 2f', 'vert', 'texCoord')])

    def tick(self, dt):
        pass

    def render(self):
        for i in range(int(len(self.quad) / 4)):
            self.s.renderer.render(mode=mgl.TRIANGLE_STRIP, first=i*4, vertices=4)

