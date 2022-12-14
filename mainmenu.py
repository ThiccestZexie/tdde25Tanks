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
                        main_loop()
                    if selected == "map1":
                        current_map = maps.map1
                    if selected == "map2":
                        current_map = maps.map2
                    if selected == "map3":
                        current_map = maps.map3
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
