import pygame
import random
import numpy as np
from enum import Enum

pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
fps = 20
zoom = 16

BLACK = (0,0,0)
GRAY = (128,128,128)
GREEN = (0,255,0)
BLUE = (0,0,255)

class States(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    ALIVE = 5
    DEAD = 6
    GAMEOVER = 7
    RUNNING = 8

class Snake():
    def __init__(self,width,height):
        self.body = np.array([[25,25],[25,26]]) #snakes body points, first row is head last row is tail
        self.heading= States.LEFT #head heading direction
        self.width = width
        self.height = height
        self.state = States.ALIVE
        self.tail = self.body[-1] # safe for growing after feed
    def move(self):
        if self.heading == States.LEFT:
            dx = -1
            self.move_horizontal(dx)
        elif self.heading == States.RIGHT:
            dx = 1
            self.move_horizontal(dx)
        elif self.heading ==States.UP:
            dy = -1
            self.move_vertical(dy)
        elif self.heading ==States.DOWN:
            dy = 1
            self.move_vertical(dy)
    def head(self):
        return self.body[0].copy()
    def move_vertical(self,dy):
        new_head = self.head()
        new_head[0] += dy
        if self.hitwall(new_head) or self.hittail(new_head):
            self.state = States.DEAD
        else:
            self.body = np.concatenate((np.expand_dims(new_head,axis=0),self.body),axis=0)
            self.tail = self.body[-1]
            self.body = self.body[0:-1]
    def move_horizontal(self,dx):
        new_head = self.head()
        new_head[1] += dx
        if self.hitwall(new_head) or self.hittail(new_head):
            self.state = States.DEAD
        else:
            self.body = np.concatenate((np.expand_dims(new_head, axis=0), self.body), axis=0)
            self.tail = self.body[-1]
            self.body = self.body[0:-1]
    def hitwall(self,new_head):
        hit = False
        y,x = new_head
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            hit = True
        return hit

    def hittail(self,new_head):
        hit = False
        if new_head.tolist() in self.body.tolist():
            hit = True
        return hit
    def feed(self):
        self.body = np.concatenate((self.body,np.expand_dims(self.tail,axis=0)),axis=0)
class Food():
    def __init__(self,width,height):
        self.width = width
        self.height = height
    def blob_pos(self):
        return np.array([self.y(),self.x()])
    def x(self):
        return self.position[0]
    def y(self):
        return self.position[1]
    def spawn(self,field):
        choiceW,choiceH = range(0,self.width),range(0,self.height)

        while True:
            y = random.choice(choiceH)
            if np.count_nonzero(field[y]) < self.width:
                break
        while True:
            x = random.choice(choiceW)
            if np.count_nonzero(field[y,x]) == 0:
                break
        self.position =x,y
class Playground():
    state = States.RUNNING
    def __init__(self,width=50,height=50):
        self.width = width
        self.height = height
        self.field =np.zeros((height,width))


        self.spawnsnake()
        self.food = Food(self.width,self.height)
        self.spawnfood()
        self.score = len(self.snake.body)-2
    def spawnsnake(self):
        self.snake = Snake(self.width,self.height)
    def spawnfood(self):
        self.food.spawn(self.field)
    def timestep(self):
        self.snake.move()
        if (self.snake.head() == self.food.blob_pos()).all(): # if snakes head is on food, eat it
            self.snake.feed()
            self.spawnfood()
            self.score = len(self.snake.body) - 2 #update score
        self.field_upate()

        if self.snake.state == States.DEAD:
            self.state = States.GAMEOVER

    def up(self):
        if self.snake.heading != States.DOWN:
            self.snake.heading = States.UP
    def down(self):
        if self.snake.heading != States.UP:
            self.snake.heading = States.DOWN
    def left(self):
        if self.snake.heading != States.RIGHT:
            self.snake.heading = States.LEFT
    def right(self):
        if self.snake.heading != States.LEFT:
            self.snake.heading = States.RIGHT

    def field_upate(self):
        self.field = np.zeros((self.height, self.width))
        self.field[self.food.y(),self.food.x()] = 2
        for bodypart in self.snake.body:
            y,x = bodypart
            self.field[y,x] = 1
done = False
game = Playground()

while not done:
    if game.state == States.RUNNING:
        game.timestep()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.up()
            if event.key == pygame.K_DOWN:
                game.down()
            if event.key == pygame.K_LEFT:
                game.left()
            if event.key == pygame.K_RIGHT:
                game.right()

    screen.fill(color=BLACK)
    # draw fields

    for i,row in enumerate(game.field):
        for j,element in enumerate(row):
            if element == 0:
                just_border = 1
                color = GRAY
            if element == 1:
                just_border = 0
                color = GREEN
            if element == 2:
                just_border = 0
                color = BLUE
            pygame.draw.rect(screen,color,[j*zoom,i*zoom,zoom,zoom],just_border)

    gameoverf = pygame.font.SysFont('Calibri',25,True,False)
    gameovert = gameoverf.render('Game Over! :(',True,(255,215,0))

    if game.state == States.GAMEOVER:
        screen.blit(gameovert,[200,300])
    score_font = pygame.font.SysFont('Calibri',25,True,False)
    text_score = score_font.render('Score: '+str(game.score),True,(255,255,255))
    score_font.render('Score:' + str(game.score), True, (255, 255, 255))
    screen.blit(text_score,[30,0])
    pygame.display.flip()
    clock.tick(fps)
