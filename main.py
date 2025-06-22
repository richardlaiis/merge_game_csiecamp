import pygame
from sys import exit, argv
from random import randint, choice

mode = 0
if len(argv) != 2:
    print('Usage: python3 main.py [1-5]')
    exit(1)
else:
    mode = int(argv[1])



pygame.init()
screen = pygame.display.set_mode((1800, 1400))
pygame.display.set_caption('Merging Game')
clock = pygame.time.Clock()

# 草地背景
bg_surface = pygame.image.load('images/grass.png')
bg_surface = pygame.transform.scale(bg_surface, (1800, 1400))

# 背景音樂
bg_music = pygame.mixer.Sound('audio/theme.mp3')
bg_music.set_volume(0.5)
bg_music.play(loops = -1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(bg_surface, (0, 0))
    pygame.display.update()
    clock.tick(60)