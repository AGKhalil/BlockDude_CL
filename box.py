import pygame

class Box:

	def __init__(self, screen, image, x, y):

		self.screen = screen

		self.x = x
		self.y = y
		self.width = 24
		self.height = 24

		self.box = pygame.image.load(image)

	def draw(self):
		for i in range(len(self.x)):
			self.screen.blit(self.box, (self.x[i], self.y[i]))

	def is_box(self, player_x, player_y):
		for i in range(len(self.x)):
			if player_x == self.x[i] and player_y == self.y[i]:
				return [True, i]
		return [False, -1]

	# def set_direction(self, direction):
	# 	if direction == 'LEFT':
	# 		self.left = True
	# 		self.right = False
	# 	else:
	# 		self.left = False
	# 		self.right = True

	# def get_direction(self):
	# 	if self.left == True and self.right == False:
	# 		return 'LEFT'
	# 	else:
	# 		return 'RIGHT'
