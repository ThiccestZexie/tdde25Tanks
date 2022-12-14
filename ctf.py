import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
from data import *
from sounds import *
#from images import *

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
from ai import *
import images
import gameobjects
import maps
from pygame import mixer
#-- Constants
FRAMERATE = 120

#-- Variables
#   Cooldown for tankshots
cooldown_tracker = 0
player_tank = 0
#   Define the current level
current_map         = maps.map0
#   List of all game objects
game_objects_list   = []
tanks_list          = []
ai_list             = []
bullet_list         = []

#-- Resize the screen to the size of the current level
screen = pygame.display.set_mode(current_map.rect().size)

#-- Generate the background
background = pygame.Surface(screen.get_size())

from pygame import mixer
from data import *


fail = ('data/Fail.wav')

# mixer.music.load('Boom.wav')
# mixer.music.load('Tiptoe.wav')
# mixer.music.load('data/Fail.wav')
# # mixer.music.load('Slip.wav')
# mixer.music.load('Background.wav')
# fail =  mixer.sound('Fail.mp3')
# fall = mixer.music.load('Fall.wav')
# background =  mixer.music.load('Background.wav')
# tiptoe = mixer.sound('Tiptoe.wav')   
#här ska respawn shield in
    # if respawn_flag:
    #     new_flag_pos = pymunk.vec2d(current_map.flag_position[0], current_map.flag_position[1])
#-- Main menu
os.environ['SDL_VIDEO_CENTERED'] = '1'


# Colors
white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

# Game Fonts
font = "data/good times rg.otf"


# Game Resolution
screen_width=  1400
screen_height=790
bg = pygame.image.load("data/backgroundimage.jpg").convert()
screen=pygame.display.set_mode((screen_width, screen_height))
# screen resolution 
res = (1400,790)

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
    return newText

def scoreboard():
    pass

def health_bar():
    health_list = []
    #color 
    red = (255, 0, 0)
    green = (0, 255, 0)
    for i in range(0, len(tanks_list)):
        health_x = tanks_list[i].body.position[0]*30
        health_y = tanks_list[i].body.position[1]*30
        health_list.append(pygame.draw.rect(screen, red, (health_x + 10, health_y + 10, 10, 10)))
        health_list.append(pygame.draw.rect(screen, green, (health_x + 10, health_y ,tanks_list[i].hp*15, 10)))

def main_menu():
   
    menu=True
    selected="start"
    indexlist= 0

    while menu:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:

                if event.key==pygame.K_UP:
                    indexlist = 0
                    if indexlist== 0:
                        selected= "start"
                        
                elif event.key==pygame.K_DOWN:
                    indexlist+=1
                    if indexlist == 1:
                        selected="quit"
                    elif indexlist == 2:
                        selected = "menu"
                    elif indexlist == 3:
                        selected = "map1"
                    elif indexlist == 4:
                        selected = "map2"
                    elif indexlist == 5:
                        selected = "map3"
                    
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        main_loop()
                    if selected=="quit":
                        pygame.quit()
                        quit()
                    if selected == "menu":
                        # fog_of_war()
                        main_loop()
                    if selected == "map1":
                        return current_map == maps.map0
                        # screen = pygame.display.set_mode(current_map.rect().size)
                    if selected == "map2":
                        return current_map == maps.map1
                        # screen = pygame.display.set_mode(current_map.rect().size)
                    if selected == "map3":
                        return current_map == maps.map2
                        # screen = pygame.display.set_mode(current_map.rect().size)
                        # background = pygame.Surface(screen.get_size())

        # Main Menu UI
        screen.fill(gray)
        screen.blit(pygame.transform.scale(images.grass, (screen_width, screen_height)), (0, 0))
        title=text_format("CTF", font, 90, yellow)
        if selected=="start":
            text_start=text_format("START", font, 75, white)
        else:
            text_start = text_format("START", font, 75, black)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, black)
        if selected == "menu":
            text_menu = text_format("OPTIONS", font, 75, white)
        else:
            text_menu = text_format("OPTIONS", font, 75, black)
        
        if selected == "map1":
            text_map1 = text_format("MAP1", font, 75, white)
        else:
            text_map1 = text_format("MAP1", font, 75, black)
        if selected == "map2":
            text_map2 = text_format("MAP2", font, 75, white)
        else:
            text_map2 = text_format("MAP2", font, 75, black)
        if selected == "map3":
            text_map3 = text_format("MAP3", font, 75, white)
        else:
            text_map3 = text_format("MAP3", font, 75, black)



        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
        menu_rect = text_menu.get_rect()
        map1_rect = text_map1.get_rect()
        map2_rect = text_map2.get_rect()
        map3_rect = text_map3.get_rect()


        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 20))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 100))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 160))
        screen.blit(text_menu, (screen_width/2 - (menu_rect[2]/2), 220))
        screen.blit(text_map1, (screen_width/2 - (map1_rect[2]/2), 280))
        screen.blit(text_map2, (screen_width/2 - (map2_rect[2]/2), 340))
        screen.blit(text_map3, (screen_width/2 - (map3_rect[2]/2), 400))
        pygame.display.update()
        clock.tick(FRAMERATE)
        pygame.display.set_caption("Main Menu Selection")
    return current_map

# def fog_of_war():
    
        
#     light=pygame.image.load('data/circle.png')
#     while True:
#         for e in pygame.event.get():
#             if e.type == pygame.QUIT: break
#         else:
#             screen.fill(pygame.color.Color('Red'))
#             for x in range(0, 640, 20):
#                 pygame.draw.line(screen, pygame.color.Color('Green'), (x, 0), (x, 480), 3)
#             filter = pygame.surface.Surface((640, 480))
#             filter.fill(pygame.color.Color('Grey'))
#             filter.blit(light, map(lambda x: x-50, player_tank.position))
#             screen.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
#             pygame.display.flip()
#             continue
#         break


#   Copy the grass tile all over the level area
def create_grass():
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # The call to the function "blit" will copy the image
            # contained in "images.grass" into the "background"
            # image at the coordinates given as the second argument
            background.blit(images.grass,  (x*images.TILE_SIZE, y*images.TILE_SIZE))


#-- Create the boxes
def create_boxes():
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # Get the type of boxes
            box_type  = current_map.boxAt(x, y)
            # If the box type is not 0 (aka grass tile), create a box
            if(box_type != 0):
                # Create a "Box" using the box_type, aswell as the x,y coordinates,
                # and the pymunk space
                box = gameobjects.get_box_with_type(x, y, box_type, space)
                game_objects_list.append(box)


#-- Create the tanks
def create_tanks():
    # Loop over the starting poistion
    for i in range(0, len(current_map.start_positions)):
        # Get the starting position of the tank "i"
        pos = current_map.start_positions[i]
        # Create the tank, images.tanks contains the image representing the tank
        tank = gameobjects.Tank(pos[0], pos[1], pos[2], images.tanks[i], space, i) # i = identifier
        # Add the tank to the list of tanks
        tanks_list.append(tank)
        game_objects_list.append(tank)

    for i in range(1, len(current_map.start_positions)):
        inst_ai = ai_creator(tanks_list[i])
        ai_list.append(inst_ai)

def ai_creator(tank):
    inst_ai = ai.Ai(tank, game_objects_list, tanks_list, space, current_map, bullet_list)
    return inst_ai
#-- Create the bases
def create_bases():
    for i in range(0,len(current_map.start_positions)):   
        pos_base = current_map.start_positions[i]
        bases = gameobjects.GameVisibleObject(pos_base[0], pos_base[1], images.bases[i])
        game_objects_list.append(bases)

#-- Create out of bound walls
def create_out_of_bounds():
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    walls  = [pymunk.Segment(body,(0,0),(0, current_map.width),0),
                pymunk.Segment(body,(0, 0), (current_map.height, 0), 0),
                pymunk.Segment(body,(0, current_map.width), (current_map.height, current_map.width), 0),
                pymunk.Segment(body,(current_map.height, 0), (current_map.height, current_map.width), 0)]
    space.add(walls)
        

#-- Create the flag
def create_flag():
    flag = gameobjects.Flag(current_map.flag_position[0], current_map.flag_position[1])
    game_objects_list.append(flag)
    return flag


   
def collision_bullet_box(arb,space,data):
    bullet = arb.shapes[0]
    box  = arb.shapes[1]
    if bullet and bullet.parent in bullet_list:
        space.remove(bullet, bullet.body) 
        bullet_list.remove(bullet.parent)
        if box.parent.destructable == True:
            game_objects_list.remove(box.parent)
            space.remove(box, box.body)
    return False

handler = space.add_collision_handler(1,3)
handler.post_solve = collision_bullet_box

def collision_bullet_tank(arb, space, data): #Instead of removing tank mby teleport it back to spawn
    bullet = arb.shapes[0]
    tank = arb.shapes[1]
    
    
    if tank.parent.name != bullet.parent.owner:
        tank.parent.hp -=1
        if tank.parent.hp == 0:    
            tank.parent.respawn()
            if tank.parent.name != player_tank:
                ai_list.append(ai_creator(tank.parent))
        #    print(ai_list[tank.parent.name].find_shortest_path())
            if tank.parent.flag == flag: 
                gameobjects.Tank.drop_flag(tank.parent, flag)
            if bullet.parent in bullet_list:
                space.remove(bullet, bullet.body)
                bullet_list.remove(bullet.parent)
        return False
    tank.hp = 3
handler = space.add_collision_handler(1,2)
handler.pre_solve = collision_bullet_tank





#----- Main Loop -----#
def main_loop():
    running = True 
    skip_update = 0
               

    while running:
        #-- Handle the events
        for event in pygame.event.get():
            # Check if we receive a QUIT event (for instance, if the user press the
            # close button of the wiendow) or if the user press the escape key.
             
            if event.type == QUIT:
                running = False
           
            if event.type ==  KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

                elif event.key == K_UP:
                    tanks_list[player_tank].accelerate() 

                elif event.key == K_DOWN:
                    tanks_list[player_tank].decelerate()

                elif event.key == K_LEFT:
                    tanks_list[player_tank].turn_left()

                elif event.key == K_RIGHT:
                    tanks_list[player_tank].turn_right()
                elif event.key == K_SPACE:
                    global cooldown_tracker
                    if cooldown_tracker >= 120:
                      bullet_list.append(tanks_list[player_tank].shoot(space))
                      cooldown_tracker = 0
                    
                

            if event.type == KEYUP:
                if event.key == K_UP:
                    tanks_list[player_tank].stop_moving() 
                    tanks_list[player_tank].stop_turning()

                elif event.key == K_DOWN:
                    tanks_list[player_tank].stop_moving() 
                    tanks_list[player_tank].stop_turning()

                elif event.key == K_LEFT:
                    tanks_list[player_tank].stop_turning()

                elif event.key == K_RIGHT:
                    tanks_list[player_tank].stop_turning()  
        def score():
            for i in range(len(tanks_list)):
                victory = tanks_list[i]
                if victory.has_won():
                    victory.score +=1
                    for j in tanks_list:
                        print(j.score)
                    victory.respawn()
            score()
        #-- Update physics
        if skip_update == 0:
            #  Loop over all the game objects and update their speed in function of their
            # acceleration.
            for obj in game_objects_list:
                obj.update()
            skip_update = 5
        else:
            skip_update -= 1

        #   Check collisions and update the objects position
        space.step(1 / FRAMERATE)

        #   Update object that depends on an other object position (for instance a flag)
        for obj in game_objects_list:
            obj.post_update()

        #-- Update Display
        # Display the background on the screen
        screen.blit(background, (0, 0))

        # Update the display of the game objects on the screen
        for obj in game_objects_list:
            obj.update_screen(screen)
        for bullets in bullet_list:
            bullets.update_screen(screen)
        #-- Checks for tanks
        for tanks in tanks_list:
            tanks.try_grab_flag(flag) 
        for tank in tanks_list:
            if tank.has_won() == True:
                score()
                # respawn.tank()
        #Ai update     
        for ai in ai_list:
            ai.decide()
        (ai_list[1].find_shortest_path())
        cooldown_tracker += 1
        health_bar() 
        
        #   Redisplay the entire screen (see double buffer technique)
        pygame.display.flip()
        #   Control the game framerate
        clock.tick(FRAMERATE)

create_grass()
create_boxes()
create_bases()
create_tanks()
create_out_of_bounds()
flag = create_flag()
main_menu()
main_loop()
