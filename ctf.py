import pygame
from pygame.locals import *
from pygame.color import *
import pymunk

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

#-- Constants
FRAMERATE = 50

#-- Variables
#   Define the current level
current_map         = maps.map0
#   List of all game objects
game_objects_list   = []
tanks_list          = []
flags_list          = []
bases_list          = []

#-- Resize the screen to the size of the current level
screen = pygame.display.set_mode(current_map.rect().size)

#-- Generate the background
background = pygame.Surface(screen.get_size())

#   Copy the grass tile all over the level area
for x in range(0, current_map.width):
    for y in range(0,  current_map.height):
        # The call to the function "blit" will copy the image
        # contained in "images.grass" into the "background"
        # image at the coordinates given as the second argument
        background.blit(images.grass,  (x*images.TILE_SIZE, y*images.TILE_SIZE))

#-- Create the boxes
for x in range(0, current_map.width):
    for y in range(0,  current_map.height):
        # Get the type of boxes
        box_type  = current_map.boxAt(x, y)
        # If the box type is not 0 (aka grass tile), create a box
        if(box_type != 0):
            # Create a "Box" using the box_type, aswell as the x,y coordinates,
            # and the pymunk space
            box = gameobjects.get_box_with_type(x, y, box_type, space)


#-- Create the tanks
# Loop over the starting poistion
for i in range(0, len(current_map.start_positions)):
    # Get the starting position of the tank "i"
    pos = current_map.start_positions[i]
    # Create the tank, images.tanks contains the image representing the tank
    tank = gameobjects.Tank(pos[0], pos[1], pos[2], images.tanks[i], space)
    # Add the tank to the list of tanks
    tanks_list.append(tank)
    game_objects_list.append(tank)

 #-- Create the bases
for i in range(0,len(current_map.start_positions)):   
    pos_base = current_map.start_positions[i]
    bases = gameobjects.GameVisibleObject(pos_base[0], pos_base[1], images.bases[i])
    game_objects_list.append(bases)

 #-- Create out of bound walls
body = pymunk.Body(body_type=pymunk.Body.STATIC)
walls = pymunk.Segment(body, (0,current_map.height), (0, current_map.width), 0)
walls_list.append(walls)   


#<INSERT CREATE FLAG>
#-- Create the flag
flag = gameobjects.Flag(current_map.flag_position[0], current_map.flag_position[1])


#----- Main Loop -----#

#-- Control whether the game run
running = True

skip_update = 0

while running:
    #-- Handle the events
    for event in pygame.event.get():
        # Check if we receive a QUIT event (for instance, if the user press the
        # close button of the wiendow) or if the user press the escape key.
        
        #Tank[0] is the player tank
        if event.type == QUIT:
            running = False
        
        if event.type ==  KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            elif event.key == K_UP:
                tanks_list[0].accelerate() 

            elif event.key == K_DOWN:
                tanks_list[0].decelerate()

            elif event.key == K_LEFT:
                tanks_list[0].turn_left()

            elif event.key == K_RIGHT:
                tanks_list[0].turn_right()
            

        if event.type == KEYUP:
            if event.key == K_UP:
                tanks_list[0].stop_moving() 
                tanks_list[0].stop_turning()

            elif event.key == K_DOWN:
                tanks_list[0].stop_moving() 
                tanks_list[0].stop_turning()

            elif event.key == K_LEFT:
                tanks_list[0].stop_turning()

            elif event.key == K_RIGHT:
                tanks_list[0].stop_turning()    

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
        obj.post_update()

    #-- Update Display

    # Display the background on the screen
    screen.blit(background, (0, 0))

    # Update the display of the game objects on the screen
    for obj in game_objects_list:
        obj.update_screen(screen)

    #Tank update
    for tank in tanks_list:
        tank.update_screen(screen)
    
    #Base update
    for bases in bases_list:
        bases.update_screen(screen)

    #Flag update
    for tanks in tanks_list:
        tanks.try_grab_flag(flag)

    flag.update_screen(screen)
    #Tank has won - only works with player tank

    if tanks_list[0].has_won() == True:
            break

    

    #   Redisplay the entire screen (see double buffer technique)
    pygame.display.flip()

    #   Control the game framerate
    clock.tick(FRAMERATE)
