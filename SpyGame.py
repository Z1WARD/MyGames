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


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.move = 7
        self.jumping = False
        self.jumpHeight = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True

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


class Weapon(object):
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.speed = 8 * direction

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)


def update_game_window():
    window.blit(bg, (0, 0))
    spy.draw(window)

    for bullet in bullets:
        bullet.draw(window)

    pygame.display.update()


spy = Player(300, 410, 64, 64)
bullets = []
run = True
while run:
    clock.tick(34)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if 15 < bullet.x < 1129:
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

        if len(bullets) < 3:
            bullets.append(Weapon(round(spy.x + spy.width), round(spy.y + spy.height // 0.73), 5, (0, 0, 0), direction))

    if buttom[pygame.K_LEFT] and spy.x > spy.move:
        spy.x -= spy.move
        spy.left = True
        spy.right = False
        spy.standing = False

    elif buttom[pygame.K_RIGHT] and spy.x < 1150 - spy.move - spy.width:
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
        if spy.jumpHeight >= -10:
            neg = 1
            if spy.jumpHeight < 0:
                neg = -1
            spy.y -= (spy.jumpHeight ** 2) / 2 * neg
            spy.jumpHeight -= 1
        else:
            spy.jumping = False
            spy.jumpHeight = 10

    update_game_window()

pygame.quit()
