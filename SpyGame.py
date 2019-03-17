import pygame
pygame.init()

window = pygame.display.set_mode((1150, 670))
pygame.display.set_caption("Spy")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png')]
bg = pygame.image.load('bg(1200*675).png')
stand = pygame.image.load('R1.png')

clock = pygame.time.Clock()

score = 0


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.move = 7
        self.jumping = False
        self.jumpHeight = 8
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 28, self.y, 35, 50)

    def draw(self, window):
        if self.walkCount + 1 > 8:
            self.walkCount = 0

        if not(self.standing):
            if self.right:
                window.blit(walkRight[self.walkCount // 2], (self.x, self.y))
                self.walkCount += 1
            elif self.left:
                window.blit(walkLeft[self.walkCount // 2], (self.x, self.y))
                self.walkCount += 1

        else:
            if self.left:
                window.blit(walkLeft[0], (self.x, self.y))
            else:
                window.blit(walkRight[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 10, 78, 140)


class Enemy(object):
    walkRight = [pygame.image.load('RE1'), pygame.image.load('RE2'), pygame.image.load('RE3'),
                 pygame.image.load('RE4'), pygame.image.load('RE5'), pygame.image.load('RE6')]
    walkLeft = [pygame.image.load('LE1'), pygame.image.load('LE2'), pygame.image.load('LE3'),
                 pygame.image.load('LE4'), pygame.image.load('LE5'), pygame.image.load('LE6')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.speed = 5
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.health = 2
        self.visible = True

    def draw(self, window):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 16:
                self.walkCount = 0

            if self.speed > 0:
                window.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                window.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 15, self.y + 12, 50, 85)
            pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 30, 50, 10))
            pygame.draw.rect(window, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 30, 50 - ((50/3) * (2 - self.health)), 10))

    def move(self):
        if self.speed > 0:
            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkCount = 0
        else:
            if self.x - self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.health -= 1
            self.visible = False
        print("HIT!")


class Weapon(object):
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.speed = 20 * direction

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)


def update_game_window():
    window.blit(bg, (0, 0))
    spy.draw(window)
    soldier.draw(window)
    text = font.render('Score: ' + str(score), 1, (5, 5, 5))
    window.blit(text, (0, 10))

    for bullet in bullets:
        bullet.draw(window)

    pygame.display.update()


font = pygame.font.SysFont('comicsans', 40, True, True)
spy = Player(300, 410, 64, 64)
soldier = Enemy(100, 475, 64, 64, 1000)
bullets = []
run = True
while run:
    clock.tick(40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < soldier.hitbox[1] + soldier.hitbox[3] and bullet.y + bullet.radius > soldier.hitbox[1]:
            if bullet.x + bullet.radius > soldier.hitbox[0] and bullet.x - bullet.radius < soldier.hitbox[0] + soldier.hitbox[2]:
                soldier.hit()
                score += 1
                if soldier.health < 0:
                    soldier = Enemy(0, 0, 0, 0, 0)
                    soldier.visible = False
                bullets.pop(bullets.index(bullet))

        if 15 < bullet.x < 1145:
            bullet.x += bullet.speed
        else:
            bullets.pop(bullets.index(bullet))

    buttom = pygame.key.get_pressed()

    if buttom[pygame.K_SPACE]:
        if spy.right:
            direction = 1
        elif spy.left:
            direction = -1
        else:
            direction = 1

        if len(bullets) < 1:
            bullets.append(Weapon(round(spy.x + spy.width), round(spy.y + spy.height // 0.73), 5, (0, 100, 200), direction))

    if buttom[pygame.K_LEFT] and spy.x > spy.move:
        spy.x -= spy.move
        spy.left = True
        spy.right = False
        spy.standing = False

    elif buttom[pygame.K_RIGHT] and spy.x < 1140 - spy.move - spy.width:
        spy.x += spy.move
        spy.left = False
        spy.right = True
        spy.standing = False
    else:
        spy.standing = True
        spy.walkCount = 0

    if not spy.jumping:
        if buttom[pygame.K_UP]:
            spy.jumping = True
            spy.right = False
            spy.left = False
            spy.walkCount = 0
    else:
        if spy.jumpHeight >= -8:
            neg = 1
            if spy.jumpHeight < 0:
                neg = -1
            spy.y -= (spy.jumpHeight ** 2) / 2 * neg
            spy.jumpHeight -= 1
        else:
            spy.jumping = False
            spy.jumpHeight = 8

    update_game_window()

pygame.quit()
