import pygame 
import moderngl 
import time 
import sys

from .scene import Scene
from .shader_pass import ShaderPass
from .window import Window

FRAMERATE_REFERENCE = 60

class App:
    """
    Handles the app lifecycle.
    """
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.screen_size = (info.current_w, info.current_h)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.timer = 0
        self._latest_time = time.perf_counter()
        self.window = Window(self)
        self._build_gl_context()
        self.scene = Scene(self)
        
    def _delta_time(self) -> None:
        """ 
        Compute the delta time.
        """
        self.dt = (time.perf_counter() - self._latest_time) * FRAMERATE_REFERENCE
        self._latest_time = time.perf_counter()

    def _build_gl_context(self) -> None:
        """
        Create the modernGl context.
        """
        self.gl_ctx = moderngl.create_context()
        self.gl_ctx.enable(moderngl.BLEND)
        self.gl_ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

        self._render_tex = self.gl_ctx.texture(self.window.internal_size, 4)
        self._render_tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self._render_fbo = self.gl_ctx.framebuffer(color_attachments=[self._render_tex])

        self._blit_pass = ShaderPass(self)
        self._blit_pass.textures["tex"] = (self._render_tex, 0)

    def _system_events(self) -> None:
        """
        Handle the system (A.K.A pygame) events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.window.toggle_fullscreen()

    def run(self) -> None:
        """
        Game loop.
        """
        while True:
            self._delta_time()
            self._system_events()

            self._render_fbo.use()
            self.gl_ctx.viewport = (0, 0, *self.window.internal_size)
            self.gl_ctx.clear(0, 0, 0)
            self.scene.update()
            self.scene.render()

            self.gl_ctx.screen.use()
            W, H = self.window.screen.get_size()
            self.gl_ctx.viewport = (0, 0, W, H)
            self.gl_ctx.clear(0, 0, 0)

            if self.window.fullscreen:
                self.gl_ctx.viewport = self.window.fullscreen_viewport()
        
            self._blit_pass.render()

            pygame.display.flip()
            self.clock.tick(1000)
            self.timer += self.dt

    @property
    def fps(self) -> float:
        return self.clock.get_fps()

    @property
    def display_size(self) -> tuple:
        return self.window.internal_size