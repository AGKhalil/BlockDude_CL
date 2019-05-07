import sys
import os
import pygame

mypath = os.path.dirname(os.path.realpath(__file__))


class Player:

    def __init__(self, screen, x, y, width, height):

        self.screen = screen

        self.x = x[:]
        self.y = y[:]
        self.width = width
        self.height = height

        self.left = False
        self.right = False

        self.walkRight = pygame.image.load(
            os.path.join(mypath, 'BD_sprites/DudeRight.png'))
        self.walkLeft = pygame.image.load(
            os.path.join(mypath, 'BD_sprites/DudeLeft.png'))

    def draw(self):
        if self.right:
            self.screen.blit(self.walkRight, (self.x[0], self.y[0]))
        else:
            self.screen.blit(self.walkLeft, (self.x[0], self.y[0]))

    def set_direction(self, direction):
        if direction == 'LEFT':
            self.left = True
            self.right = False
        else:
            self.left = False
            self.right = True

    def get_direction(self):
        if self.left == True and self.right == False:
            return 'LEFT'
        else:
            return 'RIGHT'

    def set_position(self, x_pos, y_pos):
        self.x = x_pos[:]
        self.y = y_pos[:]
