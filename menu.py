import pygame
import pymunk
import os
import math

import images
import maps
class Main_menu_creator:

    def __init__(self, settings, framerate, screen):
        self.settings = settings
        self.framerate = framerate
        self.clock  = pygame.time.Clock()
        self.screen = screen
        self.map_list = [maps.map0, maps.map1, maps.map2]
        self.current_map = self.map_list[0]
        self.create_menu()


    def create_menu(self):
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
        font = "data/font/Super Funky.ttf"


        # Game Resolution
        screen_width =  self.current_map.rect().size[0]
        screen_height= self.current_map.rect().size[1]
        bg = pygame.image.load("data/grass.png").convert()
        self.screen=pygame.display.set_mode(self.current_map.rect().size)
        # screen resolution 
        res = (screen_width,screen_height)

        # Text Renderer
        def text_format(message, textFont, textSize, textColor):
            newFont=pygame.font.Font(textFont, textSize)
            newText=newFont.render(message, 0, textColor)
            return newText


        def main_menu():
        
            menu=True
            selected="start"
            indexlist= 0
            map_index = 0
            while menu:
                for event in pygame.event.get():
                    if event.type== pygame.QUIT:
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
                            elif indexlist == 3:
                                selected = "map"
                            
                        if event.key==pygame.K_RETURN:
                            if selected=="start":
                                menu = False
                            if selected=="quit":
                                menu = False
                                pygame.quit()
                            if selected == "hot_seat":
                                if self.settings.hot_seat_multiplayer == False:
                                    self.settings.hot_seat_multiplayer = True
                                else:
                                    self.settings.hot_seat_multiplayer = False
                            if selected == "map":
                                map_index += 1
                                if map_index == 3:
                                    map_index = 0
                                self.settings.current_map = self.map_list[map_index]
                       # Main Menu UI
                font_size = math.floor(screen_width/10)
                self.screen.fill(gray)
                self.screen.blit(pygame.transform.scale(images.grass, (screen_width, screen_height)), (0, 0))
                title= text_format("CTF", font, font_size, yellow)
                if  selected =="start":
                    text_start=text_format("START", font, font_size -5, white)
                else:
                    text_start = text_format("START", font, font_size -5, black)
                if  selected =="quit":
                    text_quit=text_format("QUIT", font, font_size -5, white)
                else:
                    text_quit = text_format("QUIT", font, font_size -5, black)    
                if  selected == "hot_seat":
                    if  self.settings.hot_seat_multiplayer == True:
                        text_hot_seat = text_format("hot_seat: on", font, font_size -5, white)
                    else:
                        text_hot_seat = text_format("hot_seat: off", font, font_size -5, white)
                else:
                    if self.settings.hot_seat_multiplayer == True:
                        text_hot_seat = text_format("hot_seat: on", font, font_size -5, black)
                    else:
                        text_hot_seat = text_format("hot_seat: off", font, font_size -5, black)
                if selected == "map":
                    if  self.settings.current_map == maps.map0:
                        text_map = text_format("Map 1", font, font_size -5, white)
                    elif self.settings.current_map == maps.map1:
                        text_map = text_format("Map 2", font, font_size -5, white)
                    elif self.settings.current_map == maps.map2:
                        text_map = text_format("Map 3", font, font_size -5, white)
                else:
                    if  self.settings.current_map == maps.map0:
                        text_map = text_format("Map 1", font, font_size -5, black)
                    elif self.settings.current_map == maps.map1:
                        text_map = text_format("Map 2", font, font_size -5, black)
                    elif self.settings.current_map == maps.map2:
                        text_map = text_format("Map 3", font, font_size -5, black)
                    
                title_rect=title.get_rect()
                start_rect=text_start.get_rect()
                quit_rect=text_quit.get_rect()
                text_hot_seat_rect = text_hot_seat.get_rect()
                text_map_rect = text_map.get_rect()

                self.screen.blit(title, (screen_width/2 - (title_rect[2]/2), 20))
                self.screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), math.floor(screen_height/6)))
                self.screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), (screen_height/6 + screen_height/2)/2))
                self.screen.blit(text_hot_seat, (screen_width/2 - (text_hot_seat_rect[2]/2), screen_height/2))
                self.screen.blit(text_map, (screen_width/2 - (text_map_rect[2]/2), (screen_height/2) + text_map.get_height()))


                
                pygame.display.update()
                self.clock.tick(self.framerate)
                pygame.display.set_caption("Main Menu Selection")

        main_menu()


