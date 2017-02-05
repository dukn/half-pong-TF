#import numpy 
import pygame
from pygame.locals import *
from sys import exit
import random 
import pygame.surfarray as surfarray 
#import matplotlib.pyplot as plt 


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

#definitions
bar_x,bar_y = 150.,305.
circle_x,circle_y = 160.,40.
bar_move = 0.
speed_x, speed_y, speed_circ = 250., 250., 250. 
bar_score = 0
hi_score = 0

#clock and font objects
clock = pygame.time.Clock()
font = pygame.font.SysFont("calibri",35)
ai_speed = 15
done = False 
while done == False:
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done = True # Flag that we are done so we exit this loop
		if event.type == KEYDOWN:
			if event.key == K_LEFT:
				bar_move = -ai_speed 
			elif event.key == K_RIGHT:
				bar_move = ai_speed
		elif event.type == KEYUP:
			if event.key == K_LEFT:
				bar_move = 0.
			elif event.key == K_RIGHT:
				bar_move = 0.

	score  = font.render(str(bar_score),True,(255,255,255))
	hi_sc  = font.render("Hi: "+str(hi_score),True,(255,255,255))
	screen.blit(background,(0,0)) 
	frame = pygame.draw.rect(screen,(255,255,255),Rect((5,25),(350,290)),2) 
	#line middle_line = pygame.draw.aaline(screen,(255,255,255),(330,5),(330,475))
	screen.blit(bar,(bar_x,bar_y))
	screen.blit(circle,(circle_x,circle_y)) 
	screen.blit(score,(100.,0.)) 
	screen.blit(hi_sc,(200.,0.))
	bar_x += bar_move 

	#movement of circle 
	time_passed = clock.tick(30)
	time_sec = time_passed/1500.0
	circle_x += speed_x * time_sec
	circle_y += speed_y * time_sec

	#RULES 
	#bar
	if bar_x >= 305.: 
		bar_x = 305.
	if bar_x <= 5.: 
		bar_x = 5.
	#ball 
	if circle_x <= 5.: 
		circle_x = 5.
		speed_x = -speed_x
	if circle_x >= 345.:
		circle_x = 345.
		speed_x = - speed_x 
	if circle_y >= bar_y - 10.:
		if circle_x >= bar_x - 8 and circle_x <= bar_x + 43:
			speed_y = -speed_y 
			bar_score +=1
		else:
			if hi_score < bar_score:
				hi_score = bar_score
			bar_score = 0
			circle_x, circle_y = 160.+random.randint(-40,40),40.
	if circle_y <= 30.:
		speed_y = - speed_y


	#update and loop
	pygame.display.update()

#pygame.display.update()
#raw_input()
pygame.quit()
