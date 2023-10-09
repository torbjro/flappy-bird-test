import pygame, random, time
from pygame.locals import *

#VARIABLES, can be adjusted
SCREEN_WIDHT = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDHT = 2 * SCREEN_WIDHT
GROUND_HEIGHT= 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150


class Bird(pygame.sprite.Sprite):
    """
    class for the bird
    """
    def __init__(self):
        """
        initializing bird with images, speed and rectangel around bird
        """
        # init sprite
        pygame.sprite.Sprite.__init__(self)
        # loading images for upflap, midflap and downflap
        self.images =  [pygame.image.load('flappy-bird-test/images/bluebird-upflap.png').convert_alpha(),
                        pygame.image.load('flappy-bird-test/images/bluebird-midflap.png').convert_alpha(),
                        pygame.image.load('flappy-bird-test/images/bluebird-downflap.png').convert_alpha()]
        # setting speed
        self.speed = SPEED
        # start image
        self.current_image = 0
        self.image = pygame.image.load('flappy-bird-test/images/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        # initialize rectangel
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        """
        method for updating bird image
        """
        # new image, updates flap if needed
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        # speed of bird is gravity
        self.speed += GRAVITY
        #updating height
        self.rect[1] += self.speed

    def bump(self):
        # flap the bird
        self.speed = -SPEED

    def begin(self):
        # starting the bird
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]


class Pipe(pygame.sprite.Sprite):
    """
    class for the pipes
    """
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        # loading image of pipe and scaling it
        self. image = pygame.image.load('flappy-bird-test/images/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))
        # set rect for pipe
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        # either up or down
        if inverted:
            # flip image if inverted
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            # not inverted
            self.rect[1] = SCREEN_HEIGHT - ysize
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        # update pipe position
        self.rect[0] -= GAME_SPEED

        

class Ground(pygame.sprite.Sprite):
    """
    class for setting the ground
    """
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        # load image and transform
        self.image = pygame.image.load('flappy-bird-test/images/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        # set rect with correct position
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        # update the ground position
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    # checking if the sprite/image is off the screen
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    """
    method for creating random pipes
    returns both the pipe and inverted pipe
    """
    size = random.randint(100, 300)
    # not inverted pipe
    pipe = Pipe(False, xpos, size)
    # inverted pipe
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted

class Game():
    def __init__(self):
        self.score = 0
    
    def start(self):
        # initialize game and display
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        # loading and transforming background and start screen
        BACKGROUND = pygame.image.load('flappy-bird-test/images/background-day.png')
        BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
        BEGIN_IMAGE = pygame.image.load('flappy-bird-test/images/message.png').convert_alpha()
        # init the bird
        bird_group = pygame.sprite.Group()
        bird = Bird()
        bird_group.add(bird)
        # init the ground
        ground_group = pygame.sprite.Group()
        for i in range (2):
            ground = Ground(GROUND_WIDHT * i)
            ground_group.add(ground)
        # init the pipes (both inverted and regular)
        pipe_group = pygame.sprite.Group()
        for i in range (2):
            pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])
        # start clock
        clock = pygame.time.Clock()
        begin = True
        # loop driving background while waiting to start
        while begin:
            # updating clock
            clock.tick(15)
            # registering events in game
            for event in pygame.event.get():
                # stop game if quit
                if event.type == QUIT:
                    pygame.quit()
                # starting game
                if event.type == KEYDOWN:
                    # starting the game on space or up, breaking out of the loop
                    if event.key == K_SPACE or event.key == K_UP:
                        bird.bump()
                        begin = False
            # updating display with start display
            screen.blit(BACKGROUND, (0, 0))
            screen.blit(BEGIN_IMAGE, (120, 150))
            # updating the ground
            if is_off_screen(ground_group.sprites()[0]):
                ground_group.remove(ground_group.sprites()[0])
                # new ground
                new_ground = Ground(GROUND_WIDHT - 20)
                ground_group.add(new_ground)
            # continue the bird
            bird.begin()
            ground_group.update()
            # update
            bird_group.draw(screen)
            ground_group.draw(screen)
            # update the display
            pygame.display.update()
        self.game(clock,screen,bird, BACKGROUND, ground_group, pipe_group, bird_group)
    
    def game(self, clock, screen, bird, BACKGROUND, ground_group, pipe_group, bird_group):
        # loop driving the game when it starts
        while True:
            # updating clock
            clock.tick(15)
            # register keys
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    # flapping the bird
                    if event.key == K_SPACE or event.key == K_UP:
                        bird.bump()
            # updating the background
            screen.blit(BACKGROUND, (0, 0))
            # if new ground is required
            if is_off_screen(ground_group.sprites()[0]):
                ground_group.remove(ground_group.sprites()[0])
                new_ground = Ground(GROUND_WIDHT - 20)
                ground_group.add(new_ground)
            # if new pipes are needed
            if is_off_screen(pipe_group.sprites()[0]):
                pipe_group.remove(pipe_group.sprites()[0])
                pipe_group.remove(pipe_group.sprites()[0])
                # updating score when passing a pipe
                self.score += 1
                # get the new pipes
                pipes = get_random_pipes(SCREEN_WIDHT * 2)
                pipe_group.add(pipes[0])
                pipe_group.add(pipes[1])
            # updating bird, ground and pipes
            bird_group.update()
            ground_group.update()
            pipe_group.update()
            # draw the updates and update display
            bird_group.draw(screen)
            pipe_group.draw(screen)
            ground_group.draw(screen)
            pygame.display.update()
            # if collision with ground or pipe, break the loop
            if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                    pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
                time.sleep(1)
                break
        self.new_round(self.score)
    
    def new_round(self, prev_score):
        # score text
        font = pygame.font.Font('flappy-bird-test/FlappyFont.ttf', 50)
        string = 'Score: '
        string += str(prev_score)
        text = font.render(string, True, (255, 255, 255))
        #text_rect = text.get_rect()
        # new menu, resetting game
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        BACKGROUND = pygame.image.load('flappy-bird-test/images/background-day.png')
        BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
        BEGIN_IMAGE = pygame.image.load('flappy-bird-test/images/message.png').convert_alpha()
        bird_group = pygame.sprite.Group()
        bird = Bird()
        bird_group.add(bird)
        ground_group = pygame.sprite.Group()
        for i in range (2):
            ground = Ground(GROUND_WIDHT * i)
            ground_group.add(ground)
        pipe_group = pygame.sprite.Group()
        for i in range (2):
            pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])
        clock = pygame.time.Clock()
        begin = True
        # loop driving background while waiting to start
        while begin:
            # updating clock
            clock.tick(15)
            # registering events in game
            for event in pygame.event.get():
                # stop game if quit
                if event.type == QUIT:
                    pygame.quit()
                # starting game
                if event.type == KEYDOWN:
                    # starting the game on space or up, breaking out of the loop
                    if event.key == K_SPACE or event.key == K_UP:
                        bird.bump()
                        begin = False
            # updating display with start display
            screen.blit(BACKGROUND, (0, 0))
            screen.blit(BEGIN_IMAGE, (120, 150))
            screen.blit(text, (130, 110))
            # updating the ground
            if is_off_screen(ground_group.sprites()[0]):
                ground_group.remove(ground_group.sprites()[0])
                # new ground
                new_ground = Ground(GROUND_WIDHT - 20)
                ground_group.add(new_ground)
            # continue the bird
            bird.begin()
            ground_group.update()
            # update
            bird_group.draw(screen)
            ground_group.draw(screen)
            # update the display
            pygame.display.update()
        # reset game
        self.score = 0
        self.game(clock, screen, bird, BACKGROUND, ground_group, pipe_group, bird_group)

# driver code
if __name__ == '__main__':
    # starting game
    game = Game()
    game.start()