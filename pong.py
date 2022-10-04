# test
#April was here (:
import sys
import pygame
import random
import os
from pygame.locals import *
pygame.init()
pygame.font.init()
pygame.mixer.init() # ayy sound moment
#defines the path to the sound files in folder 'soundfiles' as s
s = 'soundfiles'
#defines the two sound files used for hitting the ball and getting a goal
hit = pygame.mixer.Sound(os.path.join(s, 'hit.wav'))
goal = pygame.mixer.Sound(os.path.join(s, 'goal.wav'))


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
pygame.display.set_caption("Pong")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

main_font = pygame.font.SysFont("comicsans", 50)
player_1_width = 35
player_1_height = 200
player_1 = pygame.Rect(25, SCREEN_HEIGHT / 2 - player_1_height / 2, player_1_width, player_1_height)
player_2_width = 35
player_2_height = 200
player_2 = pygame.Rect(SCREEN_WIDTH - (player_2_width + 25), SCREEN_HEIGHT / 2 - player_2_height / 2, player_2_width, player_2_height)
ball = pygame.Rect((SCREEN_WIDTH / 2) - (player_1.width/2), (SCREEN_HEIGHT / 2) - (player_1.width/2), 35, 35)
white = (255, 255, 255)
black = (0, 0, 0)
motion_player_1 = [0, 0]
motion_player_2 = [0, 0]
player_1_score = 0
player_2_score = 0
start_direction = random.randint(-1, 1)
while start_direction == 0:
    start_direction = random.randint(-1, 1)
motion_ball = [10 * start_direction, 0]

while True:

    screen.fill(black)

    pygame.draw.rect(screen, white, player_1)
    pygame.draw.rect(screen, white, player_2)
    pygame.draw.rect(screen, white, ball)
    score_player_1_text = main_font.render(f"Score: {player_1_score}", 1, white)
    score_player_2_text = main_font.render(f"Score: {player_2_score}", 1, white)
    screen.blit(score_player_1_text, (25, 25))
    screen.blit(score_player_2_text, (SCREEN_WIDTH - (score_player_2_text.get_width() + 25), 25))

    if player_1.colliderect(ball) or player_2.colliderect(ball):
        pygame.mixer.Sound.play(hit)
        motion_ball[0] *= -1
        motion_ball[1] = random.randint(-5, 5)
    if ball.y <= 0 or (ball.y + ball.height >= SCREEN_HEIGHT):
        motion_ball[1] *= -1

    if ball.x <= 0:
        pygame.mixer.Sound.play(goal)
        player_2_score += 1
    if ball.x + ball.width >= SCREEN_WIDTH:
        pygame.mixer.Sound.play(goal)
        player_1_score += 1
    if ball.x <= 0 or (ball.x + ball.width >= SCREEN_WIDTH):
        ball.x = (SCREEN_WIDTH / 2) - (player_1.width/2)
        ball.y = (SCREEN_HEIGHT / 2) - (player_1.width/2)
        start_direction = random.randint(-1, 1)
        while start_direction == 0:
            start_direction = random.randint(-1, 1)
        motion_ball[0] = 10 * start_direction
        motion_ball[1] = random.randint(-5, 5)
        screen.fill(black)
        pygame.draw.rect(screen, white, player_1)
        pygame.draw.rect(screen, white, player_2)
        pygame.draw.rect(screen, white, ball)
        score_player_1_text = main_font.render(f"Score: {player_1_score}", 1, white)
        score_player_2_text = main_font.render(f"Score: {player_2_score}", 1, white)
        screen.blit(score_player_1_text, (25, 25))
        screen.blit(score_player_2_text, (SCREEN_WIDTH - (score_player_2_text.get_width() + 25), 25))
        pygame.display.update()
        pygame.time.wait(1000)
        
    ball.x += motion_ball[0]
    ball.y +=motion_ball[1]

    if abs(motion_player_1[1]) < 0.1:
        motion_player_1[1] = 0
    if (player_1.y + motion_player_1[1] * 10 + player_1.height) > SCREEN_HEIGHT:
        player_1.y = SCREEN_HEIGHT - player_1.height
    elif (player_1.y + motion_player_1[1] * 10) < 0:
        player_1.y = 0
    else:
        player_1.y += motion_player_1[1] * 10


    if abs(motion_player_2[1]) < 0.1:
        motion_player_2[1] = 0
    if (player_2.y + motion_player_2[1] * 10 + player_2.height) > SCREEN_HEIGHT:
        player_2.y = SCREEN_HEIGHT - player_2.height
    elif (player_2.y + motion_player_2[1] * 10) < 0:
        player_2.y = 0
    else:
        player_2.y += motion_player_2[1] * 10

    for event in pygame.event.get():
        if (event.type == JOYAXISMOTION) and (event.axis == 0 or event.axis == 1):
            if event.axis < 2:
                motion_player_1[event.axis] = event.value
        if (event.type == JOYAXISMOTION) and (event.axis == 2 or event.axis == 3):
            if event.axis < 4:
                motion_player_2[event.axis - 2] = event.value
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()
    clock.tick(60)