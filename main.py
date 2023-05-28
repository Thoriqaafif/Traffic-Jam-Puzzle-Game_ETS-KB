# script utama tempat game dijalankan
# berisi game loop
import os
import time
import pygame
# Load our scenes
import game

g = game.Game()     # objek game

# jika game masih berjalan
# game terus melakukan update dan render
while g.running:
    while g.playing:
        g.update()
        g.render()