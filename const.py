""""
Module contains contant variables for project
"""

import pygame
import os

pygame.font.init()

WIN_WIDTH: int = 500
WIN_HEIGHT: int = 800
GEN: int = 0
bird_list = ["bird1.png", "bird2.png", "bird3.png"]

BIRDS_ITEMS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", item))) for item in bird_list]
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

