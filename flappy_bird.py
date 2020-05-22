from const import *
from typing import NoReturn, List, Tuple
import random
import neat
import pickle


class Bird:
    """"
    Object that represents Bird
    """
    __IMAGES__: List[pygame.Surface] = BIRDS_ITEMS
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
        self.img: pygame.Surface = self.__IMAGES__[0]  # base position

    def jump(self) -> NoReturn:
        """"
        Makes bird jump
        """
        # Since in Pygame the coordinates starts from top left corner,
        # if we want to go down we add negative velocity
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self) -> NoReturn:
        """"
        Bird moving
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

    def draw(self, window: pygame.Surface) -> NoReturn:
        """"
        Draw bird
        :param window -
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

        rotated_image: pygame.Surface = pygame.transform.rotate(self.img, self.tilt)
        new_rect: pygame.Rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self) -> pygame.mask.Mask:
        """"
        Get bird mask
        """
        return pygame.mask.from_surface(self.img)


class Pipe:
    """"
    Class that represents pipe object
    """
    __GAP__ = 170
    __VELOCITY__ = 7

    def __init__(self, x):
        self.x: int = x
        self.height: int = 0
        self.top: int = 0

        self.bottom: int = 0

        self.pipe_top: pygame.Surface = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.pip_bottom: pygame.Surface = PIPE_IMAGE

        self.passed: bool = False  # collision
        self.set_height()

    def set_height(self) -> NoReturn:
        """"
        Set pipe height
        """
        self.height = random.randrange(50, 600)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.__GAP__

    def move(self) -> NoReturn:
        """"
        Move pipe
        """
        self.x -= self.__VELOCITY__

    def draw(self, win: pygame.Surface) -> NoReturn:
        """"
        Draw pipe
        :param win -
        """
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pip_bottom, (self.x, self.bottom))

    def collision(self, bird: Bird) -> bool:
        """"
        Function, that calculate collision between bird object and pipe object
        :param bird -
        """
        bird_mask: pygame.mask.Mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pip_bottom)
        top_offset: Tuple[int, int] = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset: Tuple[int, int] = (self.x - bird.x, self.bottom - round(bird.y))

        b_point: Tuple[int, int] = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point: Tuple[int, int] = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True

        return False


class Ground:
    """"
    Class that represents ground
    """
    __VELOCITY__: int = 5
    __WIDTH__: int = BASE_IMAGE.get_width()
    __IMG__: pygame.Surface = BASE_IMAGE

    def __init__(self, y):
        self.y: int = y
        self.x1: int = 0
        self.x2: int = self.__WIDTH__

    def move(self) -> NoReturn:
        """"
        Function that makes ground 'move'
        """
        self.x1 -= self.__VELOCITY__
        self.x2 -= self.__VELOCITY__

        if self.x1 + self.__WIDTH__ < 0:
            self.x1 = self.x2 + self.__WIDTH__

        if self.x2 + self.__WIDTH__ < 0:
            self.x2 = self.x1 + self.__WIDTH__

    def draw(self, win) -> NoReturn:
        """"
        Draw ground
        :param win
        """
        win.blit(self.__IMG__, (self.x1, self.y))
        win.blit(self.__IMG__, (self.x2, self.y))


def draw_window(
        win: pygame.Surface,
        birds: List[Bird],
        pipes: List[Pipe],
        base: Ground,
        score: int,
        gen: int) -> NoReturn:

    """"
    Function, that draw game window and all game object
    :param win - game window
    :param birds - list of birds object
    :param pipes - list of pipes object
    :param base - ground object
    :param score - score counter
    :param gen - generation counter
    """
    win.blit(BG_IMAGE, (0, 0))

    for pipe in pipes:  # type: Pipe
        pipe.draw(win)
    text: pygame.Surface = STAT_FONT.render(f"Score: {str(score)}", 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text: pygame.Surface = STAT_FONT.render(f"Generation: {str(gen)}", 1, (255, 255, 255))
    win.blit(text, (10, 10))

    base.draw(win)

    for bird in birds:  # type: Bird
        bird.draw(win)

    pygame.display.update()


def main(genomes: List[Tuple], config: neat.config.Config) -> NoReturn:
    """"
    Main game function
    :param genomes -
    :param config -
    """
    global GEN
    GEN += 1

    nets: List[neat.nn.feed_forward.FeedForwardNetwork] = []
    ge: List[neat.genome.DefaultGenome] = []
    birds: List[Bird] = []

    for _, g in genomes:
        net: neat.nn.feed_forward.FeedForwardNetwork = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(200, 350))
        g.fitness = 0
        ge.append(g)

    base: Ground = Ground(730)
    pipes: List[Pipe] = [Pipe(700)]
    win: pygame.Surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    score: int = 0
    clock = pygame.time.Clock()

    game_running: bool = True
    while game_running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()
                quit()

        pipe_ind: int = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_ind = 1
        else:
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output: List[float] = nets[x].activate(
                (
                    bird.y,
                    abs(bird.y - pipes[pipe_ind].height),
                    abs(bird.y - pipes[pipe_ind].bottom)
                 )
            )

            if output[0] > 0.5:
                bird.jump()

        rem: List[Pipe] = []
        add_pipe: bool = False
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collision(bird):
                    # ge[x].fitness = -1 Uncomment it if you want to encourage fitness function
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.pipe_top.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() > 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)


def run(file: str) -> NoReturn:
    """"
    Run experiment
    :param file
    """
    config: neat.config.Config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
        file
    )

    population: neat.population.Population = neat.Population(config)

    # detail statistics
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    winner: neat.genome.DefaultGenome = population.run(main, 50)
    create_best_bird(winner)


def create_best_bird(winner: neat.genome.DefaultGenome) -> NoReturn:
    """"
    :param winner - best bird in population
    """
    # Save the winner.
    with open('winner-ctrnn', 'wb') as f:
        pickle.dump(winner, f)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config.txt')
    run(config_file)
