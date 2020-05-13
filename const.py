""""
Module contains contant variables for project
"""

import pygame
import os

WIN_WIDTH = 500
WIN_HEIGHT = 800

bird_list = ["bird1.png", "bird2.png", "bird3.png"]

BIRDS_ITEMS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", item))) for item in bird_list]
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))