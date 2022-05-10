import pygame
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 900, 500
BALEN_WIDTH, BALEN_HEIGHT = 80, 80
OLI_WIDTH, OLI_HEIGHT = 70, 75
RAN1_OLI = random.randint(50, 100)
RAN2_OLI = random.randint(-100, 200)
BORDER = pygame.Rect(WIDTH/2-5, 0, 10, HEIGHT)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lauro! Clean The City")

# Events
RED_HIT = pygame.USEREVENT+1
YELLOW_HIT = pygame.USEREVENT+2

# health
red_health = 100
yellow_health = 100


# Consts
BLACK = (0, 0, 0)
PURPLE = (75, 0, 130)
COLOR = WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3

BALEN_image = pygame.image.load(os.path.join('Assets', 'bale.jpg'))
BALEN = pygame.transform.scale(BALEN_image, (BALEN_WIDTH, BALEN_HEIGHT))
OLI_image = pygame.image.load(os.path.join('Assets', 'oli.jpg'))
OLI = pygame.transform.scale(OLI_image, (OLI_WIDTH, OLI_HEIGHT))
VOTE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'vote.jpg')), (WIDTH, HEIGHT))
APPLE_imgae = pygame.image.load(os.path.join('Assets', 'apple.png'))
APPLE = pygame.transform.scale(APPLE_imgae, (13, 13))
LAURO = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'lauro.png')), (100, 20))

HEALTH_FONT = pygame.font.SysFont('comicsans', 20)

red_bullets = []  # red bullets= lauro
yellow_bullets = []  # yellow bullets= apple


winner_text = ""


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(VOTE, (0, 0))
    pygame.draw.rect(WIN, PURPLE, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (10, 10))
    WIN.blit(yellow_health_text, (WIDTH-yellow_health_text.get_width()-10, 10))
    WIN.blit(BALEN, (red.x, red.y))
    WIN.blit(OLI, (yellow.x, yellow.y))
    #WIN.blit(HAS,(red.x+80, red.y+40) )
    for bullet in red_bullets:
        WIN.blit(LAURO, (bullet.x, bullet.y))
        #pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        WIN.blit(APPLE, (bullet.x, bullet.y))
        #pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def red_handel_movement(keys, red):
    if keys[pygame.K_a] and red.x-VEL > 0:  # left
        red.x -= VEL
    if keys[pygame.K_d] and red.x < BORDER.x-BALEN_WIDTH:  # Right
        red.x += VEL
    if keys[pygame.K_w] and red.y-VEL > 0:  # UP
        red.y -= VEL
    if keys[pygame.K_s] and red.y+VEL+BALEN_HEIGHT < HEIGHT:  # Dow
        red.y += VEL


def yellow_handel_movement(keys, yellow):
    if keys[pygame.K_LEFT] and yellow.x-VEL > BORDER.x:  # left
        yellow.x -= VEL
    if keys[pygame.K_RIGHT] and yellow.x < WIDTH-OLI_WIDTH:  # Right
        yellow.x += VEL
    if keys[pygame.K_UP] and yellow.y-VEL > 0:  # UP
        yellow.y -= VEL
    if keys[pygame.K_DOWN] and yellow.y+VEL+BALEN_HEIGHT < HEIGHT:  # Dow
        yellow.y += VEL


def handle_bullets(yellow_bullets, red_bullets, red, yellow):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)


def main():
    # rectangle to control the player movement, x,y,wid, heig
    red = pygame.Rect(100, 300, BALEN_WIDTH, BALEN_HEIGHT)
    yellow = pygame.Rect(700, 0, OLI_WIDTH, OLI_HEIGHT)
    global red_health  # As we will change this inside main()
    global yellow_health
    global winner_text
    clock = pygame.time.Clock()  # control the fram rate
    run = True
    while run:
        clock.tick(FPS)

        # defferent events and looping through them
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:  # pressed the key
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x+red.width, red.y+red.height//2, 10, 5)
                    red_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x, yellow.y+yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 10
            if event.type == YELLOW_HIT:
                yellow_health -= 10

        if (red_health <= 0):
            winner_text = "Oli Wins"
        if (yellow_health <= 0):
            winner_text = "Balen Wins"

        if winner_text != "":
            pass  # somone won
        # what keys are currently pressed everytime loops
        keys_pressed = pygame.key.get_pressed()
        red_handel_movement(keys_pressed, red)
        yellow_handel_movement(keys_pressed, yellow)
        handle_bullets(yellow_bullets, red_bullets, red, yellow)
        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)
    pygame.quit()


if __name__ == '__main__':  # only run if the file is run directly , won't run while importing!
    main()
