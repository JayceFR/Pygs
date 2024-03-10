from .ui import display, grass, fireflies, bg_particles, water
from .entities import player
from .map import map
import pygame, random, math, time as t
class Game():
    def __init__(self, window_size = [0,0], double_buf = True, is_shader = False, vertex_loc = "", fragment_loc = ""):
        self.run = True
        self.window_size = window_size
        self.double_buf = double_buf
        self.shader_stuf = {}
        self.hud_controls = {"run" : True}
        self.display = display.Display("Pygs", self.window_size[0], self.window_size[1], self.double_buf)
        if is_shader:
            self.display = display.Display("Pygs", self.window_size[0], self.window_size[1], self.double_buf, True, vertex_loc, fragment_loc )
        else:
            self.display = display.Display("Pygs", self.window_size[0], self.window_size[1], self.double_buf)
        
    def load_game_items(self, game_items = {'player' : {}, 'map' : {}, 'world' : {}}):
        self.shader_stuf = game_items['world']['shader']
        entities = {}
        if game_items['map'].get('entities'):
            for entity in game_items['map']['entities'].keys():
                entities[entity] = []
        # print(entities)
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
                height = random.randint(3,15)
                self.grasses.append(grass.grass([x_pos, loc[1]+(14*2) - (height - 9) ], 2, height))
        #water
        self.water_pos = []
        for loc in self.entity_loc['w']:
            if self.water_pos == []:
                self.water_pos.append([loc,])
            else:
                if loc[0] - 32 == self.water_pos[-1][-1][0]:
                    self.water_pos[-1].append(loc)
        self.waters = []
        self.water_locs = []
        for locations in self.water_pos:
            self.waters.append(water.Water((locations[0][0], locations[0][1]+20), (len(locations) + 1) *2, 16, 64-20))
            self.water_locs.append([(locations[0][0], locations[0][1]+20), (locations[0][0] + len(locations) * 32, locations[0][1] + 64)])
        if game_items['map'].get("ignore_entities"):
            for key in game_items['map']['ignore_entities']:
                self.e_entities.pop(key)
        self.firefly = None
        if game_items['world'].get("fireflies"):
            self.firefly = fireflies.Fireflies(0, 100, 3000, 1000)
        self.bg_particle_effect = None
        if game_items['world'].get("leaves")[0]:
            self.bg_particle_effect = bg_particles.Master(game_items['world']['leaves'][1])
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
        start_time = t.time()
        #silhouette
        val = 0
        # waterm = water.Water((1000,310), 50, 16, 60)
        while self.hud_controls["run"]:
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
            self.player.move(self.tile_rects, time, self.hud_controls, self.water_locs)
            self.player.draw(self.display, scroll)
            # print(self.player.get_rect().x, self.player.get_rect().y)
            '''
            #Sillhouette
            self.display.sillhouette(val)
            val += 1
            if val > 255:
                val = 0'''
            for waterm in self.waters:
                waterm.update(scroll, self.player.get_rect())
                waterm.draw(self.display.water_display, scroll)
            #grass movement
            if time - self.grass_last_update > self.grass_cooldown:
                for grass in self.grasses:
                    grass.move()
                self.grass_last_update = time
            self.blit_grass(self.grasses, self.display, scroll, self.player)
            if self.bg_particle_effect:
                self.bg_particle_effect.recursive_call(time, self.display, scroll, 1)
            if self.firefly:
                self.firefly.recursive_call(time, self.display, scroll)
            # print(scroll)
            self.hud_controls = self.display.clean({"noise_tex1": self.shader_stuf['noise_img'], "noise_tex2": self.shader_stuf['noise_img2']}, { "itime": t.time() - start_time, "cam_scroll" : tuple(list(scroll))})
            # self.hud_controls = self.display.clean({})
