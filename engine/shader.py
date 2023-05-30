import moderngl as mgl
import pygame as pg
import array

# Loosely from https://www.youtube.com/watch?v=LFbePt8i0DI

def surf2tex(surf):
    tex = Shader.ctx.texture(surf.get_size(), 4)
    tex.filter = (mgl.NEAREST, mgl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex

class Shader:
    ctx = None
    def __init__(self, vs='res/shader/vert.glsl', fs='res/shader/frag.glsl'):
        self.quad_buffer = Shader.ctx.buffer(data=array.array('f', [
            -1.0, 1.0,  0.0, 0.0,
             1.0, 1.0,  1.0, 0.0,
            -1.0,-1.0,  0.0, 1.0,
             1.0,-1.0,  1.0, 1.0
        ]))

        vsf = open(vs, 'r')
        vertex_shader = vsf.read()
        vsf.close()

        fsf = open(fs, 'r')
        fragment_shader = fsf.read()
        fsf.close()

        self.program = Shader.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.renderer = Shader.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texCoord')])

