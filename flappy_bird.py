import pygame
import random

from const import *

pygame.font.init()


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


class Pipe:
    """"
    Class that represents pipe object
    """
    __GAP__ = 20
    __VELOCITY__ = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0

        self.bottom = 0

        self.pipe_top = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.pip_bottom = PIPE_IMAGE

        self.passed = False  # collision
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.__GAP__

    def move(self):
        self.x -= self.__VELOCITY__

    def draw(self, win):
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pip_bottom, (self.x, self.bottom))

    def collision(self, bird):
        """"

        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pip_bottom)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True

        return False


class Base:
    """"
    Class that represents ground
    """
    __VELOCITY__ = 5
    __WIDTH__ = BASE_IMAGE.get_width()
    __IMG__ = BASE_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.__WIDTH__

    def move(self):
        """"
        """
        self.x1 -= self.__VELOCITY__
        self.x2 -= self.__VELOCITY__

        if self.x1 + self.__WIDTH__ < 0:
            self.x1 = self.x2 + self.__WIDTH__

        if self.x2 + self.__WIDTH__ < 0:
            self.x2 = self.x1 + self.__WIDTH__

    def draw(self, win):
        """"

        """
        win.blit(self.__IMG__, (self.x1, self.y))
        win.blit(self.__IMG__, (self.x2, self.y))


def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMAGE, (0, 0))

    for pipe in pipes:
        pipe.draw(win)
    text = STAT_FONT.render(f"Score: {str(score)}", 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    base.draw(win)

    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    score = 0
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        rem = []
        # bird.move()
        add_pipe = False
        for pipe in pipes:
            if pipe.collision(bird):
                pass

            if pipe.x + pipe.pipe_top.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() > 730:
            pass

        base.move()
        draw_window(win, bird, pipes, base, score)

    pygame.quit()
    quit()


main()
