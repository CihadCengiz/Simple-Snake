# -*- coding: utf-8 -*-

#import pygame and other modules
import pygame
import sys
import random
import time

from pygame.locals import *

#initialize the pygame module
pygame.init()

#Set FPS
FPS = 5

UP    = 0b0001
DOWN  = 0b0010
LEFT  = 0b0100
RIGHT = 0b1000

#load and set the logo
logo_path = "icons/snake.png"
logo = pygame.image.load(logo_path)
pygame.display.set_icon(logo)

#colors
bg_color = [40, 53, 71] #dark blue???
tile_color = [40, 53, 71] #darker blue???
border_color = [255, 255, 255] #white,

#change caption name
pygame.display.set_caption("Snake!")

#create a surface on screen (width x height)
SCREEN_WIDTH, SCREEN_HEIGHT  = 832, 544
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill(bg_color) #fill the screen

#fps controller
fps_controller = pygame.time.Clock()

###DRAWING BORDER
#top 32 pixell - bottom 32 pixell
#30x30 (square (480x480))
#sides - 32 pixell from left - 320 pixell from right
BORDER_SIZE = 16
BORDER_WIDTH = SCREEN_WIDTH / BORDER_SIZE
BORDER_HEIGHT = SCREEN_HEIGHT / BORDER_SIZE

#BORDER SETTINGS
thickness = 1
top, left, b_widht, b_height = 32, 32, 480, 480

#screen.blit(surface, (0,0))

def draw_box(surf, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (BORDER_SIZE, BORDER_SIZE))
    pygame.draw.rect(surf, color, r)

#DRAWING SCORE
font = pygame.font.SysFont(None,24) #Font size and type
score_img = font.render('Score: ',True, border_color) #Converting text to img
screen.blit(score_img, (652,32)) #Drawing the text

class Snake(object):
    #load image
    body_img = ("icons/snake_body.png")
    head_img = ("icons/snake_head.png")
    snake_head = pygame.image.load(head_img)
    snake_body = pygame.image.load(body_img)

    #make image background transparent - has no effects!
    snake_head.set_alpha(None)
    snake_head.set_colorkey((40,53,71))
    snake_body.set_alpha(None)
    snake_body.set_colorkey((40,53,71))

    head_e = snake_head
    head_s = pygame.transform.rotate(snake_head, -90)
    head_n = pygame.transform.rotate(snake_head, 90)
    head_w = pygame.transform.rotate(snake_head, 180)

    def __init__(self):
        self.length = 1
        self.surface = surface
        self.vel = 16
        start_pos = 32, 32
        self.body = [start_pos]
        self.direction = RIGHT
        self.image = self.head_e


    def move(self, surface):
        #self.keys = pygame.key.get_pressed()
        #if any((self.keys[pygame.K_w], self.keys[pygame.K_s], self.keys[pygame.K_a], self.keys[pygame.K_d])):
        #    self.direction = self.keys[pygame.K_w]*1 + self.keys[pygame.K_s]*2 + self.keys[pygame.K_a]*4 + self.keys[pygame.K_d]*8

        if self.direction == UP:
            self.image = self.head_n
        elif self.direction == DOWN:
            self.image = self.head_s
        elif self.direction == LEFT:
            self.image = self.head_w
        elif self.direction == RIGHT:
            self.image = self.head_e

        x, y = self.body[0] # Get the head position, which is always the first in the "history" aka body.
        self.body.pop() # Remove the last object from history

        if self.direction & UP:
            if y > 16:
                y = (y - self.vel)%512
            if y <= 16:
                y = 496

        elif self.direction & DOWN:
            if y >= 496:
                y = 16
            if y < 496:
                y = (y + self.vel)%512

        elif self.direction & LEFT:
            if not x <= 16:
                x = (x - self.vel)%512
            if x <= 16:
                x = 512
                x = (x - self.vel)%512

        elif self.direction & RIGHT:
            if x >= 496:
                x = 16
            if x < 496:
                x = (x + self.vel)%512
        self.body.insert(0, (x, y))

    def draw(self, surface):
        for x, y in self.body:
            surface.blit(self.snake_body, (x, y))
        for x, y in self.body:
            surface.blit(self.image, (x, y))
            break

class Apple(object):
    def __init__(self):
        self.position = [0,0]
        self.color = (255,0,0)
        self.randomize()

    def randomize(self):
        self.position = (random.choice(range(32,512,16)), random.choice(range(32,512,16)))
        if self.position in snake.body:
            self.position = (random.choice(range(32,512,16)), random.choice(range(32,512,16)))

    def draw(self, surf):
        draw_box(surf, self.color, self.position)

def checkEat(snake, apple):
    x, y = snake.body[0]
    if x == apple.position[0] and y == apple.position[1]:
        snake.length += 1
        apple.randomize()
        snake.body.append(snake.body[-1])
        return True
    else:
        return False

font_style = pygame.font.SysFont(None, 35)

def message(msg,color):
    mesg = font_style.render(msg, True, color)
    #mesg2 = font.render('New Game', True, (255,255,255))
    surface.fill((0,0,0))
    surface.blit(mesg, [450/2, 512/2])
    #surface.blit(mesg2, [652, 132])

#main loop control key
running = True

#runs only if this module is executed as the main script
if __name__ == "__main__":
    snake = Snake()
    apple = Apple()


    #main loop
    while running:
        #event handling
        for event in pygame.event.get():
            #QUIT func - (Close(X) button)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_w:
                    if snake.direction != UP and snake.direction != DOWN:
                        snake.direction = UP
                elif event.key == pygame.K_s:
                    if snake.direction != DOWN and snake.direction != UP:
                        snake.direction = DOWN 
                elif event.key == pygame.K_a:
                    if snake.direction != LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT 
                elif event.key == pygame.K_d:
                    if snake.direction != RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT
        
        surface.fill(bg_color)
        snake.move(surface)
        #msg2 = font.render('New Game', True, (255,255,255))
        #surface.blit(msg2, [652, 132])

        if snake.body[0] in snake.body[1:]:
            running = False
            message("You lost",border_color)
            pygame.display.update()

        checkEat(snake, apple)
        snake.draw(surface)
        apple.draw(surface)
        pygame.draw.rect(surface,border_color,[top,left,b_widht,b_height], thickness)
        screen.blit(surface, (0,0))

        #score board
        font = pygame.font.SysFont(None,24) #Font size and type
        score_img = font.render('Score: ' + str(snake.length), True, border_color) #Converting text to img
        screen.blit(score_img, (652,32)) #Drawing the text

        pygame.display.flip()
        pygame.display.update()
        fps_controller.tick(FPS + snake.length/3)
        #fps_controller.tick(5)
      
    
    time.sleep(100)