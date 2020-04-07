#Music Credits: Jan125, https://opengameart.org/content/stereotypical-90s-space-shooter-music

# Import libraries
import pygame as py
import random as rn
import pickle as pk
from os import path

# Declare path from image and sound folder
img_dir = path.join(path.dirname(__file__), 'src/img')
snd_dir = path.join(path.dirname(__file__), 'src/snd')

# Game settings
width = 1024
height = 768
fps = 60
game_speed = 2
player_speed = 7
bullet_speed = 7
player_speed1 = 7
player_speed2 = 6
player_speed3 = 5
bullet_speed1 = 7
bullet_speed2 = 6
bullet_speed3 = 5

# Define colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (3,173,76)
blue = (0,0,255)

# Load Highscore
try:
    with open('highscore.dat', 'rb') as file:
        highscore = pk.load(file)
except:
    highscore = 0

# Initialize pygame and create window
py.mixer.pre_init(44100, -16, 2, 2048)
py.mixer.init()
py.init()
screen = py.display.set_mode((width,height))
py.display.set_caption('Land Runner')
py.mouse.set_visible(0)
clock = py.time.Clock()

# Definition for drawing text
def draw_text(surf, text, size, x, y, color):
    font = py.font.Font(path.join(path.dirname(__file__), 'src/font/galaxy-monkey.regular.ttf'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midbottom = (x, y)
    surf.blit(text_surface, text_rect)

# Definition for spawning rocks
def newmob():
    m = mob()
    all_sprites.add(m)
    mobs.add(m)

# Definition for spawning enemies
def newenemy():
    e = enemy()
    all_sprites.add(e)
    enemies.add(e)

# Definition for start screen
def start_screen():
    craft = startscreen_ship()
    startscreen_sprites.add(craft)
    lastupdate = py.time.get_ticks()
    waiting = True
    #joystick = py.joystick.Joystick(0)
    #joystick.init()
    while waiting:
        #button = joystick.get_button(0)
        key = py.key.get_pressed()
        nowupdate = py.time.get_ticks()
        clock.tick(fps)
        BackGround.update(screen)
        startscreen_sprites.update()
        startscreen_sprites.draw(screen)
        draw_text(screen, str(highscore), 72, width/2, height/2, white)
        for event in py.event.get():
            if event.type == py.QUIT or key[py.K_ESCAPE]:
                py.quit()
            if key[py.K_SPACE]:
                if nowupdate - lastupdate >2000:
                    craft.kill()
                    waiting = False
            #if button:
                #if nowupdate - lastupdate > 2000:
                    #craft.kill()
                    #waiting = False
        py.display.flip()
    
def gameoverscreen():
    gameover = True
    lastcheck = py.time.get_ticks()
    while gameover:
        nowcheck = py.time.get_ticks()
        BackGround.update(screen)
        draw_text(screen, 'Score', 72, width/2, height/2 -80, white)
        draw_text(screen, str(score), 72, width/2, height/2, white)
        if nowcheck - lastcheck > 3000:
            gameover = False
        py.display.flip()



# Scrolling Background
class background(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image = bg_img
        self.rect = self.image.get_rect()
        self.y1 = 0
        self.y2 = height * -1

    def update(self, screen):
        screen.blit(self.image, (0, self.y1))
        screen.blit(self.image, (0, self.y2))
        self.y1 += game_speed
        self.y2 += game_speed

        if self.y1 > height:
            self.y1 = self.y2 - height
        if self.y2 > height:
            self.y2 = self.y1 - height

# Creating startscreen player
class startscreen_ship(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image = start_img[0]
        self.image.set_colorkey(black)
        #self.image.fill(green)
        self.rect = self.image.get_rect()
        self.radius = 28
        self.rect.centerx = width / 2
        self.rect.bottom = height
        self.last = py.time.get_ticks()
        
    def update(self):
        now = py.time.get_ticks()
        if now - self.last > 200:
            self.image = start_img[1]
            self.image.set_colorkey(black)
        if now - self.last > 400:
            self.image = start_img[0]
            self.image.set_colorkey(black)
            self.last = now
            
# Creating player sprite
class player(py.sprite.Sprite):
    def __init__(self):
        # Built in sprite init function
        py.sprite.Sprite.__init__(self)
        self.image = player_img[0]
        self.image.set_colorkey(black)
        #self.image.fill(green)
        self.rect = self.image.get_rect()
        self.radius = 28
        #py.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.centerx = width / 2
        self.rect.bottom = height - 40
        self.speed_x = 0
        self.speed_y = 0
        self.last = py.time.get_ticks()
        self.last_bullet = py.time.get_ticks()

    def animation(self):
        now = py.time.get_ticks()
        if now - self.last > 200:
            self.image = player_img[1]
            self.image.set_colorkey(black)
        if now - self.last > 400:
            self.image = player_img[0]
            self.image.set_colorkey(black)
            self.last = now


    # Bewegungen die der Spieler machen kann
    def update(self):
        self.animation()
        self.speed_x = 0
        self.speed_y = 0
        key = py.key.get_pressed()
        #joystick = py.joystick.Joystick(0)
        #joystick.init()
        #updown = joystick.get_axis(1)
        #rightleft = joystick.get_axis(0)

        # Rechts links steuerung und Border
        if key[py.K_LEFT]:
            self.speed_x = player_speed *-1
        if key[py.K_RIGHT]:
            self.speed_x = player_speed
        self.rect.x += self.speed_x
        if self.rect.right > width -200:
            self.rect.right = width -200
        if self.rect.left < 200:
            self.rect.left = 200
        # Hoch runter steuerung und Border
        if key[py.K_UP]:
            self.speed_y = -1 * player_speed
        if key[py.K_DOWN]:
            self.speed_y = player_speed
        self.rect.y += self.speed_y
        if self.rect.top < 40:
            self.rect.top = 40
        if self.rect.bottom > height - 10:
            self.rect.bottom = height - 10

    def shoot(self):
        bullet_now = py.time.get_ticks()
        if bullet_now - self.last_bullet > 300:
            bullet = Bullet(self.rect.centerx, self.rect.top + 20)
            all_sprites.add(bullet)
            bullets.add(bullet)  # add bullet to a group, so we can add collision
            self.last_bullet = bullet_now
            shoot_sound.play()

# Creating enemy sprite
class enemy(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image = enemyship_img[0]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 28
        #py.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = rn.randrange(200, width - 200 - self.rect.width)
        self.rect.y = rn.randrange(-500, -300)
        self.speed_y = game_speed + 1
        self.last = py.time.get_ticks()
        self.lastshot = py.time.get_ticks()
        self.shootcount = 0
        self.shootplace = rn.randrange(0, height/4)
        self.shoottimer = rn.randrange(300, 1000)
        self.shotallow = rn.randrange(1,3)
        self.speed_x = rn.randrange(-1, 1)

    def animation(self):
        now = py.time.get_ticks()
        if now - self.last > 200:
            self.image = enemyship_img[1]
            self.image.set_colorkey(black)
        if now - self.last > 400:
            self.image = enemyship_img[0]
            self.image.set_colorkey(black)
            self.last = now

    def update(self):
        self.animation()
        self.movex()
        self.speed_y = game_speed + 1
        self.rect.y += self.speed_y
        if self.rect.y > self.shootplace:
            self.shoot()

    def shoot(self):
        ebulletnow = py.time.get_ticks()
        if self.shootcount < self.shotallow:
            if ebulletnow - self.lastshot > self.shoottimer:
                enemybullet = Enemybullet(self.rect.centerx, self.rect.bottom)
                all_sprites.add(enemybullet)
                enemybullets.add(enemybullet)  # add bullet to a group, so we can add collision
                shoot_sound.play()
                self.shootcount += 1
                self.lastshot = ebulletnow

    def movex(self):
        if score >= 80:
            self.rect.x += self.speed_x
            if self.rect.left < 200 or self.rect.right > width - 200:
                self.speed_x = self.speed_x * -1

# Creating rock sprite
class mob(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.image.set_colorkey(black)
        #self.image.fill(red)
        self.rect = self.image.get_rect()
        self.radius = 25
        #py.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.x = rn.randrange(200, width - 200 - self.rect.width)
        self.rect.y = rn.randrange(-2000, -400)
        self.speed_y = game_speed

    def update(self):
        self.speed_y = game_speed
        self.rect.y += self.speed_y
        #self.rect.x += self.speed_x
        #if self.rect.left < 82 or self.rect.right > width - 82:
            #self.speed_x = self.speed_x * -1
        #if self.rect.top > height + 10:
            #self.rect.x = rn.randrange(82, width - 82 - self.rect.width)
            #self.rect.y = rn.randrange(-3000, -200)
            #self.speed_y = game_speed

# Creating bullet sprite
class Bullet(py.sprite.Sprite):
    def __init__(self, x, y):
        py.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(black)
        #self.image.fill(white)
        self.rect = self.image.get_rect()
        self.radius = 8
        #py.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -1 * bullet_speed

    def update(self):
        self.rect.y += self.speed_y
        # remove if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# Creating enemybullet sprite
class Enemybullet(py.sprite.Sprite):
    def __init__(self, x, y):
        py.sprite.Sprite.__init__(self)
        self.image = enemybullet_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 8
        self.rect.top = y
        self.rect.centerx = x
        self.speed_y = game_speed + bullet_speed

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > height:
            self.kill()

# Creating explosion sprite
class explosion(py.sprite.Sprite):
    def __init__(self, center, size):
        py.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = -1
        self.last_update = py.time.get_ticks()
        self.frame_rate = 30
        self.speed_y = game_speed

    def update(self):
        self.rect.y += game_speed
        now = py.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Creating border sprite
class border(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image = py.Surface((1024, 10))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = height + 100

# Load all game graphics
start_img1 = py.image.load(path.join(img_dir, "startscreen1.png")).convert()
start_img2 = py.image.load(path.join(img_dir, "startscreen2.png")).convert()
start_img = [start_img1, start_img2]
bg_img = py.image.load(path.join(img_dir, "bg.png")).convert()
player_img1 = py.transform.scale(py.image.load(path.join(img_dir, "player1.png")).convert(), (72, 92))
player_img2 = py.transform.scale(py.image.load(path.join(img_dir, "player2.png")).convert(), (72, 92))
player_img = [player_img1, player_img2]
bullet_img = py.transform.scale(py.image.load(path.join(img_dir, "bullet.png")).convert(), (20,30))
enemybullet_img = py.transform.scale(py.image.load(path.join(img_dir, "bulletenemy.png")).convert(), (20,30))
enemy_img = py.transform.scale(py.image.load(path.join(img_dir, "enemy.png")).convert(), (70,80))
enemyship_img1 = py.transform.scale(py.image.load(path.join(img_dir, "enemyship1.png")).convert(), (72, 92))
enemyship_img2 = py.transform.scale(py.image.load(path.join(img_dir, "enemyship2.png")).convert(), (72, 92))
enemyship_img = [enemyship_img1, enemyship_img2]
explosion_animation = {}
explosion_animation['lg'] = []
explosion_animation['sm'] = []
for i in range(8):
    filename = 'explosion-{}.png'.format(i)
    img = py.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    img_lg = py.transform.scale(img, (60,60))
    explosion_animation['lg'].append(img_lg)
    img_sm = py.transform.scale(img, (25,25))
    explosion_animation['sm'].append(img_sm)

# Load all game sounds
shoot_sound = py.mixer.Sound(path.join(snd_dir, "lasershoot.wav"))
shoot_sound.set_volume(0.25)
explosion_enemy_sound = py.mixer.Sound(path.join(snd_dir, "explosionenemy.wav"))
explosion_enemy_sound.set_volume(0.25)
explosion_player_sound = py.mixer.Sound(path.join(snd_dir, "explosionplayer.wav"))
explosion_player_sound.set_volume(0.25)
explosion_bullet_sound = py.mixer.Sound(path.join(snd_dir, "explosionbullet.wav"))
explosion_bullet_sound.set_volume(0.05)
py.mixer.music.load(path.join(snd_dir, "theme.ogg"))
py.mixer.music.set_volume(0.15)

# Start scrolling Background
BackGround = background()

# Start playing game music
py.mixer.music.play(loops=-1)

# Groups
startscreen_sprites = py.sprite.Group()

#----------Game Loop----------#
game_over = True
run = True
while run:
    if game_over:
        start_screen()
        game_over = False
        # All the sprites
        all_sprites = py.sprite.Group()
        enemies = py.sprite.Group()
        bullets = py.sprite.Group()
        enemybullets = py.sprite.Group()
        Player = player()
        Border = border()
        mobs = py.sprite.Group()
        all_sprites.add(Player)
        all_sprites.add(Border)
        for i in range(6):
            newmob()
        for i in range(1):
            newenemy()

        #add score
        score = 0
        counter = 0
    clock.tick(fps)
    # Game speed

    if score >= 5:#5
        if counter == 0:
            fps = 80
            player_speed = player_speed2
            bullet_speed = bullet_speed2
            counter = 1
    if score >= 10:#15
        if counter == 1:
            newenemy()
            counter = 2
    if score >= 20:#25
        if counter == 2:
            fps = 100
            player_speed = player_speed3
            bullet_speed = bullet_speed3
            counter = 3
    if score >= 30:#40
        if counter == 3:
            fps = 60
            game_speed = 3
            player_speed = player_speed1
            bullet_speed = bullet_speed1
            counter = 4
    if score >= 50:#55
        if counter == 4:
            fps = 80
            player_speed = player_speed2
            bullet_speed = bullet_speed2
    if score >= 70:#80
        fps = 100
        bullet_speed = bullet_speed3
        player_speed = player_speed3


    #initialize variables
    key = py.key.get_pressed()
    # Keep loop running at the right speed

    # Process input
    for event in py.event.get():
        #check for closing window
        if event.type == py.QUIT or key[py.K_ESCAPE]:
            run = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                Player.shoot()


    # Update
    all_sprites.update()

    # Check to see if a bullet hits enemies
    bullethits = py.sprite.groupcollide(enemies, bullets, True, True, py.sprite.collide_circle)
    for hit in bullethits:
        score += 1
        explosion_enemy_sound.play()
        expl = explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newenemy()
    # Check to see if a bullet hits rock
    rockhits = py.sprite.groupcollide(bullets, mobs, True, False, py.sprite.collide_circle)
    for hit in rockhits:
        explosion_bullet_sound.play()
        explsm = explosion(hit.rect.center, 'sm')
        all_sprites.add(explsm)
    # Check to see if a mob hits the border
    mobdodge = py.sprite.spritecollide(Border, mobs, True)
    if mobdodge:
        newmob()
    enemydodge = py.sprite.spritecollide(Border, enemies, True)
    if enemydodge:
        newenemy()
    # Check to see if a mob hit the player
    hits = py.sprite.spritecollide(Player, mobs, True, py.sprite.collide_circle)
    if hits:
        explosion_player_sound.play()
        death_explosion = explosion(Player.rect.center, 'lg')
        all_sprites.add(death_explosion)
        Player.kill()
    hits2 = py.sprite.spritecollide(Player, enemies, True, py.sprite.collide_circle)
    if hits2:
        explosion_player_sound.play()
        death_explosion = explosion(Player.rect.center, 'lg')
        all_sprites.add(death_explosion)
        Player.kill()
    hits3 = py.sprite.spritecollide(Player, enemybullets, True, py.sprite.collide_circle)
    if hits3:
        explosion_player_sound.play()
        death_explosion = explosion(Player.rect.center, 'lg')
        all_sprites.add(death_explosion)
        Player.kill()


    if not Player.alive() and not death_explosion.alive():
        if score > highscore:
            highscore = score
        with open('highscore.dat', 'wb') as file:
            pk.dump(highscore, file)
        game_speed = 2
        fps = 60
        bullet_speed = 7
        player_speed = 7
        game_over = True
        gameoverscreen()


    # Draw / Render
    screen.fill(black)
    BackGround.update(screen)
    draw_text(screen, str(score), 80, width / 2, 90, green)
    all_sprites.draw(screen)

    # After drawing everything ,flip the display
    py.display.flip()

py.quit()
