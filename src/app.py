import pygame 
import moderngl 
import time 
import sys

from .scene import Scene

class App:
    """ 
    Main App class 
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((256, 240), pygame.SCALED | pygame.OPENGL | pygame.DOUBLEBUF, vsync = False) 
        self.clock = pygame.time.Clock() 
        self.dt = 0
        self.timer = 0
        self._latest_time = time.perf_counter()
        self._build_gl_context()
        self.scene = Scene(self) 

    def _delta_time(self):
        self.dt = time.perf_counter() - self._latest_time 
        self._latest_time = time.perf_counter()

    def _build_gl_context(self):
        self.gl_ctx = moderngl.create_context()
        self.gl_ctx.enable(moderngl.BLEND)
        self.gl_ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA 

    def _system_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self._delta_time()
            self._system_events() 
            self.gl_ctx.clear(0, 0, 0)
            self.scene.update()
            self.scene.render()
            pygame.display.flip() 
            self.clock.tick(1000)
            self.timer += self.dt

    @property 
    def fps(self):
        return self.clock.get_fps()
    
    @property 
    def display_size(self):
        return self.screen.get_size()

