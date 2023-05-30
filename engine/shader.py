import moderngl as mgl
import pygame as pg
import array

# Loosely from https://www.youtube.com/watch?v=LFbePt8i0DI

def surf2tex(surf, s):
    tex = s.ctx.texture(surf.get_size(), 4)
    tex.filter = (mgl.NEAREST, mgl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex

class Shader:
    def __init__(self, vs='res/shader/vert.glsl', fs='res/shader/frag.glsl',
            quad=[-1.0, 1.0,  0.0, 0.0, 1.0, 1.0,  1.0, 0.0, -1.0,-1.0,  0.0, 1.0, 1.0,-1.0,  1.0, 1.0]):

        self.ctx = mgl.create_context()
        self.quad_buffer = self.ctx.buffer(data=array.array('f', quad))

        vsf = open(vs, 'r')
        vertex_shader = vsf.read()
        vsf.close()

        fsf = open(fs, 'r')
        fragment_shader = fsf.read()
        fsf.close()

        self.program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.renderer = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texCoord')])

