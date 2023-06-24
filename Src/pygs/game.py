from .ui import display, grass, fireflies
from .entities import player
from .map import map
import pygame
class Game():
    def __init__(self, window_size = [0,0], double_buf = True):
        self.run = True
        self.display = display.Display("Pygs", window_size[0], window_size[1], double_buf)
        
    def load_game_items(self, game_items = {'player' : {}, 'map' : {}, 'world' : {}}):
        entities = {}
        if game_items['map'].get('entities'):
            for entity in game_items['map']['entities'].keys():
                entities[entity] = []
        print(entities)
        self.e_entities = game_items['map'].get('entities')
        self.map = map.Map(game_items['map']['map_loc'], game_items['map']['width_of_tiles'], game_items['map']['location_of_tiles'], game_items['map']['is_there_collide_tiles'], game_items['map']['is_there_non_collide_tiles'], entities )
        self.tile_rects, self.entity_loc = self.map.get_rect()
        self.player = player.Player(game_items['player'])
        self.game_items = game_items
        self.clock = pygame.time.Clock()
        #Grass
        self.grasses = []
        for loc in self.entity_loc['g']:
            x_pos = loc[0]
            while x_pos < loc[0] + 32:
                x_pos += 2.5
                self.grasses.append(grass.grass([x_pos, loc[1]+(14*2)], 2, 9))
        if game_items['map'].get("ignore_entities"):
            for key in game_items['map']['ignore_entities']:
                self.e_entities.pop(key)
        self.firefly = None
        if game_items['world'].get("fireflies"):
            self.firefly = fireflies.Fireflies(0, 100, 3000, 1000)
        self.entity_loc.pop("g")
        self.grass_last_update = 0
        self.grass_cooldown = 50
    
    def blit_grass(self, grasses, display, scroll, player):
        for grass in grasses:
            if grass.get_rect().colliderect(player.get_rect()):
                grass.colliding()
            grass.draw(display, scroll)
    
    def game_loop(self):
        true_scroll = [0,0]
        while self.run:
            self.clock.tick(60)
            time = pygame.time.get_ticks()
            self.display.redraw()
            #Normal code
            true_scroll[0] += (self.player.get_rect().x - true_scroll[0] - 202) 
            true_scroll[1] += (self.player.get_rect().y - true_scroll[1] - 132) 
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])
            self.map.draw(self.display, scroll)
            #Blitting entities
            for key in self.e_entities.keys():
                for loc in self.entity_loc[key]:
                    self.display.blit(self.e_entities[key][0], (loc[0] - scroll[0] - self.e_entities[key][1][0], loc[1] - scroll[1] - self.e_entities[key][1][1]))
            self.player.move(self.tile_rects, time)
            self.player.draw(self.display, scroll)
            #grass movement
            if time - self.grass_last_update > self.grass_cooldown:
                for grass in self.grasses:
                    grass.move()
                self.grass_last_update = time
            self.blit_grass(self.grasses, self.display, scroll, self.player)
            if self.firefly:
                self.firefly.recursive_call(time, self.display, scroll)
            self.run = self.display.clean()
