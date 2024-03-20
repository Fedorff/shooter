from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('music.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.3)
fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.2)

window = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
display.set_caption('QWERTY')
enemy_random = randint(1, 699)
lost = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect))
    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('pulka.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y >= 450:
            self.direction2 = 'up'
        if self.rect.y <= 5:
            self.direction2 = 'down'
        if self.direction2 == 'up':
           lost += 1
           enemy_random = randint(1, 699)
           self.rect.y = 4
           self.rect.x = enemy_random
        if self.direction2 == 'down':
           self.rect.y += self.speed
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player('player.png', 300, 420, 65, 65, 15)
#enemy = Enemy('ufo.png', 300, 4, 2)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(20, 680), 4, 65, 65, 3)
    monsters.add(enemy)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(20, 680), 4, 65, 65, 3)
    asteroids.add(asteroid)
font.init()
font1 = font.SysFont('Arial', 20)
font2 = font.SysFont('Arial', 80)
win = font2.render('YOU WIN', True, (0, 255, 0))
lose = font2.render('YOU LOSE', True, (255, 0, 0))


finish = False
run = True
rel_time = False
num_fire = 0
live = 3
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <5 and rel_time != True:
                    fire_sound.play()
                    player.fire()
                    num_fire += 1
                if num_fire >=5 and rel_time != True:
                    rel_time = True
                    last_time = timer()
    if not finish:
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text = font1.render("Счёт: " + str(score), 1, (255, 255, 255))
        text_l = font1.render("Хп: " + str(live), 1, (255, 255, 255))
        window.blit(background, (0, 0))
        window.blit(text_lose, (1, 1))
        window.blit(text, (1, 20))
        window.blit(text_l, (1, 39))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        collides = sprite.groupcollide(bullets, monsters, True, True)
        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('ПЕРЕЗАРЯДКА', True, (100,200,100))
                window.blit(reload, (250,450))
            else:
                num_fire = 0
                rel_time = False
        for i in collides:
            score += 1
            enemy = Enemy('ufo.png', randint(20, 680), 4, 65, 65, 3)
            monsters.add(enemy)
        if sprite.spritecollide(player, monsters, False) and live == 1:
            window.blit(lose, (150, 150))
            finish = True
        if sprite.spritecollide(player, asteroids, False) and live == 1:
            window.blit(lose, (150, 150))
            finish = True
        if sprite.spritecollide(player, monsters, True):
            live -= 1
        if sprite.spritecollide(player, asteroids, True):
            live -= 1
        if score > 29:
            window.blit(win, (150, 150))
            finish = True
        #if live < 1:
        #    window.blit(lose, (150, 150))
    else:
        finish = False
        score = 0
        lost = 0
        live = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(5):
            enemy = Enemy('ufo.png', randint(1, 699), 4, 65, 65, 3)
            monsters.add(enemy)
        for i in range(3):
            asteroid = Enemy('asteroid.png', randint(20, 680), 4, 65, 65, 3)
            asteroids.add(asteroid)
    display.update()
    time.delay(20)