import os
import time
import pygame
# Load our scenes
import game

g = game.Game()
while g.running:
    g.game_loop()
