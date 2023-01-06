import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
from data import *
from images import *
from pygame import mixer
from pygame.mixer import Sound
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


#-- Constants
FRAMERATE = 60

#-- Variables
player_tank = 0
winning_amount = 5
time_in_seconds = 120 

#-- Options
hot_seat_multiplayer = False
#-- Fog of war only works without hot_seat_multiplayer
fog_of_war = False
unfair_ai = False
win_con_time = False
win_con_total_rounds = True
win_con_winning = False


#   Define the current level
current_map         = maps.map0
#   List of all game objects
game_objects_list   = []
tanks_list          = []
ai_list             = []
bullet_list         = []
explosion_list      = []

#-- Resize the screen to the size of the current level
screen = pygame.display.set_mode(current_map.rect().size)
#-- Generate the background
background = pygame.Surface(screen.get_size())



# fail = ('data/Fail.wav')
# pygame.mixer.init()
# background_music = pygame.mixer.music.load("data\Background.wav")
# pygame.mixer.music.set_volume(0.05)
# pygame.mixer.music.play(-1)
# hit_sound = Sound("data\Boom.wav")
# wood_sound = Sound("data\woodbreak.wav")



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
    if hot_seat_multiplayer == False:
        for i in range(1, len(current_map.start_positions)):
            inst_ai = ai_creator(tanks_list[i])
            ai_list.append(inst_ai)
    else: 
        for i in range(2, len(current_map.start_positions)):
            inst_ai = ai_creator(tanks_list[i])
            ai_list.append(inst_ai)
def print_points():
    for i in range(len(tanks_list)):
        print(f"Player {i+1}: {tanks_list[i].points}")

def ai_creator(tank):
    inst_ai = ai.Ai(tank, game_objects_list, tanks_list, space, current_map, unfair_ai, bullet_list)
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


def create_fog_of_war():
        screen_width, screen_height = screen.get_size()
        radius = min(screen_width, screen_height)
        fog_of_war = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        fog_of_war.fill((0, 0, 0))
        pygame.draw.circle(fog_of_war, (0,0,0, 100), (radius, radius), 150)
        fog_of_war_rect = fog_of_war.get_rect()
        fog_of_war_rect.center = physics_to_display(tanks_list[player_tank].body.position)

        # Draw the fog of war over the game screen
        screen.blit(fog_of_war, fog_of_war_rect)



def print_text(font_size, input_text, screen_pos):
    font = pygame.font.Font(None, font_size)
    display_text = font.render(str(input_text), 1, (255,0,0))
    screen.blit(display_text, screen_pos)
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
screen_width=  current_map.rect().size[0]
screen_height=current_map.rect().size[1]
# bg = pygame.image.load("data/backgroundimage.jpg").convert()
screen=pygame.display.set_mode(current_map.rect().size)
# screen resolution 
res = (screen_width,screen_height)

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
    return newText

def settings(hot_seat_multiplayer):
    hot_seat_multiplayer = True
    return hot_seat_multiplayer

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
                        selected = "hot_seat"

                    
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        menu = False

                    if selected=="quit":
                        menu = False
                        pygame.quit()
                    if selected == "hot_seat":
                        global hot_seat_multiplayer
                        if hot_seat_multiplayer == False:
                            hot_seat_multiplayer = True
                        else:
                            hot_seat_multiplayer = False

        # Main Menu UI
        font_size = math.floor(screen_width/10)
        screen.fill(gray)
        screen.blit(pygame.transform.scale(images.grass, (screen_width, screen_height)), (0, 0))
        title=text_format("CTF", font, font_size, yellow)
        if selected=="start":
            text_start=text_format("START", font, font_size -5, white)
        else:
            text_start = text_format("START", font, font_size -5, black)
        if selected=="quit":
            text_quit=text_format("QUIT", font, font_size -5, white)
        else:
            text_quit = text_format("QUIT", font, font_size -5, black)    
        if selected == "hot_seat":
            if hot_seat_multiplayer == True:
                text_hot_seat = text_format("hot_seat: on", font, font_size -5, white)
            else:
                text_hot_seat = text_format("hot_seat: off", font, font_size -5, white)
        else:
            if hot_seat_multiplayer == True:
                text_hot_seat = text_format("hot_seat: on", font, font_size -5, black)
            else:
                text_hot_seat = text_format("hot_seat: off", font, font_size -5, black)
        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
        text_hot_seat_rect = text_hot_seat.get_rect()

        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 20))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), math.floor(screen_height/6)))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), (screen_height/6 + screen_height/2)/2))
        screen.blit(text_hot_seat, (screen_width/2 - (text_hot_seat_rect[2]/2), screen_height/2))
        pygame.display.update()
        clock.tick(FRAMERATE)
        pygame.display.set_caption("Main Menu Selection")
        
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

#   Copy the grass tile all over the level area
def create_grass():
    for x in range(0, current_map.width):
        for y in range(0,  current_map.height):
            # The call to the function "blit" will copy the image
            # contained in "images.grass" into the "background"
            # image at the coordinates given as the second argument
            background.blit(images.grass,  (x*images.TILE_SIZE, y*images.TILE_SIZE))


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
                # wood_sound.set_volume(0.05)
                # wood_sound.play()
                explosion_object = gameobjects.Explosion(explosion, box.parent.body.position)
                game_objects_list.append(explosion_object)
                game_objects_list.remove(box.parent)
                space.remove(box, box.body)
    return False

handler = space.add_collision_handler(1,3)
handler.post_solve = collision_bullet_box

def collision_bullet_tank(arb, space, data): #Instead of removing tank mby teleport it back to spawn
    bullet = arb.shapes[0]
    tank = arb.shapes[1]

    if tank.parent.name != bullet.parent.owner:
        if tank.parent.protection_timer == 0:
            tank.parent.health -= 1
        if tank.parent.health == 0:
            explosion_object = gameobjects.Explosion(explosion, tank.parent.body.position)
            game_objects_list.append(explosion_object) # När tanken dör läggs en explosion till
            # hit_sound.play( )
            tank.parent.respawn(flag)
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

def player_1(event):
        
    if event.type == KEYDOWN:
        if event.key == K_UP:
            tanks_list[player_tank].accelerate() 

        elif event.key == K_DOWN:
            tanks_list[player_tank].decelerate()

        elif event.key == K_LEFT:
            tanks_list[player_tank].turn_left()

        elif event.key == K_RIGHT:
            tanks_list[player_tank].turn_right()
        elif event.key == K_SPACE:
            if tanks_list[player_tank].cooldown_tracker >= 60:
                bullet_list.append(tanks_list[player_tank].shoot(space))

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


def player_2(event):
    if event.type == KEYDOWN:
        if event.key == K_w:
            tanks_list[player_2_tank].accelerate() 

        elif event.key == K_s:
            tanks_list[player_2_tank].decelerate()

        elif event.key == K_a:
            tanks_list[player_2_tank].turn_left()

        elif event.key == K_d:
            tanks_list[player_2_tank].turn_right()
        elif event.key == K_LSHIFT:
            if tanks_list[player_2_tank].cooldown_tracker >= 60:
                bullet_list.append(tanks_list[player_2_tank].shoot(space))
                
        

    if event.type == KEYUP:
        if event.key == K_w:
            tanks_list[player_2_tank].stop_moving() 
            tanks_list[player_2_tank].stop_turning()

        elif event.key == K_s:
            tanks_list[player_2_tank].stop_moving() 
            tanks_list[player_2_tank].stop_turning()

        elif event.key == K_a:
            tanks_list[player_2_tank].stop_turning()

        elif event.key == K_d:
            tanks_list[player_2_tank].stop_turning()  
#----- Main Loop -----#
def main_loop():
    running = True 
    skip_update = 0
    time_limit =  time_in_seconds* FRAMERATE
    total_rounds = 0
    max_rounds = 12

    while running:
     
        #-- Handle the events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type ==  KEYDOWN:
                if event.key == K_ESCAPE:
                    print_points()
                    running = False
                    break
            if hot_seat_multiplayer == True:
                player_1(event)
                player_2(event)
            elif hot_seat_multiplayer == False:
                player_1(event)


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

        for explosion in game_objects_list:
            if isinstance(explosion, Explosion):
                if explosion.tracker == 20:
                    game_objects_list.remove(explosion)
                explosion.tracker += 1
    
        
        #-- Checks for tanks
        for tanks in tanks_list:
            if win_con_winning == True:
                print_text(24,f"{tanks.points}/{winning_amount}", physics_to_display(tanks.start_position))
            if win_con_winning == False:
                print_text(24,tanks.points, physics_to_display(tanks.start_position))

            tanks.try_grab_flag(flag) 
            tanks.cooldown_tracker += 1
            if tanks.has_won() == True:
                tanks.points += 1
                total_rounds += 1
                if tanks.points == winning_amount and win_con_winning == True:  # possibly present the winner in a cool way.
                    running = False
                if total_rounds == max_rounds and win_con_total_rounds == True:
                    running = False
                tanks.respawn(flag)
                flag.x = current_map.flag_position[0]
                flag.y = current_map.flag_position[1]                
            if tanks.protection_timer > 0:
                tanks.protection_timer -= 1/FRAMERATE
                if tanks.protection_timer < 0:
                    tanks.protection_timer = 0
        #Ai update     
        for ai in ai_list:
            ai.decide()  

        if not hot_seat_multiplayer and fog_of_war == True: 
            create_fog_of_war()
        #-- Display text that updates.
        #win con rounds go out
        if win_con_total_rounds == True:
            print_text(40, (f"{total_rounds}/{max_rounds}"), (screen_width/2 ,5))

        #Win con timer
        if win_con_time == True:
            print_text(40, math.floor(time_limit/60), (screen_width/2,5))
            if time_limit <= 0:
                running = False
            time_limit -= 1

          
        #   Redisplay the entire screen (see double buffer technique)
        pygame.display.flip()
        #   Control the game framerate
        clock.tick(FRAMERATE)

main_menu()
if hot_seat_multiplayer == True:
    player_2_tank = 1

create_grass()
create_boxes()
create_bases()
create_tanks()
create_out_of_bounds()
flag = create_flag()
main_loop()
quit()
