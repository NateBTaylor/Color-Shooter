import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Color Shooter")

health = 5
score = 0

my_font = pygame.font.SysFont('eufm10', 80)
my_font2 = pygame.font.SysFont('eufm10', 60)

tank_image = pygame.image.load('tank.png')
blue_bullet_image = pygame.image.load('blue_bullet.png')
red_bullet_image = pygame.image.load('red_bullet.png')
green_bullet_image = pygame.image.load('green_bullet.png')
red_enemy_image = pygame.image.load('Red_enemy.png')
blue_enemy_image = pygame.image.load('Blue_enemy.png')
green_enemy_image = pygame.image.load('Green_enemy.png')


in_game = True

clock = pygame.time.Clock()

direction = [1, 0]

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

enemy_pos_choices = [[-20, 280], [380, -20], [380, 620], [820, 280]]

timer = 180
old_time = timer

class Player:
  def __init__(self, x, y, size, color, rotation):
    self.x = x
    self.y = y
    self.size = size
    self.color = color
    self.rotation = rotation
  
  def get_rect(self):
    return pygame.Rect(self.x, self.y, self.size, self.size)
  
  def draw(self):
    pygame.draw.rect(screen, player.color, [player.x, player.y, player.size, player.size])

class Bullet:
  def __init__(self, x, y, xvel, yvel, size, color, image):
    self.x = x
    self.y = y 
    self.xvel = xvel
    self.yvel = yvel
    self.size = size
    self.color = color
    self.image = image
  
  def set_vel(self):
    self.xvel = 2 * direction[0]
    self.yvel = 2 * direction[1]

  def update(self):
    self.x += self.xvel
    self.y += self.yvel
  
  def draw(self):
    pygame.draw.rect(screen, bullet.color, [bullet.x, bullet.y, bullet.size, bullet.size])
    screen.blit(self.image, (self.x, self.y))
    
  def get_rect(self):
    return pygame.Rect(self.x, self.y, self.size, self.size)
    
  def get_color(self):
    return self.color

class Enemy:
    def __init__(self, x, y, vel, size, color): 
        self.x = x 
        self.y = y
        self.vel = vel
        self.size = size
        self.color = color

    def update(self):
        if self.x > player.x + 20:
            self.x -= self.vel
        elif self.x < player.x + 20:
            self.x += self.vel
        if self.y < player.y + 20:
            self.y += self.vel
        elif self.y > player.y + 20:
            self.y -= self.vel
            
    def draw(self):
      pygame.draw.rect(screen, enemy.color, [enemy.x, enemy.y, enemy.size, enemy.size])
      if self.color == (0, 0, 255):
        screen.blit(blue_enemy_image, (self.x, self.y))
      if self.color == (0, 255, 0):
        screen.blit(green_enemy_image, (self.x, self.y))
      if self.color == (255, 0, 0):
        screen.blit(red_enemy_image, (self.x, self.y))


    def get_rect(self):
      return pygame.Rect(self.x, self.y, self.size, self.size)
      
    def get_color(self):
      return self.color
            
def collision_check():
  global health, score
  for enemy in enemies:
    if player.get_rect().colliderect(enemy.get_rect()):
      health -= 1
      enemies.remove(enemy)
    for bullet in bullets:
      if bullet.get_rect().colliderect(enemy.get_rect()) and bullet.get_color() == enemy.get_color():
        score += 1
        bullets.remove(bullet)
        enemies.remove(enemy)

def reset_timer():
  global old_time
  if old_time <= 50:
    old_time, new_time = 50, 50
  else:
    old_time, new_time = old_time - 5, old_time - 5
  return new_time
  
player = Player(360, 260, 80, (0, 0, 0), 0)
bullets = []
enemies = []

wait = 0

while in_game:
  screen.fill((135, 206, 235))
  keys = pygame.key.get_pressed()
  
  timer -= 1
  if timer <= wait:
    epos = random.choice(enemy_pos_choices)
    enemies.append(Enemy(epos[0], epos[1], 1, 40, random.choice(colors)))
    timer = reset_timer()
    
  score_text = my_font.render("Score: " + str(score), False, (0, 0, 128))  
  health_text = my_font.render("Health: " + str(health), False, (0, 0, 128))
  end_game_text = my_font2.render("Game Over! Your final score was: " + str(score), False, (0, 0, 128))
    
  screen.blit(score_text,(10,10))
  screen.blit(health_text, (450, 10))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      in_game = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_1:
        bullets.append(Bullet(392, 292, 0, 0, 18, colors[0], red_bullet_image))
        bullet = bullets[-1]
        bullet.set_vel()
      if event.key == pygame.K_2:
        bullets.append(Bullet(392, 292, 0, 0, 18, colors[1], green_bullet_image))
        bullet = bullets[-1]
        bullet.set_vel()
      if event.key == pygame.K_3:
        bullets.append(Bullet(392, 292, 0, 0, 18, colors[2], blue_bullet_image))
        bullet = bullets[-1]
        bullet.set_vel()
      if event.key == pygame.K_DOWN:
        direction = [0, 1]
        player.rotation = 270
      if event.key == pygame.K_UP:
        direction = [0, -1]
        player.rotation = 90
      if event.key == pygame.K_LEFT:
        direction = [-1, 0]
        player.rotation = 180
      if event.key == pygame.K_RIGHT:
        direction = [1, 0]
        player.rotation = 0
  
  player.draw()

  for bullet in bullets:
    bullet.draw()
    bullet.update()

    if bullet.x >= 800 or bullet.x <= -20:
      bullets.remove(bullet)
    if bullet.y >= 600 or bullet.y <= -20:
      bullets.remove(bullet)

  for enemy in enemies:
    enemy.draw()
    enemy.update()

  collision_check()
  
  if health <= 0:
    wait = -500
    screen.blit(end_game_text, (50, 400))
    health = 0
    score = score
    direction = [0, 0]
    if timer <= -400:
      in_game = False

  screen.blit(pygame.transform.rotate(tank_image, player.rotation), (320, 210))

  
  pygame.display.update()

  clock.tick(60)

pygame.quit()
quit()