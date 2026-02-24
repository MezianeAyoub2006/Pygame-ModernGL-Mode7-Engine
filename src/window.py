from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .app import App

INTERNAL_W, INTERNAL_H = 256, 240
WINDOW_SCALE = 3

import pygame 

class Window:
    """
    Component that handle Window related behaviors such as 
    * rescaling
    * fullscreen 
    * ...
    """
    def __init__(self, app:"App"):
        self.app = app
        self._internal_size = (INTERNAL_W, INTERNAL_H)
        info = pygame.display.Info()
        self.screen_size = (info.current_w, info.current_h) 
        self.screen = self.create_screen()
        self.fullscreen = False
    
    def toggle_fullscreen(self) -> None:
        if self.fullscreen:
            self.screen = self.create_screen()     
        else:
            self.screen = self.create_screen(None)  
        self.fullscreen = not self.fullscreen
  
    def create_screen(self, scale:int = WINDOW_SCALE, vsync:bool = False) -> pygame.Surface:
        if scale:
            self.offset = (0, 0)
            return pygame.display.set_mode(
                    (
                        self.internal_size[0] * scale, 
                        self.internal_size[1] * scale
                    ), 
                    pygame.OPENGL | pygame.DOUBLEBUF, 
                    vsync=vsync
                )
        else:
            fullscreen_viewport = self.fullscreen_viewport()
            self.offset = (
                fullscreen_viewport[0], 
                fullscreen_viewport[1]
            )
            return pygame.display.set_mode(
                self.screen_size, 
                pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN, 
                vsync=vsync
            )
        
    def fullscreen_viewport(self) -> tuple:
        """ 
        Returns the viewport shape, at fullscreen.
        """
        ratio = self.internal_size[0] / self.internal_size[1]
        
        if self.screen_size[0] / self.screen_size[1] > ratio:
            fullscreen_y = self.screen_size[1]
            fullscreen_x = fullscreen_y * ratio
            offset_x = (self.screen_size[0] - fullscreen_x) / 2
            offset_y = 0
        else:
            fullscreen_x = self.screen_size[0]
            fullscreen_y = fullscreen_x / ratio
            offset_x = 0
            offset_y = (self.screen_size[1] - fullscreen_y) / 2
        
        return int(offset_x), int(offset_y), int(fullscreen_x), int(fullscreen_y)
    
    @property
    def internal_size(self) -> tuple:
        return self._internal_size