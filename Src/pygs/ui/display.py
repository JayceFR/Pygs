import pygame 
from ..shader import shader
from ..ui import hud

class Display():
    def __init__(self, title, screen_w, screen_h, double_up = True, open_gl = False, vertex_loc = "", fragment_loc = ""):
        self.title = title
        self.double_up = double_up
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.open_gl = open_gl
        self.vertex_loc = vertex_loc
        self.fragment_loc = fragment_loc
        self.shader_obj = None
        self.hud = hud.Hud()
        if double_up:
            if self.open_gl:
                self.screen = pygame.display.set_mode((screen_w, screen_h), pygame.OPENGL | pygame.DOUBLEBUF)
                self.window = pygame.Surface((screen_w, screen_h))
            else:
                self.window = pygame.display.set_mode((screen_w, screen_h))
            self.dummy_display = pygame.Surface((screen_w//2, screen_h//2))
        else:
            if self.open_gl:
                self.dummy_display = pygame.display.set_mode((screen_w, screen_h), pygame.OPENGL | pygame.DOUBLEBUF)
            else:
                self.dummy_display = pygame.display.set_mode((screen_w, screen_h))
        self.display = pygame.Surface((screen_w//2, screen_h//2), pygame.SRCALPHA)
        if self.open_gl:
            self.shader_obj = shader.Shader(True, vertex_loc, fragment_loc)
            self.ui_display = pygame.Surface((screen_w//2, screen_h//2), pygame.SRCALPHA)
            self.water_display = pygame.Surface((screen_w//2, screen_h//2), pygame.SRCALPHA) 
        pygame.display.set_caption(title)
    
    def redraw(self):
        self.dummy_display.fill((0,0,0))
        self.display.fill((0,0,0,0))
        if self.open_gl:
            self.ui_display.fill((0,0,0,0))
            self.water_display.fill((0,0,0,0))

    def clean(self, uniform = {}, variables = {}):
        self.dummy_display.blit(self.display, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        if self.double_up:
            surf = self.dummy_display.copy()
            surf = pygame.transform.scale(surf, (self.screen_w, self.screen_h))
            self.window.blit(surf, (0,0))
        self.hud.events()
        if self.shader_obj:
            uniform['tex'] = self.window
            uniform['ui_tex'] = self.ui_display
            uniform['water_tex'] = self.water_display
            #self.shader_obj.draw({"tex" : self.window, "noise_tex1": noise_img, "ui_tex" : ui_display}, { "itime": int((t.time() - start_time) * 100) })
            self.shader_obj.draw(uniform, variables)
        pygame.display.flip()
        return self.hud.get_controls()

    def sillhouette(self, val):
        display_mask = pygame.mask.from_surface(self.display)
        display_sillhoutte = display_mask.to_surface(setcolor=(0,0,0,val), unsetcolor=(0,0,0,0))
        self.blit(display_sillhoutte, (0,0))
    
    def blit(self, img, dest, special_flags = None, ui_display = False):
        if not ui_display:
            if special_flags:
                self.display.blit(img, dest, special_flags=special_flags)
            else:
                self.display.blit(img, dest)
        else:
            if special_flags:
                self.ui_display.blit(img, dest, special_flags=special_flags)
            else:
                self.ui_display.blit(img, dest)

    
    def draw_polygon(self, color, points):
        pygame.draw.polygon(self.display, color, points)
    
    def draw_circle(self, color, center, radius, ui_display = False):
        if ui_display:
            pygame.draw.circle(self.ui_display, color, center, radius)    
        pygame.draw.circle(self.display, color, center, radius)
    
        
        

