import pygame
import random

# initiate pygame
pygame.init()

# create the screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fight_the_virus')

# create a clock object
clock = pygame.time.Clock()

font = pygame.font.Font('FONT/Retro Gaming.ttf', 50)
font2 = pygame.font.Font('FONT/Retro Gaming.ttf', 20)
background = pygame.image.load('Graphics/space.png')
start_time = 0
score = 0
game_run = True
game_over_txt = font.render('GAME OVER', True, 'red')
game_over_rect = game_over_txt.get_rect(center=(350, 250))
elyes_win = font.render('les elyes ont gagner', True, 'red')
elyes_win_rect = elyes_win.get_rect(center=(350, 325))
restart_txt = font2.render('appuyer sur ESPACE pour recommencer', True, 'white')
restart_txt_rect = restart_txt.get_rect(center=(350, 375))


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(pygame.image.load('Graphics/spaceship_yellow.png'), 90)
        self.rect = self.image.get_rect()
        self.rect.center = (50, 335)

    def movement(self, keys_pressed):
        if keys_pressed[pygame.K_UP] and self.rect.top > 0:
            self.rect.top -= 5
        if keys_pressed[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.bottom += 5


class Projectile(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(pygame.image.load('Graphics/bullet.png'), 270)
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)

    def update(self):
        self.rect.right += 5
        if self.rect.right >= SCREEN_WIDTH + 10:
            self.kill()


class Obstacle(pygame.sprite.Sprite):

    def __init__(self):
        y_pos = random.randint(25, SCREEN_HEIGHT - 25)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotozoom(pygame.image.load('Graphics/image_compromettante.png'), 0, 0.09)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH + 50, y_pos)

    def update(self):
        global game_run
        self.rect.left -= 2
        if self.rect.right <= 0:
            game_run = False


def wave_systeme():
    global start_time
    break_time = int(pygame.time.get_ticks() / 100) - start_time
    if break_time == 10:
        start_time = int(pygame.time.get_ticks() / 100)
        obstacle1 = Obstacle()
        obstacles.add(obstacle1)


def collitions_projectile(proj):
    global score
    if pygame.sprite.spritecollide(proj, obstacles, True):
        proj.kill()
        score += 1


def collition_player():
    global game_run
    if pygame.sprite.spritecollide(player, obstacles, False):
        game_run = False


player = Player()
projectiles = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
while True:
    projectiles.update()

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if game_run:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                projectile = Projectile(x_pos=player.rect.centerx, y_pos=player.rect.centery)
                projectiles.add(projectile)
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.sprite.Group.empty(obstacles)
                score = 0
                game_run = True
                start_time = int(pygame.time.get_ticks() / 100)
    if game_run:
        score_txt = font.render(str(score), True, 'black')
        score_txt_rect = score_txt.get_rect(center=(350, 150))
        for i in projectiles:
            collitions_projectile(i)
        keys = pygame.key.get_pressed()
        screen.blit(background, (0, 0))
        projectiles.draw(screen)
        screen.blit(player.image, player.rect)
        obstacles.update()
        obstacles.draw(screen)
        player.movement(keys)
        screen.blit(score_txt, score_txt_rect)
        collition_player()
        wave_systeme()
    else:
        screen.blit(game_over_txt, game_over_rect)
        screen.blit(elyes_win, elyes_win_rect)
        screen.blit(restart_txt, restart_txt_rect)
    pygame.display.update()
    clock.tick(65)
