import os
import time
import pygame
# Load our scenes
import game

g = game.Game()
while g.running:
    g.game_loop()

# pygame.init()
# screen=pygame.display.set_mode((800,600))

# color=(200,0,0)
# screen.fill(color,pygame.Rect(30,30,60,60))
# # pygame.draw.rect(screen,color,pygame.Rect(30,30,60,60))
# pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
# pygame.mouse.set_cursor(pygame.cursors.arrow)
# pygame.display.flip()

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()