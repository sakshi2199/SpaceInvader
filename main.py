import pygame
import random
import math
from pygame import mixer

pygame.init()  # initializing pygame
# (width, height)
screen = pygame.display.set_mode((800, 600))

# background
bg = pygame.image.load('galaxy.png')

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")

# Add Attribution rocket=  https://www.flaticon.com/free-icon/rocket_599193?term=space%20ships&page=1&position=14
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy aka monster
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(35)

# bullet
# ready = you cannot see the bullet on the screen
# fire = bullet is moving

bulletImg = pygame.image.load('bullet1.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('game_over.ttf', 70)
textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('game_over.ttf', 100)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (250, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))  # drawing the image on the screen, blit = to draw


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# player = https://www.flaticon.com/free-icon/space-invaders_744737?term=arcade%20space&page=1&position=1
# bullet = https://www.flaticon.com/free-icon/bullet_523764?term=bullet&page=1&position=3
# Game Loop
running = True
while running:
    # RGB  0-255
    screen.fill((0, 0, 0))
    # background image fill
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():  # every event gets locked in this
        if event.type == pygame.QUIT:
            running = False
        # check if a key is pressed, if it is left or right
        if event.type == pygame.KEYDOWN:  # KEYDOWN means pressing on the Key And KEYUP means releasing it
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # setting up boundary for player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800-64 = 736
        playerX = 736

    # boundary settings for enemy
    for i in range(num_of_enemies):
        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # 800-64 = 736
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        # monster = https://www.flaticon.com/free-icon/alien_1970352?term=alien&page=1&position=15
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            expl_Sound = mixer.Sound('explosion.wav')
            expl_Sound.play()
            # expl =explosion
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # always add this line
