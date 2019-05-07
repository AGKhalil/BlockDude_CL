import sys
import os
import pygame

mypath = os.path.dirname(os.path.realpath(__file__))


class Component:

    def __init__(self, screen, image, x, y):

        self.screen = screen

        self.x = x[:]
        self.y = y[:]

        self.component = pygame.image.load(os.path.join(mypath, image))

    def draw(self):
        for i in range(len(self.x)):
            self.screen.blit(self.component, (self.x[i], self.y[i]))

    def is_component(self, player_x, player_y):
        for i in range(len(self.x)):
            if player_x == self.x[i] and player_y == self.y[i]:
                return [True, i]
        return [False, -1]

    def is_door(self, player_x, player_y):
        if player_x == self.x and player_y == self.y:
            return True
        return False

    def set_position(self, x_pos, y_pos):
        self.x = x_pos[:]
        self.y = y_pos[:]
