import pygame
import Src.pygs.game as game
import Src.pygs.utils.misc as misc

#loading images
help = misc.Misc()
display = pygame.display.set_mode((100,100))
#player
idle_animation = help.load_animation("./Assets/Sprites/squirrel_idle.png", 4, 2, (63,72,204))
print(idle_animation)
run_animation = help.load_animation("./Assets/Sprites/squirrel_run.png", 4, 2, (63,72,204))
jump_img = help.load_img("./Assets/Sprites/squirrel_jump.png", (63,72,204), 45, 2)
fall_img = help.load_img("./Assets/Sprites/squirrel_jump.png", (63,72,204), -25, 2)
#entities
orange_tree = help.load_img("./Assets/Entities/tree.png", (0,0,0), scale=1.5)
pink_tree = help.load_img("./Assets/Entities/tree2.png", (0,0,0), scale=1.5)
fence = help.load_img("./Assets/Entities/fence.png", (255,255,255), scale_coords=[32,19])

pass_e_game = {
    'player' : {
        'x' : 1000, 
        'y' : 200, 
        'width' : idle_animation[0].get_width(), 
        'height': idle_animation[0].get_height(), 
        'idle_animation' : idle_animation, 
        'run_animation' : run_animation, 
        'jump_img' : jump_img, 
        'fall_img': fall_img
        },
    'map' : {
        'map_loc' : "./Assets/Maps/map.txt", 
        'width_of_tiles': 32, 
        'location_of_tiles' : "./Assets/Tiles", 
        'is_there_collide_tiles' : True, 
        'is_there_non_collide_tiles': True,
        'entities' : {
            "f" : [fence, [0, -12]],
            "o" : [orange_tree, [69,110]],
            "p" : [pink_tree, [69,110]],
        }
        }
    }

e = game.Game([1000,600], True, pass_e_game )
e.game_loop()