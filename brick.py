import pygame

class Brick:

	def __init__(self, screen, x, y):

		self.screen = screen

		self.x = x
		self.y = y
		self.width = 24
		self.height = 24

		self.brick = pygame.image.load('BD_sprites/Brick.png')

	def draw(self):
		for i in range(len(self.x)):
			self.screen.blit(self.brick, (self.x[i], self.y[i]))

	def is_brick(self, player_x, player_y):
		for i in range(len(self.x)):
			if player_x == self.x[i] and player_y == self.y[i]:
				return (True, i)
			else:
				return (False, -1)