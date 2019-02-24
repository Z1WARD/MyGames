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

x = 40
y = 500
width = 64
height = 64
move = 7

jumping = False
jumpheight = 10

left = False
right = False
walkcount = 0


def updateGameWindow():
    global walkcount
    window.blit(bg, (0, 0))

    if walkcount + 1 > 8:
        walkcount = 0

    if left:
        window.blit(walkLeft[walkcount//2], (x, y))
        walkcount += 1
    elif right:
        window.blit(walkRight[walkcount//2], (x, y))
        walkcount += 1
    else:
        window.blit(stand, (x, y))

    pygame.display.update()


run = True
while run:
    clock.tick(34)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    buttom = pygame.key.get_pressed()

    if buttom[pygame.K_LEFT] and x > move:
        x -= move
        left = True
        right = False

    elif buttom[pygame.K_RIGHT] and x < 1800 - move - width:
        x += move
        left = False
        right = True
    else:
        right = False
        left = False
        walkcount = 0

    if not jumping:
        if buttom[pygame.K_SPACE]:
            jumping = True
            right = False
            left = False
            walkcount = 0
    else:
        if jumpheight >= -10:
            neg = 1
            if jumpheight < 0:
                neg = -1
            y -= (jumpheight ** 2) / 2 * neg
            jumpheight -= 1
        else:
            jumping = False
            jumpheight = 10

    updateGameWindow()

pygame.quit()
