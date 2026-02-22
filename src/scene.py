import pygame 
import math 

from .shader_pass import ShaderPass
from .pygame_layer import PygameLayer

class Scene:
    """
    Render and Update hooks container, used to organization puposes.
    """
    def __init__(self, app):
        self.app = app 
        self._fonts = {}
        
        with open("assets/shader.glsl", "r", encoding = "utf-8") as f:
            self.ground = ShaderPass(app, f.read()) 
        self.ground.load_texture("tex", "assets/ground.png", 0)
        self.ground.load_texture("tex_infinite", "assets/ground-infinite.png", 1)
        with open("assets/outline.glsl", "r", encoding = "utf-8") as f:
            self.hud = PygameLayer(app, f.read()) 
        self.player_x = 0
        self.player_y = 0
        self.player_z = 0
        self.player_angle = 0
        self.horizon = 0
    
    def update(self):
        dx, dy = 0, 0
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.horizon -= 0.01
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.horizon += 0.01
        if pygame.key.get_pressed()[pygame.K_z]:
            dy += 0.0015
        if pygame.key.get_pressed()[pygame.K_s]:
            dy -= 0.0015

        cos_a = math.cos(self.player_angle)
        sin_a = math.sin(self.player_angle)
        self.player_x += dx * cos_a - dy * sin_a
        self.player_y += dx * sin_a + dy * cos_a

        if pygame.key.get_pressed()[pygame.K_UP]:
            self.player_z += 0.02
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.player_z -= 0.02
        if pygame.key.get_pressed()[pygame.K_d]:
            self.player_angle -= 0.02
        if pygame.key.get_pressed()[pygame.K_q]:
            self.player_angle += 0.02

        pygame.display.set_caption(f"FPS : {str(round(self.app.fps))}")

    def _get_font(self, size, bold=True):
        key = (size, bold)
        if key not in self._fonts:
            self._fonts[key] = pygame.font.SysFont("lucidaconsole", size, bold)
        return self._fonts[key]

    def render_text(self, text, size, position, color=(255, 255, 255)):
        surf = self._get_font(size).render(text, False, color)
        self.hud.blit(surf, position)


    def render_hud(self):
        self.render_text("MODE-7-ENGINE", 20, (40, 10))
    
        self.render_text(f"x : {round(self.player_x * 100, 1)}", 10, (10, 70))
        self.render_text(f"y : {round(self.player_y * 100, 1)}", 10, (10, 85))
        self.render_text(f"z : {round(self.player_z * 100, 1)}", 10, (10, 100))
        self.render_text(f"angle : {round(math.degrees(self.player_angle), 1)}", 10, (10, 115))
        self.render_text(f"horizon : {round(self.horizon, 1)}", 10, (10, 130))
        


    def render(self):
        self.render_hud()
        self.ground.set_uniform("player_x", self.player_x)
        self.ground.set_uniform("player_y", self.player_y)
        self.ground.set_uniform("player_z", self.player_z)
        self.ground.set_uniform("player_angle", self.player_angle)
        self.ground.set_uniform("tex_infinite_scale", 9)
        self.ground.set_uniform("horizon_height", self.horizon)
        self.hud.set_uniform("time", self.app.timer)
        self.ground.render()
        self.hud.render()