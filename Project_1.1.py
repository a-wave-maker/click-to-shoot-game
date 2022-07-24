from genericpath import exists
import pygame
import random
import string

from pygame import display, init


# region                                                                                            GLOBAL
GREEN = (0,255,0)
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1000

DEAD = -1
MOVING = 0
ATTACKING = 1
WAITING = 2

score = 0
enemycount = 0

#settings
baseenemyspeed = 15
baseenemyhelf = 20
basebasehelf = 100
PLANESPAWNMOD = 2
TANKSPAWNMOD = 4
DIFFMOD = 10
# endregion

# region                                                                                            INITIALAZING
# initialize the pygame module
pygame.init()
pygame.mixer.init()
pygame.font.init()

#preload fonts
myfont = pygame.font.SysFont('Comic Sans MS', 30)
mybiggerfont = pygame.font.SysFont('Comic Sans MS', 75)

#preload sounds
s_bang = pygame.mixer.Sound('./resources/bang.wav')
s_death = pygame.mixer.Sound('./resources/death.wav')
s_boom = pygame.mixer.Sound('./resources/boom.wav')
s_crash = pygame.mixer.Sound('./resources/crash.wav')

clock = pygame.time.Clock()

# endregion


class Enemy(pygame.sprite.Sprite):                                                                  #BASE ENEMY CLASS
    
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("./resources/enemy.png")
        self.imagebase = pygame.image.load("./resources/enemy.png")
        self.imageshoot = pygame.image.load("./resources/enemy_f.png")
        self.imagedead = pygame.image.load("./resources/enemy_d.png")

        self.rect = self.image.get_rect()
        self.rect.center = (0, random.randint(400, SCREEN_HEIGHT - 300))

        self.speed = baseenemyspeed
        self.helf = baseenemyhelf
        self.status = MOVING
        self.timer = 0
        self.score = 1
 
    def updateSelf(self):
        global score
        global enemycount

        if self.status == DEAD:
            pass
        elif self.helf <= 0:
            self.status = DEAD
            self.image = self.imagedead
            s_death.play()
            score += self.score
            enemycount -= 1
        elif self.status == WAITING:
            self.image = self.imagebase
            if random.randint(1, 10) > 5:
                self.status = ATTACKING
        elif self.status == ATTACKING:
            self.image = self.imageshoot
            if random.randint(1, 10) > 5:
                self.status = WAITING
        elif self.rect.left < 1200:  
            self.rect.move_ip(self.speed, 0)
        else:
            self.status = WAITING
 
    def getShot(self):
        self.helf -= 10

    def drawSelf(self, surface):
        surface.blit(self.image, self.rect)
        #helfbar
        pygame.draw.rect(surface, GREEN, pygame.Rect(self.rect.left + 25, self.rect.top - 25, self.helf, 5))
 
class Tank(Enemy):                                                                                  #TANK CLASS
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./resources/tank.png")
        self.imagebase = pygame.image.load("./resources/tank.png")
        self.imageshoot = pygame.image.load("./resources/tank_f.png")
        self.imagedead = pygame.image.load("./resources/tank_d.png")

        self.rect = self.image.get_rect()
        self.rect.center = (0, random.randint(600, SCREEN_HEIGHT - 100))

        self.speed = self.speed / 1.5
        self.helf = self.helf * 3
        self.score = 2

    def updateSelf(self):
        global score
        global enemycount

        if self.status == DEAD:
            pass
        elif self.helf <= 0:
            self.status = DEAD
            self.image = self.imagedead
            s_boom.play()
            score += self.score
            enemycount -= 1
        elif self.status == WAITING:
            self.image = self.imagebase
            if random.randint(1, 100) > 75:
                self.status = ATTACKING
        elif self.status == ATTACKING:
            self.image = self.imageshoot
            if random.randint(1, 100) > 95:
                self.status = WAITING
        elif self.rect.left < 1200:  
            self.rect.move_ip(self.speed, 0)
        else:
            self.status = WAITING

class Plane(Enemy):                                                                                 #PLANE CLASS
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./resources/plane.png")
        self.imagebase = pygame.image.load("./resources/plane.png")
        self.imageshoot = pygame.image.load("./resources/plane_f.png")
        self.imagedead = pygame.image.load("./resources/plane_d.png")

        self.rect = self.image.get_rect()
        self.rect.center = (0, random.randint(300, SCREEN_HEIGHT - 600))

        self.speed = self.speed * 2
        self.helf = self.helf / 2
        self.score = 3

    def updateSelf(self):
        global score
        global enemycount

        if self.status == DEAD:
            pass
        elif self.helf <= 0:
            self.status = DEAD
            self.image = self.imagedead
            s_crash.play()
            score += self.score
            enemycount -= 1
        elif self.status == WAITING:
            self.image = self.imagebase
            if random.randint(1, 10) > 2:
                self.status = ATTACKING
        elif self.status == ATTACKING:
            self.image = self.imageshoot
            if random.randint(1, 10) > 2:
                self.status = WAITING
        elif self.rect.left < 1200:  
            self.rect.move_ip(self.speed, 0)
        else:
            self.status = WAITING

class Player(pygame.sprite.Sprite):                                                                 #PLAYER CLASS
    
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("./resources/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (1450, 650)
 
    def updateSelf(self):
        self.image = pygame.image.load("./resources/player.png")

    def fireGun(self, master, x, y):
        self.image = pygame.image.load("./resources/player_f.png")
        s_bang.play()
        for enemy in master.enemies:
            if enemy.rect.collidepoint(x,y):
                enemy.getShot()

    def drawSelf(self, surface):
        surface.blit(self.image, self.rect)  

class Gamemaster():                                                                                 #CLASS FOR MANAGING THE GAME
    
    def __init__(self):
        global score

        self.player = Player()
        self.enemies = []

        self.background = pygame.image.load("./resources/map.png")

        self.basehelf = basebasehelf
        self.basedamage = 0
        self.score = myfont.render(str(score), False, (0,0,0))
        self.planespawnmod = PLANESPAWNMOD
        self.tankspawnmod = TANKSPAWNMOD
        self.level = 1

    def spawnEnemy(self):
        #to stop the game from breaking from having too many enemies at a time
        global enemycount 

        #spawn random enemy
        r = random.randint(0, 10)
        if r < self.planespawnmod:
            tmp_e = Plane()
        elif r < self.tankspawnmod:
            tmp_e = Tank()
        else:
            tmp_e = Enemy()
        
        self.enemies.append(tmp_e)
        enemycount += 1

    def drawAll(self, surface):
        surface.blit(self.background, (0,0))
        surface.blit(self.score, (10,0))
        self.player.drawSelf(surface)
        pygame.draw.rect(surface, GREEN, pygame.Rect(1400, 300, self.basehelf, 20))
        for enemy in self.enemies:
            enemy.drawSelf(surface)

    def updateAll(self):
        global baseenemyspeed
        global baseenemyhelf

        #update player
        self.player.updateSelf()

        #update score
        self.score = myfont.render(str(score), False, (0,0,0))

        #update enemies
        for enemy in self.enemies:
            enemy.updateSelf()
            if enemy.status == ATTACKING or enemy.status == WAITING:
                self.basedamage += 1
            elif enemy.status == DEAD:
                if enemy.timer == 500:
                    enemy.kill()
                    self.enemies.remove(enemy)
                else:
                    enemy.timer += 1

        #update difficulty
        if score > DIFFMOD * self.level:
            baseenemyhelf += 1
            baseenemyspeed += 1
            self.level += 1

    def damageBase(self):
        self.basehelf -= self.basedamage
        self.basedamage = 0

    def gameOver(self, surface):
        surface.fill((0,0,0))
        master.player.image = pygame.image.load("./resources/player_d.png")
        master.drawAll(surface)
        gosplash = pygame.image.load("./resources/g_over_splash.png")
        self.background = pygame.image.load("./resources/game_over.png")
        surface.blit(self.background, (0,0))
        surface.blit(gosplash, (0,0))
        surface.blit(mybiggerfont.render(str(score), False, (0,0,0)), (820,645))
        pygame.time.wait(200)


# region                                                                                            PRE-GAME STUFF
FramePerSec = pygame.time.Clock()

#general stuffs
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
#textsurface = myfont.render(str(pygame.time.get_ticks()), True, (0,0,0))
logo = pygame.image.load("./resources/player.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Stick war or sth")
#endofstuffs

# create a surface on screen, now in FULL HD
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill((0,0,0))

#initialize the game master
master = Gamemaster()

#timer
milliseconds_delay = 1000
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, milliseconds_delay)

running = True     
# endregion

pygame.mixer.music.load ( "./resources/backg.mid" )  
pygame.mixer.music.queue ( "./resources/backg.mid" )
pygame.mixer.music.play(-1)


# main loop                                                                                         MAIN LOOP
while running:
    if master.basehelf <= 0:    #game over if base helf <= 0
        master.gameOver(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                running = False
    else:                       #game plays normally
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                master.player.fireGun(master, x, y)
            elif event.type == timer_event:                 #happens every second
                master.damageBase()
                if enemycount < 50:
                    master.spawnEnemy()
        
        #reset screen
        screen.fill((0,0,0))
        master.drawAll(screen)
        pygame.display.update()

        #update all
        master.updateAll()                                  #update gamestate
        
        FramePerSec.tick(120)

