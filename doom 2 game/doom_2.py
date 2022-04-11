from pygame import *
from random import *
 
clock = time.Clock()
gamescreen = display.set_mode((800, 600))
 
class Base(sprite.Sprite):
    def __init__(self, name, x, y, w = 500, h = 1000):
        super().__init__()
        self.image = image.load(name)
        self.image = transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        gamescreen.blit(self.image, self.rect)
 
class Player(Base):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x <= 800:
            self.rect.x += 5
        if keys[K_a] and self.rect.x >= 0:
            self.rect.x -= 5
    def shoot(self):
        global score
        shot.play()
        if score<10:
            b1 = Bullet('bullet.png', self.rect.x+20, self.rect.y+5, 10, 20)
            fire.add(b1)
        elif score<20:
            b1 = Bullet('bullet.png', self.rect.x+10, self.rect.y+5, 10, 20)
            b2 = Bullet('bullet.png', self.rect.x+30, self.rect.y+5, 10, 20)
            fire.add(b1, b2)
        elif score<30:
            b1 = Bullet('bullet.png', self.rect.x, self.rect.y+5, 10, 20)
            b2 = Bullet('bullet.png', self.rect.x+20, self.rect.y+5, 10, 20)
            b3 = Bullet('bullet.png', self.rect.x+40, self.rect.y+5, 10, 20)
            fire.add(b1, b2, b3)
        else:
            b1 = Bullet('bullet.png', self.rect.x+5, self.rect.y+5, 30, 60)
            fire.add(b1)
        
class Bullet(Base):
    def update(self):
        self.rect.y -= 5
        if self.rect.y < 0:
            fire.remove(self)
 
class Enemy(Base):
    def update(self):
        global health
        self.rect.y += 2
        if self.rect.y >= 600:
            self.rect.y = -50
            self.rect.x = randint(0, 750)
            health -= 1
        if sprite.spritecollide(self, fire, True):
            self.rect.y = -50
            self.rect.x = randint(0, 750)
            global score
            score += 1
        if sprite.collide_rect(self, hero):
            health -= 1
            self.rect.y = -25
            self.rect.x = randint(0, 1000)

class Asteroid  (Base):
    def update(self):
        self.rect.y += 2
        if self.rect.y >= 600:
            self.rect.y = -50
            self.rect.x = randint(0, 750)         
        if sprite.collide_rect(self, hero):
            global health
            health -=1
            self.rect.y = -50
            self.rect.x = randint(0, 750)

class Boss(Base):
    def start_hp(self):
        self.hp = 23
        self.side = 1
    def update(self):
        self.rect.x += self.side
        if self.rect.x < 200 or self.rect.x > 400:
            self.side = - self.side
 
        self.rect.y += 1
        if self.rect.y >= 600 or sprite.collide_rect(self, hero):
            global health
            health = 0
        if sprite.spritecollide(self, fire, True):
            self.hp -= 1
 
hero = Player('player.png', 500, 500, 50, 50)
enem = Enemy('enemy.png',randint(0, 800), -50, 50, 50)
enem2 = Enemy('enemy.png',randint(0, 800), -50, 50, 50)
enem3 = Enemy('enemy.png',randint(0, 800), -50, 50, 50)
enem4 = Enemy('enemy.png',randint(0, 800), -50, 50, 50)
fire = sprite.Group()
enemies = sprite.Group()
enemies.add(enem, enem2, enem3, enem4)
bg = image.load('galaxy.jpg')
bg = transform.scale(bg, (800, 600))
big_boss = Boss('boss.png', 300, -200, 125, 125)
big_boss.start_hp()
 
a1 = Asteroid('asteroid.png', -50, randint(0, 750), 100, 100)

health = 5
score = 0

font.init()
shrift = font.Font(None, 35)
mixer.init()
shot = mixer.Sound('fire.ogg')
mixer.music.load('space1.mp3')
mixer.music.play(-1)
bossmusic = 0
 
while health  > 0:
    for e in event.get():
        if e.type == QUIT:
            quit()
            exit()
        if e.type == MOUSEBUTTONDOWN:
            hero.shoot()
 
    gamescreen.blit(bg, (0, 0))
    hero.update()
    hero.reset()

    a1.update()
    a1.reset()

 
    fire.update()
    fire.draw(gamescreen)
 
    health_txt = shrift.render('Здоровье : ' +str(health), 1, (255, 0, 0))
    gamescreen.blit(health_txt, (0, 0))
 
    score_txt = shrift.render('Счёт : ' +str(score), 1, (0, 0, 0))
    gamescreen.blit(score_txt, (0, 40))
 
    if score >= 25:
        if bossmusic == 0:
            mixer.music.stop()
            mixer.music.load('space.mp3')
            mixer.music.play(-1)
            bossmusic = 1
        big_boss.update()
        big_boss.reset()
        if big_boss.hp <= 0:
            gamescreen.blit(bg, (0, 0))
            end = shrift.render('ПОБЕДА', 1, (255, 0, 0))
            gamescreen.blit(end, (200, 200))
            gamescreen.blit(score_txt, (200, 250))
            display.update()
            time.delay(3000)
            quit()
            exit()
    else:
        enemies.update()
        enemies.draw(gamescreen)
 
    display.update()
    clock.tick(75)  
 
gamescreen.blit(bg, (0, 0))
end = shrift.render('Поражение', 1, (255, 0, 0))
gamescreen.blit(end, (200, 200))
gamescreen.blit(score_txt, (200, 250))
display.update()
time.delay(3000)
 
 

