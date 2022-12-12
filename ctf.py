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
pygame.display.set_mode((800, 600))

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
screen_width=800
screen_height=600
screen=pygame.display.set_mode((screen_width, screen_height))

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
    return newText




def main_menu():

    menu=True
    selected="start"
    
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        print("Start")
                    if selected=="quit":
                        pygame.quit()
                        quit()
    
        # Main Menu UI
        screen.fill(red)
        title=text_format("CTF", font, 90, yellow)
        if selected=="start":
            text_start=text_format("START", font, 75, white)
        else:
            text_start = text_format("START", font, 75, black)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, black)
    
        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
    
        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 360))
        pygame.display.update()
        clock.tick(FRAMERATE)
        pygame.display.set_caption("Main Menu Selection")


#-- buttons
# class Button:
#     """Create a button, then blit the surface in the while loop"""

#     def __init__(self, text,pos, font, bg="black", feedback=""):
#         self.x, self.y = pos
#         self.font = pygame.font.SysFont("data/good times rg.otf", font)
#         if feedback == "":
#             self.feedback = "text"
#         else:
#             self.feedback = feedback
#             self.change_text(text, bg)

#     def change_text(self, text, bg="black"):
#         """Change the text whe you click"""
#         self.text = self.font.render(text, 1, pygame.Color("White"))
#         self.size = self.text.get_size()
#         self.surface = pygame.Surface(self.size)
#         self.surface.fill(bg)
#         self.surface.blit(self.text, (0, 0))
#         self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

#     def show(self):
#         screen.blit(start_button.surface, (self.x, self.y))

#     def click(self, event):
#         x, y = pygame.mouse.get_pos()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if pygame.mouse.get_pressed()[0]:
#                 if self.rect.collidepoint(x, y):
#                     self.change_text(self.feedback, bg="red")

# start_button= Button(
#     "Click here",
#     (100, 100),
#     font=30,
#     bg="navy",
#     feedback="You clicked me")

    #-- Create the flag
def create_flag():
    flag = gameobjects.Flag(current_map.flag_position[0], current_map.flag_position[1])
    game_objects_list.append(flag)
    return flag


   
def collision_bullet_box(arb,space,data):
    bullet = arb.shapes[0]
    box  = arb.shapes[1]
    if bullet and bullet.parent in bullet_list:
        box.parent.health -= 1
        space.remove(bullet, bullet.body) 
        bullet_list.remove(bullet.parent)
        if box.parent.destructable == True:
            if box.parent.health == 0:
                game_objects_list.remove(box.parent)
                space.remove(box, box.body)
    return False

handler = space.add_collision_handler(1,3)
handler.pre_solve = collision_bullet_box

def collision_bullet_tank(arb, space, data): #Instead of removing tank mby teleport it back to spawn
    bullet = arb.shapes[0]
    tank = arb.shapes[1]

    if tank.parent.name != bullet.parent.owner:
        tank.parent.health -= 1
        if tank.parent.health == 0:
            tank.parent.respawn()
        if tank.parent.name != player_tank:
            ai_list.append(ai_creator(tank.parent))
        if tank.parent.flag == flag: 
            gameobjects.Tank.drop_flag(tank.parent, flag)
        if bullet.parent in bullet_list:
            space.remove(bullet, bullet.body)
            bullet_list.remove(bullet.parent)
    return False

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
                for tank in tanks_list:
                    for i in range(len(tanks_list)):
                        print(f"Player {i +1}: {tank.points}")
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


        #-- Update physics
        if skip_update == 0:
            #  Loop over all the game objects and update their speed in function of their
            # acceleration.
            for obj in game_objects_list:
                obj.update()
            skip_update = 3
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
                tank.points = tank.points + 1
                for tank in tanks_list:
                    for i in range(len(tanks_list)):
                        print(f"Player {i +1}: {tank.points}")
                #running = False
        
        #Ai update     
        for ai in ai_list:
            ai.decide()
        cooldown_tracker += 1

        
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
#main_menu()
#pygame.quit()
main_loop()
quit()
