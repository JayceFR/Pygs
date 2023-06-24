import pygame 

class Display():
    def __init__(self, title, screen_w, screen_h, double_up = True):
        self.title = title
        self.double_up = double_up
        self.screen_w = screen_w
        self.screen_h = screen_h
        if double_up:
            self.window = pygame.display.set_mode((screen_w, screen_h))
            self.display = pygame.Surface((screen_w//2, screen_h//2))
        else:
            self.display = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption(title)
    
    def redraw(self):
        self.display.fill((0,0,0))

    def clean(self):
        if self.double_up:
            surf = self.display.copy()
            surf = pygame.transform.scale(surf, (self.screen_w, self.screen_h))
            self.window.blit(surf, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        pygame.display.flip()
        return True
    
    def blit(self, img, dest, special_flags = None):
        if special_flags:
            self.display.blit(img, dest, special_flags=special_flags)
        else:
            self.display.blit(img, dest)
    
    def draw_polygon(self, color, points):
        pygame.draw.polygon(self.display, color, points)
    
    def draw_circle(self, color, center, radius):
        pygame.draw.circle(self.display, color, center, radius)
    
        
        

