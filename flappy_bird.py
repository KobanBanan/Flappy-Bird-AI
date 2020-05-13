import pygame
import neat
import time
import os
import random

from const import *


class Bird:
    """"
    Object that represents Flappy Bird
    """
    __IMAGES__ = BIRDS_ITEMS  # TODO type
    __MAX_ROTATION__: int = 25  # How much bird is going to  tilt
    __ROT_VEL__: int = 20
    __ANIMATION_TIME__: int = 5

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.tilt: int = 0
        self.tick_count: int = 0
        self.velocity: int = 0
        self.height: int = self.y
        self.img_count: int = 0
        self.img = self.__IMAGES__[0]  # base position

    def jump(self):
        """"
        Makes bird jump
        """
        # Since in Pygame the coordinates starts from top left corner, if we want to go down we add negative velocity
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """"
        Moving
        """
        self.tick_count += 1

        # - 10.5 + 1.5 = till zero
        d: int = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.__MAX_ROTATION__:
                self.tilt = self.__MAX_ROTATION__
        else:
            if self.tilt > -90:
                self.tilt -= self.__ROT_VEL__

    def draw(self, window):
        """"
        :param window
        """
        self.img_count += 1

        if self.img_count < self.__ANIMATION_TIME__:
            self.img = self.__IMAGES__[0]
        elif self.img_count < self.__ANIMATION_TIME__ * 2:
            self.img = self.__IMAGES__[1]
        elif self.img_count < self.__ANIMATION_TIME__ * 3:
            self.img = self.__IMAGES__[2]
        elif self.img_count < self.__ANIMATION_TIME__ * 4:
            self.img = self.__IMAGES__[1]
        elif self.img_count == self.__ANIMATION_TIME__ * 4 + 1:
            self.img = self.__IMAGES__[0]
            self.img_count = 0

        if self.tilt <= - 80:
            self.img = self.__IMAGES__[1]
            self.img_count = self.__ANIMATION_TIME__ * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def draw_window(win, bird):
    win.blit(BG_IMAGE,  (0, 0))
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(win, bird)

    pygame.quit()
    quit()

main()

