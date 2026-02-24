from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .app import App

import pygame
import moderngl 
import numpy as np

PASSTHROUGH_VERT = """
#version 330
in vec2 in_pos;
in vec2 in_uv;
out vec2 uv;
void main() {
    uv = in_uv;
    gl_Position = vec4(in_pos, 0.0, 1.0);
}
"""

PASSTHROUGH_FRAG = """
#version 330
in vec2 uv;
out vec4 fragColor;
uniform sampler2D tex;
void main() {
    fragColor = texture(tex, uv);
}
"""

def make_quad(x1:int, y1:int, x2:int, y2:int) -> np.ndarray:
    """
    Create a quad as a numpy array.
    """
    return np.array([
        x1, y1,  0.0, 0.0,
        x2, y1,  1.0, 0.0,
        x1, y2,  0.0, 1.0,
        x2, y1,  1.0, 0.0,
        x2, y2,  1.0, 1.0,
        x1, y2,  0.0, 1.0,
    ], dtype='f4')

def pixels_to_ndc(ox:int, oy:int, sw:int, sh:int, W:int, H:int) -> tuple:
    """ 
    Convert rectangle cordinates to NDC.
    """
    x1 = (ox / W) * 2 - 1
    y1 = 1 - ((oy + sh) / H) * 2
    x2 = ((ox + sw) / W) * 2 - 1
    y2 = 1 - (oy / H) * 2
    return x1, y1, x2, y2

class ShaderPass:
    """ 
    Interface that handles modernGl textures, their loading and rendering, 
    for 2D puproses (no custom vertex shader).
    """
    def __init__(self, app:"App", frag_prog:str = None):
        self.app = app
        self.textures = {}   
        self.uniforms = {}   
        self.shader_prog = app.gl_ctx.program(
            vertex_shader=PASSTHROUGH_VERT,
            fragment_shader=frag_prog or PASSTHROUGH_FRAG
        )
        self._vbo = app.gl_ctx.buffer(make_quad(-1, -1, 1, 1).tobytes(), dynamic=True)
        self._vao = app.gl_ctx.vertex_array(self.shader_prog, [(self._vbo, '2f 2f', 'in_pos', 'in_uv')])
        self._viewport = None  

    def set_viewport(self, ox:int, oy:int, sw:int, sh:int) -> None:
        """ 
        Sets the shape of the display.
        """
        self._viewport = (ox, oy, sw, sh)

    def dump_pygame_surf(self, name:str, surf:pygame.Surface, slot:int, filter:int = moderngl.NEAREST) -> None:
        """ 
        Dump a pygame surface, so it can be rendered.
        """
        data = pygame.image.tobytes(surf, "RGBA", True)
        tex = self.app.gl_ctx.texture(surf.get_size(), 4)
        tex.filter = (filter, filter)
        tex.write(data)
        if slot in [s for _, s in self.textures.values()]:
            raise ValueError(f"Slot {slot} already occupied.")
        self.textures[name] = (tex, slot)


    def load_texture(self, name:str, path:str, slot:int, filter:int = moderngl.NEAREST) -> None:
        """
        Abstraction to dump a directly loaded pygame surf.
        """
        self.dump_pygame_surf(
            name, 
            pygame.image.load(path).convert_alpha(), 
            slot, 
            filter
        )

    def set_uniform(self, name:str, value:int) -> None:
        self.uniforms[name] = value

    def render(self) -> None:
        """ 
        Rendering hook.
        """
        self._update_quad()
        for name, (tex, slot) in self.textures.items():
            tex.use(slot)
            self.shader_prog[name] = slot
        for name, value in self.uniforms.items():
            if name in self.shader_prog:
                self.shader_prog[name] = value
        self._vao.render()

    def _update_quad(self) -> None:
        if self._viewport is None:
            x1, y1, x2, y2 = -1, -1, 1, 1
        else:
            W, H = self.app.window.screen.get_size()
            ox, oy, sw, sh = self._viewport
            x1, y1, x2, y2 = pixels_to_ndc(ox, oy, sw, sh, W, H)
        self._vbo.write(make_quad(x1, y1, x2, y2).tobytes())
