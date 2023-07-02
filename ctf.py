import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import pygame.mixer
from pygame.mixer import Sound
import math


#----- Initialisation -----#

#-- Initialise the display
pygame.init()
pygame.display.set_mode()

#-- Initialise the clock
clock = pygame.time.Clock()

#-- Initialise the physics engine
space = pymunk.Space()
space.gravity = (0.0,  0.0)
space.damping = 0.1 # Adds friction to the ground for all objects


#-- Import from the ctf framework
import ai
import images
import gameobjects
import maps
import settings
import menu

#-- Constants
FRAMERATE = 120

#-- Variables
#   Define the current settings
game_settings       = settings.Settings() 
#   List of all game objects
game_objects_list   = []
tanks_list          = []
ai_list             = []

# Tank variables
player_tank = None
player_two_tank = None



#-- initialize all sounds.
pygame.mixer.init()

background_music = pygame.mixer.music.load("data/sounds/music.wav")
hit_sound = Sound("data/sounds/tankboom.wav")
wood_sound = Sound("data/sounds/woodhit.wav")

pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

#-- create game border.. 
def create_out_of_area(): 
    static_body = space.static_body
    space.add(*[
        pymunk.Segment(static_body, (0, 0), (0, game_settings.current_map.height), 0),
        pymunk.Segment(static_body, (0, 0), (game_settings.current_map.width, 0), 0),
        pymunk.Segment(static_body,
                        (game_settings.current_map.width, game_settings.current_map.height),
                        (game_settings.current_map.width, 0), 0),
        pymunk.Segment(static_body,
                        (game_settings.current_map.width, game_settings.current_map.height),
                        (0, game_settings.current_map.height), 0)
    ])

def create_fog_of_war():
        screen_width, screen_height = screen.get_size()
        radius = min(screen_width, screen_height)
        fog_of_war = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        fog_of_war.fill((0, 0, 0))
        pygame.draw.circle(fog_of_war, (0,0,0, 100), (radius, radius), 150)
        fog_of_war_rect = fog_of_war.get_rect()
        fog_of_war_rect.center = gameobjects.physics_to_display(tanks_list[0].body.position)

        # Draw the fog of war over the game screen
        screen.blit(fog_of_war, fog_of_war_rect)



def create_objects():
    for x in range(0, game_settings.current_map.width):
        for y in range(0,  game_settings.current_map.height):
            background.blit(images.grass,  (x*images.TILE_SIZE, y*images.TILE_SIZE))
    #-- Create the boxes
    for x in range(0, game_settings.current_map.width):
        for y in range(0,  game_settings.current_map.height):
            # Get the type of boxes
            box_type  = game_settings.current_map.boxAt(x, y)
            # If the box type is not 0 (aka grass tile), create a box
            if(box_type != 0):
                # Create a "Box" using the box_type, aswell as the x,y coordinates,
                # and the pymunk space
                box = gameobjects.get_box_with_type(x, y, box_type, space)
                game_objects_list.append(box)

    #-- Create the tanks
    # Loop over the starting poistion
    for i in range(0, len(game_settings.current_map.start_positions)):
        # Get the starting position of the tank "i"
        pos = game_settings.current_map.start_positions[i]
        # Create the tank, images.tanks contains the image representing the tank
        tank = gameobjects.Tank(pos[0], pos[1], pos[2], images.tanks[i], space, i, FRAMERATE)
        # Add the tank to the list of tanks
        tanks_list.append(tank)
        game_objects_list.append(tank)
    if not game_settings.hot_seat_multiplayer:
        for i in range(1, len(game_settings.current_map.start_positions)):
            ai_list.append(ai.Ai(tanks_list[i],game_objects_list, tanks_list, space, game_settings))
    else:
         for i in range(2, len(game_settings.current_map.start_positions)):
            ai_list.append(ai.Ai(tanks_list[i],game_objects_list, tanks_list, space, game_settings))

    #-- Create the tank bases
    for i in range(0,len(game_settings.current_map.start_positions)):   
        pos_base = game_settings.current_map.start_positions[i]
        bases = gameobjects.GameVisibleObject(pos_base[0], pos_base[1], images.bases[i])
        game_objects_list.append(bases)

def display_text(font_size, input_text, screen_pos):
    font = pygame.font.Font(None, font_size)
    display_text = font.render(str(input_text), 1, (255,0,0))
    screen.blit(display_text, screen_pos)

def score_screen():
        screen_width =  game_settings.current_map.rect().size[0]
        screen_height= game_settings.current_map.rect().size[1]
        bg = pygame.image.load("data/grass.png").convert()       
        score = True
        while score:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    score = False
                if event.type ==  KEYDOWN:
                    if event.key == K_ESCAPE:
                        score = False
                        break
            
            screen.fill((50, 50, 50))
            screen.blit(pygame.transform.scale(images.grass, (screen_width, screen_height)), (0, 0))
            location = 50
            for tanks in tanks_list:
                display_text(50, (f"Player {tanks.id + 1}: {tanks.points}"),(screen_width/2 - 100, location) )
                location += 50
            pygame.display.update()
            clock.tick(FRAMERATE) 

def player_1(event):
        
        # Check if we receive a QUIT event (for instance, if the user press the
        # close button of the wiendow) or if the user press the escape key.
        if event.type == KEYDOWN:
            if event.key == K_UP:
                player_tank.accelerate() 

            elif event.key == K_DOWN:
                player_tank.decelerate()
            elif event.key == K_LEFT:
                player_tank.turn_left()

            elif event.key == K_RIGHT:
                player_tank.turn_right()
            elif event.key == K_SPACE:
                if player_tank.shoot_cooldown < 1: game_objects_list.append(player_tank.shoot(space))            

        if event.type == KEYUP:
            if event.key == K_UP:
                player_tank.stop_moving() 
                player_tank.stop_turning()

            elif event.key == K_DOWN:
                player_tank.stop_moving() 
                player_tank.stop_turning()

            elif event.key == K_LEFT:
                player_tank.stop_turning()

            elif event.key == K_RIGHT:
                player_tank.stop_turning()    
    

def player_2(event):
    if event.type == KEYDOWN:
        if event.key == K_w:
            player_two_tank.accelerate() 

        elif event.key == K_s:
            player_two_tank.decelerate()

        elif event.key == K_a:
            player_two_tank.turn_left()

        elif event.key == K_d:
            player_two_tank.turn_right()
        elif event.key == K_LSHIFT:
            if player_two_tank.shoot_cooldown < 1: game_objects_list.append(player_tank.shoot(space))            
                
        

    if event.type == KEYUP:
        if event.key == K_w:
            player_two_tank.stop_moving() 
            player_two_tank.stop_turning()

        elif event.key == K_s:
            player_two_tank.stop_moving() 
            player_two_tank.stop_turning()

        elif event.key == K_a:
            player_two_tank.stop_turning()

        elif event.key == K_d:
            player_two_tank.stop_turning()  

def tank_update():
    #Tank update
    for tank in tanks_list:
        tank.update_screen(screen) 
        if game_settings.wincon == 3:
            display_text(24,f"{tank.points}/{game_settings.points_to_win}", gameobjects.physics_to_display(tank.start_position))
            if tank.points == game_settings.points_to_win:
                score_screen()
                game_settings.running =False
        else:
            display_text(24,tank.points, gameobjects.physics_to_display(tank.start_position))

        if tank.has_won():
            tank.points += 1
            game_settings.curr_round += 1
            tank.respawn()
            flag.x = game_settings.current_map.flag_position[0]
            flag.y = game_settings.current_map.flag_position[1]     
            score_screen()
            
            if game_settings.wincon == 1:
                if game_settings.curr_round == game_settings.t_rounds:
                    return False
            if game_settings.wincon == 3:
                if tank.points == game_settings.points_to_win:
                    return False
            else: 
                return False
        
def win_con_display():
    if game_settings.wincon == 2:
            display_text(40, (f"{game_settings.curr_round}/{game_settings.t_rounds}"), (screen_width/2 ,5))
            if game_settings.curr_round == game_settings.t_rounds:
                score_screen()
                game_settings.running = False
        #Win con timer
    if game_settings.wincon == 0:
            display_text(40, math.floor(game_settings.time), (screen_width/2,5))
            if game_settings.time <= 1:
                score_screen()
                game_settings.running = False
            game_settings.time -=(1/FRAMERATE)
def tanks_grab_flag():
    [tank.try_grab_flag(flag) for tank in tanks_list]
def remove_explosion():
    [game_objects_list.remove(explosion) for explosion in game_objects_list if isinstance(explosion, gameobjects.Explosion)  and explosion.tracker > FRAMERATE/2] 



#----- Main Loop -----#
#-- Resize the screen to the size of the current level
screen = pygame.display.set_mode(game_settings.current_map.rect().size)
screen_width = screen.get_width()

#-- Generate the background
background = pygame.Surface(screen.get_size())

#Create menu
game_menu = menu.Main_menu_creator(game_settings, FRAMERATE, screen)
# recreate background if a new map is set.
screen = pygame.display.set_mode(game_settings.current_map.rect().size)
background = pygame.Surface(screen.get_size()) 

create_out_of_area()
create_objects()

#-- Create the variables
flag = gameobjects.Flag(game_settings.current_map.flag_position[0], game_settings.current_map.flag_position[1])
game_objects_list.append(flag)
player_tank = tanks_list[0]
if game_settings.hot_seat_multiplayer:
    player_two_tank = tanks_list[1]



#-- Collision handelers
def collision_bullet_tank(arb, space, data):
    bullet = arb.shapes[0].parent
    tank = arb.shapes[1].parent

    if bullet.owner != tank.id:
        if tank.invicible_frames < 1:
            if(tank.hp == 1):
                game_objects_list.append(gameobjects.Explosion(images.explosion, tank.body.position ))  
                tank.respawn()
            else: 
                tank.hp -= 1
            hit_sound.play()
        game_objects_list.remove(bullet)
        space.remove(bullet.shape, bullet.body)

    return False


def collision_bullet_box(arb,space,data):
    bullet = arb.shapes[0].parent
    box  = arb.shapes[1].parent
    if bullet in game_objects_list:
        space.remove(bullet.shape, bullet.body) 
        game_objects_list.remove(bullet)
    if box.destructable == True:
        if box in game_objects_list:
            if box.hp == 1:
                wood_sound.play()
                game_objects_list.append(gameobjects.Explosion(images.explosion, box.body.position))
                game_objects_list.remove(box)
                space.remove(box.shape, box.body)
            else:
                box.hp -= 1
    return False


def collision_bullet_rest(arb,space,data):
    bullet=arb.shapes[0].parent
    if bullet in game_objects_list:
        game_objects_list.remove(bullet)
        space.remove(bullet.shape, bullet.body)
    return False


handler = space.add_collision_handler(1,0)
handler.pre_solve = collision_bullet_rest

handler = space.add_collision_handler(1,3)
handler.pre_solve = collision_bullet_box

handler_tank = space.add_collision_handler(1, 2)
handler_tank.pre_solve = collision_bullet_tank

#-- Control whether the game run
game_settings.running = True

skip_update = 0

while game_settings.running:
    #-- Handle the events
    for event in pygame.event.get():
            if event.type == QUIT:
                game_settings.running = False
            if event.type ==  KEYDOWN:
                if event.key == K_ESCAPE:
                    game_settings.running = False
                    break
            if game_settings.hot_seat_multiplayer == True:
                player_1(event)
                player_2(event)
            elif game_settings.hot_seat_multiplayer == False:
                player_1(event)

 

    #-- Update physics
    if skip_update == 0:
        # Loop over all the game objects and update their speed in function of their
        # acceleration.
        for obj in game_objects_list:
            obj.update()
        skip_update = 2
    else:
        skip_update -= 1
    

    #   Check collisions and update the objects position
    space.step(1 / FRAMERATE)

    #   Update object that depends on an other object position (for instance a flag)
    for obj in game_objects_list:
        if obj != None:
            obj.post_update()

    #-- Update Display
    #   remove expired explosions
    remove_explosion()

    # Display the background on the screen
    screen.blit(background, (0, 0))

    # Update the display of the game objects on the screen
    for obj in game_objects_list:
        if obj != None:
            obj.update_screen(screen)

    #Flag update    
    flag.update_screen(screen)
    tank_update()
    # Self implemented game checks
    tanks_grab_flag()
    win_con_display()
        
    #win con rounds go out
    if game_settings.fog_of_war:
        create_fog_of_war()
    #Ai decide loop
    [Ai.decide() for Ai in ai_list]

    #----------------------
    #   Redisplay the entire screen (see double buffer technique)
    pygame.display.flip()
    
    #   Control the game framerate
    clock.tick(FRAMERATE)

# print points
[print(f"Player {tanks.id + 1}: {tanks.points}") for tanks in tanks_list]


