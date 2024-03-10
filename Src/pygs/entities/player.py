import pygame
from pygame.locals import *
class Player():
    #items keys :  x, y, width, height, idle_animation, run_animation, jump_img, fall_img) -> None:
    def __init__(self, items, replace_x = None, replace_y = None):
        if replace_x or replace_y:
            self.rect = pygame.rect.Rect(replace_x, replace_y, items['width'], items['height'])    
        else:
            self.rect = pygame.rect.Rect(items['x'], items['y'], items['width'], items['height'])
        self.movement = [0,0]
        self.display_x = 0
        self.display_y = 0
        self.moving_left = False
        self.moving_right = False
        self.collision_type = {}
        self.speed = 4
        self.display_x = 0
        self.display_y = 0
        self.idle_animation = items['idle_animation']
        self.run_animation = items['run_animation']
        self.frame = 0
        self.frame_last_update = 0
        self.frame_cooldown = 200
        self.facing_right = True
        self.jump = False
        self.jump_img = items['jump_img']
        self.fall_img = items['fall_img']
        self.jump_last_update = 0
        self.radius = items['width'] 
        self.jump_cooldown = 200
        self.jump_up_spped = 9
        self.air_timer = 0
        self.falling = False
        self.jump_count = 2
        self.joy_value = 0.0
        self.gravity = 8

    def collision_test(self, tiles):
        hitlist = []
        for tile in tiles:
            if tile.touchable:
                if self.rect.colliderect(tile.get_rect()):
                    hitlist.append(tile)
        return hitlist
    
    def collision_checker(self, tiles):
        collision_types = {"top": [False, []], "bottom": [False, []], "right": [False, []], "left": [False, []]}
        self.rect.x += self.movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if not tile.ramp:
                if self.movement[0] > 0:
                    self.rect.right = tile.get_rect().left
                    collision_types["right"][0] = True
                    collision_types["right"][1].append(tile)
                elif self.movement[0] < 0:
                    self.rect.left = tile.get_rect().right
                    collision_types["left"][0] = True
                    collision_types["left"][1].append(tile)
        self.rect.y += self.movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if not tile.ramp:
                if self.movement[1] > 0:
                    self.rect.bottom = tile.get_rect().top
                    collision_types["bottom"][0] = True
                    collision_types["bottom"][1].append(tile)
                if self.movement[1] < 0:
                    self.rect.top = tile.get_rect().bottom
                    collision_types["top"][0] = True
                    collision_types['top'][1].append(tile)
        
        for tile in hit_list:
            if tile.ramp == True:
                rel_x = self.rect.x - tile.get_rect().x
                if tile.ramp_type == 1:
                    pos_height = rel_x + self.rect.width
                elif tile.ramp_type == 2:
                    pos_height = 32 - rel_x
                pos_height = min(pos_height, 32)
                pos_height = max(pos_height, 0)
                target_y = tile.get_rect().y + 32 - pos_height
                if self.rect.bottom > target_y:
                    self.rect.bottom = target_y
                    collision_types["bottom"][0] = True
                    self.movement[1] = self.rect.y
        return collision_types
    
    def move(self, tiles, time, hud_controls, water_locs):
        self.movement = [0, 0]
        #check if in water
        in_water = False
        for locations in water_locs:
            if self.rect.x > locations[0][0] and self.rect.x < locations[1][0]:
                if self.rect.y > locations[0][1] and self.rect.y <= locations[1][1]:
                    in_water = True
        if in_water:
            self.speed = 2
            self.gravity = 1
        else:
            self.speed = 4
            self.gravity = 8
        
        if self.moving_right:
            self.facing_right = True
            self.movement[0] += self.speed
            self.moving_right = False
        if self.moving_left:
            self.facing_right = False
            self.movement[0] -= self.speed
            self.moving_left = False
        if self.jump:
            if self.air_timer < 40:
                self.air_timer += 1
                self.movement[1] -= self.jump_up_spped
                self.jump_up_spped -= 0.5
            else:
                self.air_timer = 0
                self.jump = False
                self.jump_up_spped = 9

        if time - self.frame_last_update > self.frame_cooldown:
            self.frame_last_update = time
            self.frame += 1
            if self.frame >= 4:
                self.frame = 0

        if not self.jump:
            self.movement[1] += self.gravity

        

        self.collision_type = self.collision_checker(tiles)

        if not self.collision_type['bottom'][0]:
            self.falling = True
        else:
            self.jump_count = 2
            self.falling = False
        if hud_controls.get("x_axis"):
            self.joy_value = hud_controls.get("x_axis")
        if hud_controls.get("left") or self.joy_value < -0.3:
            self.moving_left = True
        if hud_controls.get("right") or self.joy_value > 0.3:
            self.moving_right = True
        if hud_controls.get("jump"):
            if self.jump_count > 0:
                if time - self.jump_last_update > self.jump_cooldown:
                    #self.music.play()
                    self.jump = True
                    self.air_timer = 0
                    self.jump_up_spped = 9
                    self.jump_count -= 1
                    self.jump_last_update = time

        
    
    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        if self.air_timer >= 1 and self.air_timer > 20:
            if self.facing_right:
                display.blit(self.fall_img, self.rect)
            else:
                flip = self.fall_img.copy()
                flip = pygame.transform.flip(flip, True, False)
                display.blit(flip, self.rect)
        elif not self.jump and  self.falling:
            if self.facing_right:
                display.blit(self.fall_img, self.rect)
            else:
                flip = self.fall_img.copy()
                flip = pygame.transform.flip(flip, True, False)
                display.blit(flip, self.rect)
        elif self.jump:
            if self.facing_right:
                display.blit(self.jump_img, self.rect)
            else:
                flip = self.jump_img.copy()
                flip = pygame.transform.flip(flip, True, False)
                display.blit(flip, self.rect)
        elif self.moving_right:
            display.blit(self.run_animation[self.frame], self.rect)
        elif self.moving_left:
            flip = self.run_animation[self.frame].copy()
            flip = pygame.transform.flip(flip, True, False)
            display.blit(flip, self.rect)
        else:
            if self.facing_right:
                display.blit(self.idle_animation[self.frame], self.rect)
            else:
                flip = self.idle_animation[self.frame].copy()
                flip = pygame.transform.flip(flip, True, False)
                display.blit(flip, self.rect)
        
        #display.blit(self.circle_surf(), (self.rect.x - 15, self.rect.y - 15), special_flags=BLEND_RGBA_ADD)

        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def get_rect(self):
        return self.rect

    def circle_surf(self):
        surf = pygame.Surface((self.radius * 4, self.radius * 4))
        pygame.draw.circle(surf, (20, 20,20), (self.radius, self.radius), self.radius)
        surf.set_colorkey((0, 0, 0))
        return surf
