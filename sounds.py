
from pygame import mixer
import pygame
import os
main_dir = os.path.split(os.path.abspath(__file__))[0]
def backgroundmusic():
    file = os.path.join(main_dir, 'data.py', 'Background.wav')
    mixer.init()
    mixer.music.load(file)
    mixer.music.play(-1)

def play(file):
    # mixer.init()
    sound = pygame.mixer.Sound(file)
    sound.play()


# sounds.play("fslip.wav")