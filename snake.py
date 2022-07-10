import pygame
from pygame.locals import *
import random

pygame.init()

# create the game screen
width = 480
height = 480
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Snake Game')

# grid variables
grid_size = 20
num_rows = width // grid_size
num_cols = height // grid_size

# directions
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

# colors
black = (0, 0, 0)
blue = (25, 103, 181)
dark_green = (67, 160, 71)
light_green = (129, 199, 132)
red = (200, 0, 0)
white = (255, 255, 255)

# game variables
score = 0
gameover = False

# game clock
clock = pygame.time.Clock()
fps = 10

class Apple:
    
    def __init__(self):
        self.randomize_location()
        
    def randomize_location(self):
        random_x = random.randint(0, num_cols - 1) * grid_size
        random_y = random.randint(0, num_rows - 1) * grid_size
        self.location = (random_x, random_y)
        
    def draw(self):
        square = pygame.Rect(self.location, (grid_size, grid_size))
        pygame.draw.rect(screen, red, square)
        
class Snake:
    
    def __init__(self):
        self.body = [(width / 2, height / 2)]
        self.direction = right
        self.head = self.body[0]
        
    def turn(self, direction):
        
        # snake can move in any direction if length is 1
        if len(self.body) == 1:
            self.direction = direction
        else:
            
            # if turning left or right, ensure that
            # the first two body parts are not in the same y position
            if direction == left or direction == right:
                if self.body[0][1] != self.body[1][1]:
                    self.direction = direction
                    
            # if turning up or down, ensure that
            # the first two body parts are not in the same x position
            if direction == up or direction == down:
                if self.body[0][0] != self.body[1][0]:
                    self.direction = direction
        
        
    def move(self):
        
        # determine the head's next location
        x, y = self.direction
        next_x = (self.head[0] + x * grid_size)
        next_y = (self.head[1] + y * grid_size)
        
        # if next location hits a wall, wrap to the opposite wall
        next_x = next_x % width
        next_y = next_y % height
        next_location = (next_x, next_y)
        
        # add new head location to front of list
        self.body.insert(0, next_location)
        self.head = self.body[0]
        
        # check if apple is at the head's location
        if self.head == apple.location:
            
            # move the apple to another location
            apple.randomize_location()
            
            # make sure the apple's new location is not where the snake is
            while apple.location in self.body:
                apple.randomize_location()
                
        else:
            
            # remove the last body part from list
            self.body.pop()
        
    def check_collision(self):
        
        # check if head collided with a body part
        if self.head in self.body[1:]:
            return True
        else:
            return False
        
        
    def draw(self):
        for body_part in self.body:
            square = pygame.Rect(body_part, (grid_size, grid_size))
            pygame.draw.rect(screen, blue, square)
            pygame.draw.rect(screen, white, square, 1)

# create the apple
apple = Apple()

# create the snake
snake = Snake()
        
# game loop
running = True
while running:
    
    clock.tick(fps)
    
    # check for event actions
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            
            # use arrow keys to turn the snake
            if event.key == K_UP:
                snake.turn(up)
            elif event.key == K_DOWN:
                snake.turn(down)
            elif event.key == K_LEFT:
                snake.turn(left)
            elif event.key == K_RIGHT:
                snake.turn(right)
    
    # draw the background
    for x in range(num_cols):
        for y in range(num_rows):
            
            # create a single square for the grid
            square = pygame.Rect((x * grid_size, y * grid_size), (grid_size, grid_size))
            
            # alternate colors for a checkered background
            if (x + y) % 2 == 0:
                pygame.draw.rect(screen, dark_green, square)
            else:
                pygame.draw.rect(screen, light_green, square)
        
    # draw the apple
    apple.draw()
    
    # move the snake
    snake.move()
    
    # draw the snake
    snake.draw()
    
    # display the score
    font = pygame.font.SysFont('monoface', 16)
    text = font.render("Score: {0}".format(len(snake.body)), 1, black)
    screen.blit(text, (5, 10))
    
    # check for collision
    collision = snake.check_collision()
    if collision:
        gameover = True
        
    # gameover state
    while gameover:
        
        clock.tick(fps)
        
        # draw the gameover text
        pygame.draw.rect(screen, black, (0, height / 2 - 50, width, 100))
        text = font.render("Game over! Press SPACE to play again", 1, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, height / 2)
        screen.blit(text, text_rect)
        pygame.display.update()
        
        # check if the user exited or pressed the space bar
        for event in pygame.event.get():
            
            if event.type == QUIT:
                gameover = False
                running = False
                
            elif event.type == KEYDOWN and event.key == K_SPACE:
                
                # reset the game
                gameover = False
                score = 0
                snake.body = [(width / 2, height / 2)]
                snake.direction = right
                snake.head = snake.body[0]
                apple.randomize_location()
            
    pygame.display.update()
    
pygame.quit()