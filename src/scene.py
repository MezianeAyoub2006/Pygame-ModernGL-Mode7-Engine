import pygame 
import math 

from .shader_pass import ShaderPass
from .pygame_layer import PygameLayer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .app import App

class Scene:
    """
    Render and update hooks container, used for organization purposes.
    """
    def __init__(self, app:"App"):
        self.app = app 
        self._fonts = {}
        with open("shaders/outline.glsl", "r", encoding = "utf-8") as f:
            self.hud = PygameLayer(app, f.read()) 
        with open("shaders/mode7.glsl", "r", encoding = "utf-8") as f:
            self.ground = ShaderPass(app, f.read()) 
        self.ground.load_texture("tex", "assets/ground.png", 0)
        self.ground.load_texture("tex_infinite", "assets/ground-infinite.png", 1)
      
        self.init_player_data()

    def init_player_data(self) -> None:
        self.player_x = 0.5
        self.player_y = 0
        self.player_z = 3
        self.player_angle = 0
        self.horizon = 0.3

    def update(self) -> None:
        """
        Updating hook.
        """
        self.player_movement()
        pygame.display.set_caption(f"Mode-7-Engine")
        self.set_uniforms()

    def render(self) -> None:
        """
        Rendering hook.
        """
        self.render_hud()    
        self.ground.render()
        self.hud.render()
    
    def player_movement(self) -> None:
        """
        Handles player movements.
        """
        dx, dy = 0, 0
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.horizon -= 0.01 * self.app.dt
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.horizon += 0.01 * self.app.dt
        if pygame.key.get_pressed()[pygame.K_z]:
            dy += 0.0015 * self.app.dt
        if pygame.key.get_pressed()[pygame.K_s]:
            dy -= 0.0015 * self.app.dt

        cos_a = math.cos(self.player_angle)
        sin_a = math.sin(self.player_angle)
        self.player_x += dx * cos_a - dy * sin_a
        self.player_y += dx * sin_a + dy * cos_a

        if pygame.key.get_pressed()[pygame.K_UP]:
            self.player_z += 0.02 * self.app.dt
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.player_z -= 0.02 * self.app.dt
        if pygame.key.get_pressed()[pygame.K_d]:
            self.player_angle -= 0.02 * self.app.dt
        if pygame.key.get_pressed()[pygame.K_q]:
            self.player_angle += 0.02 * self.app.dt

    def set_uniforms(self) -> None:
        """ 
        Sets the uniforms of the ground ShaderPass layer.
        """
        self.ground.set_uniform("player_x", self.player_x)
        self.ground.set_uniform("player_y", self.player_y)
        self.ground.set_uniform("player_z", self.player_z)
        self.ground.set_uniform("player_angle", self.player_angle)
        self.ground.set_uniform("tex_infinite_scale", 9)
        self.ground.set_uniform("horizon_height", self.horizon)
        self.ground.set_uniform("time", self.app.timer)

    def render_hud(self) -> None:
        """ 
        Renders the HUD, in pygame.
        x, y, z positions are rendered 100 times larger 
        for uniformity purposes.
        """
        self.render_text("MODE-7-ENGINE", 20, (40, 10))
        self.render_text(f"x : {round(self.player_x * 100, 1)}", 10, (10, 160))
        self.render_text(f"y : {round(self.player_y * 100, 1)}", 10, (10, 175))
        self.render_text(f"z : {round(self.player_z * 100, 1)}", 10, (10, 190))
        self.render_text(f"angle : {round(math.degrees(self.player_angle), 1)}", 10, (10, 205))
        self.render_text(f"horizon : {round(self.horizon, 1)}", 10, (10, 220))
        self.render_text(f"fps : {round(self.app.fps, 1)}", 10, (170, 220))

    def render_text(self, text:str, size:tuple, position:tuple, color:tuple = (255, 255, 255)):
        """ 
        Renders a text.
        """
        surf = self._get_font(size).render(text, False, color)
        self.hud.blit(surf, position)

    def _get_font(self, size:tuple, bold:bool = True):
        """ 
        SysFont caching method.
        """
        key = (size, bold)
        if key not in self._fonts:
            self._fonts[key] = pygame.font.SysFont("lucidaconsole", size, bold)
        return self._fonts[key]
  