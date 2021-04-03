import pygame
import random
import math

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('space_background.jpg')

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('server-icon.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerDx = 0

FPS = 60
enemyImg = []
enemyX = []
enemyY = []
enemyDx = []
enemyDy = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyDx.append(3)
    enemyDy.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletDy = 6
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

game_over_font = pygame.font.Font('freesansbold.ttf', 64)

background_rect = background.get_rect()


def render(surface, text, size, x, y):
    font_name = pygame.font.match_font('8-BIT WONDER.ttf')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def start_menu():
    screen.blit(background, background_rect)
    render(screen, "Welcome to Space Game", 48, 800 / 2, 600 / 4)
    render(screen, "Arrows to move", 25, 800 / 2, 600 / 1.5)
    render(screen, "Press any key to begin", 22, 800 / 2, 600 * 3 / 4)
    pygame.display.flip()
    menu = True
    while menu:
        clock.tick(FPS)
        for key in pygame.event.get():
            if key.type == pygame.QUIT:
                pygame.quit()
            if key.type == pygame.KEYUP:
                menu = False


def end_menu():
    screen.blit(background, background_rect)
    render(screen, "YOU ARE LOSER", 64, 800 / 2, 600 / 4)
    render(screen, "Your Scores:" + str(score_value), 32, 800 / 2, 600 / 2)
    render(screen, "Press ESCAPE To End", 22, 800 / 2, 600 * 3 / 4)
    pygame.display.flip()
    end = True
    while end:
        clock.tick(FPS)
        for key in pygame.event.get():
            key_pressed = pygame.key.get_pressed()
            if key.type == pygame.QUIT:
                pygame.quit()
            if key_pressed[pygame.K_ESCAPE]:
                pygame.quit()


def game_over_text():
    over = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


ok = True
keyPressed = True
New_Game = True
Game_Over = False

while ok:
    clock.tick(FPS)
    if New_Game:
        start_menu()
        New_Game = False
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ok = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerDx = -5
            if event.key == pygame.K_RIGHT:
                playerDx = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerDx = 0

    playerX += playerDx
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[i] = 2000
            #game_over_text()
            Game_Over = True
            end_menu()
            break
        enemyX[i] += enemyDx[i]
        if enemyX[i] <= 0:
            enemyDx[i] = 3
            enemyY[i] += enemyDy[i]
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyDx[i] = -3
            enemyY[i] += enemyDy[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletDy

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
