import pygame, math, random

# Inicijalizacija py game biblioteke
pygame.init();

# background image
backgroundImg = pygame.image.load("background.png")

# Linija za postavljanje ekrana
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

# Podesavanja ekrana
pygame.display.set_caption("CS324-PZ-VeljkoArsic")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# podesavanja za igru
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
score_textX = 10
score_textY = 10

lives_value = 3
lives_font = pygame.font.Font('freesansbold.ttf', 32)
lives_textX = 10
lives_textY = 40

deathFont = pygame.font.Font('freesansbold.ttf', 50)


def showScore(x, y):
    score = score_font.render("Score : " + str(int(score_value)), True, (255, 0, 0))
    screen.blit(score, (x, y))


def showLives(x, y):
    if lives_value == 3:
        lives = lives_font.render("Lives : " + str(lives_value), True, (0, 255, 0))
    elif lives_value == 2:
        lives = lives_font.render("Lives : " + str(lives_value), True, (255, 255, 0))
    elif lives_value == 1:
        lives = lives_font.render("Lives : " + str(lives_value), True, (255, 0, 0))
    elif lives_value == 0:
        lives = lives_font.render("Lives : " + str(lives_value), True, (0, 0, 0))

    screen.blit(lives, (x, y))


def deathScreen():
    if isDead:
        dead = lives_font.render("You are dead! Press R to restart!", True, (255, 0, 0))
        screen.blit(dead, (150, 200))


# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
player_speed = 0
isDead = False

# explosion
explosionImage = pygame.image.load("explosion.png")
explosionX = playerX
explosionY = playerY

# enemies
enemyImg = []
enemyX = []
enemyY = []
enemy_speed = []
num_of_enemies = 6
isSpedUp = False

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(1, 740))
    enemyY.append(random.randint(-200, -2))
    enemy_speed.append(2)

# bullet
# Ready - spreman za ispaljivanje
# Fire - metak je ispaljen
bulletImg = pygame.image.load("bullet1.png")
bulletX = playerX
bulletY = playerY
bullet_speed = 10
bullet_state = "ready"


def showExplosion(x, y):
    global isDead
    if isDead:
        screen.blit(explosionImage, (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))


def restart():
    global bullet_speed, isDead, enemy_speed, lives_value, score_value

    lives_value = 3
    bullet_speed = 10
    score_value = 0
    isDead = False
    for i in range(num_of_enemies):
        enemyY[i] = random.randint(-200, -2)
        enemyX[i] = random.randint(1, 740)
        enemy_speed[i] = 2


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def speedUp():
    for i in range(num_of_enemies):
        enemy_speed[i] += 0.2
        print(enemy_speed[i])


def distance_between(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance < 27:
        return True
    else:
        return False


# Main game loop
time_elapsed = 0
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Kontrole
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and isDead is False:
                player_speed = -4
            if event.key == pygame.K_RIGHT and isDead is False:
                player_speed = 4
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                fire(bulletX, playerY)
                fire(bulletX + 52, playerY)
            if event.key == pygame.K_r and isDead:
                restart()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_speed = 0
    if playerX <= 0:
        playerX = 0
    if playerX >= 737:
        playerX = 737

    playerX += player_speed
    player(playerX, playerY)

    # kretanje metka
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire(bulletX, bulletY)
        fire(bulletX + 52, bulletY)
        bulletY -= bullet_speed

    showScore(score_textX, score_textY)
    showLives(lives_textX, lives_textY)
    for i in range(num_of_enemies):
        enemyY[i] += enemy_speed[i]
        enemy(enemyX[i], enemyY[i], i)
        # detekcija kolizije
        collision = distance_between(enemyX[i], enemyY[i], bulletX, bulletY)

        playerCollision = distance_between(enemyX[i], enemyY[i], playerX, playerY)

        if playerCollision:
            enemyY[i] = random.randint(-200, -2)
            enemyX[i] = random.randint(1, 740)
            lives_value -= 1

        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyY[i] = random.randint(-200, -2)
            enemyX[i] = random.randint(1, 740)
        if enemyY[i] >= 600:
            enemyY[i] = random.randint(-200, -2)
            enemyX[i] = random.randint(1, 740)

        if lives_value == 0:
            isDead = True
            player_speed = 0
            enemy_speed[i] = 0
            bullet_speed = 0
            showExplosion(playerX - 32, playerY - 32)

    dt = clock.tick(60)
    time_elapsed += dt

    if time_elapsed > 10000:
        speedUp()
        time_elapsed = 0

    deathScreen()
    pygame.display.update()
