import numpy
import pygame
import os
from pygame.locals import *
from sys import exit
import random
import pygame.surfarray as surfarray 
import matplotlib.pyplot as plt 

position = 5, 325
os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])
pygame.init()
screen = pygame.display.set_mode((360,320),0,32)

# Create a bar, a ball and background.
back = pygame.Surface((360,320))
background = back.convert()
background.fill((0,0,0))
abar = pygame.Surface((50,10)) 
bar = abar.convert()
bar.fill((255,100,100))
circ_sur = pygame.Surface((15,15)) 
circ = pygame.draw.circle(circ_sur,(255,255,255),(15/2,15/2),15/2)
circle = circ_sur.convert()
circle.set_colorkey((0,0,0)) 

#clock and font objects
clock = pygame.time.Clock()
font = pygame.font.SysFont("calibri",35)
ai_speed = 15

class GameState:
	"""docstring for GameState"""
	def __init__(self):
		self.bar_x, self.bar_y = 150.,305.
		self.circle_x, self.circle_y = 160.,40.
		self.bar_move = 0.
		self.speed_x, self.speed_y, self.speed_circ = 7., 7., 7. 
		self.bar_score = 0
		self.hi_score = 0

	def gameframe(self,input_vector):
		pygame.event.pump()
		reward = 0 

		if sum(input_vector) != 1:
			print '\tinput vector:',input_vector
			raise ValueError('Multiple input action!')

		if input_vector[1] ==1: # Left
			self.bar_move = -ai_speed 
		elif input_vector[2] == 1: # right
			self.bar_move = ai_speed 
		else:
			self.bar_move = 0 

		self.score  = font.render(str(self.bar_score),True,(255,255,255)) 
		self.hi_sc  = font.render("Hi: "+str(self.hi_score),True,(255,255,255)) 

		screen.blit(background,(0,0)) 
		frame = pygame.draw.rect(screen,(255,255,255),Rect((5,25),(350,290)),2) 
		#line middle_line = pygame.draw.aaline(screen,(255,255,255),(330,5),(330,475))
		screen.blit(bar,(self.bar_x,self.bar_y))
		screen.blit(circle,(self.circle_x,self.circle_y)) 
		screen.blit(self.score,(100.,0.)) 
		screen.blit(self.hi_sc,(200.,0.))
		self.bar_x += self.bar_move
		#RULES 
		#bar
		if self.bar_x >= 305.:
			self.bar_x = 305.
		if self.bar_x <= 5.: 
			self.bar_x = 5.
		#ball 
		if self.circle_x <= 5.: 
			self.circle_x = 5.
			self.speed_x = -self.speed_x
		if self.circle_x >= 345.:
			self.circle_x = 345.
			self.speed_x = - self.speed_x 
		if self.circle_y >= self.bar_y - 10.:
			if self.circle_x >= self.bar_x - 8 and self.circle_x <= self.bar_x + 43:
				self.speed_y = -self.speed_y 
				self.bar_score +=1
				reward = 1
			else:
				if self.hi_score < self.bar_score:
					self.hi_score = self.bar_score
				self.bar_score = 0
				reward = -1
				self.circle_x, self.circle_y = 160.+random.randint(-40,40),40.
		if self.circle_y <= 30.:
			self.speed_y = - self.speed_y
		self.circle_x += self.speed_x
		self.circle_y += self.speed_y
		
		#update and loop
		image_data = pygame.surfarray.array3d(pygame.display.get_surface())

		pygame.display.update()

		return image_data, reward
#
