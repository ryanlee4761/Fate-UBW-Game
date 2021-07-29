import pygame
from sys import exit
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Arcade")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 30)
start_time = 0

#bgm = pygame.mixer.Sound('ubw_bgm.mp3')
#bgm.play(loops=-1)

game_active = False

doublejump = False
player_pull = 0

alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet_keys = [pygame.key.key_code(letter) for letter in alphabet]
numbers = "1234567890"

timed = 0
level = 0
score = 0
currency = 0
blades = 0
counted = 0
shifted = False

background = pygame.image.load('sprites/ubw_background_sprite.jpg').convert()
background = pygame.transform.scale(background, (800, 600))

#display level and score as well
def display_time():
  global level, counted

  current_time = int(pygame.time.get_ticks()/1000) - start_time
  time_surf = test_font.render(f"Time in Seconds: {current_time}", False, (64, 64, 64))
  time_rect = time_surf.get_rect(topleft = (0, 100))
  score_surf = test_font.render(f"Score: {score}", False, (64, 64, 64))
  score_rect = score_surf.get_rect(topleft = (0, 50))
  level_surf = test_font.render(f"Level: {level+1}", False, (64, 64, 64))
  level_rect = level_surf.get_rect(topleft = (0, 0))

  pygame.draw.rect(screen, "#c0e8ec", time_rect)
  pygame.draw.rect(screen, "#c0e8ec", time_rect, 10)
  pygame.draw.rect(screen, "#c0e8ec", score_rect)
  pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
  pygame.draw.rect(screen, "#c0e8ec", level_rect)
  pygame.draw.rect(screen, "#c0e8ec", level_rect, 10)
  screen.blit(time_surf, time_rect)
  screen.blit(score_surf, score_rect)
  screen.blit(level_surf, level_rect)

  if current_time % 15 == 0 and current_time != counted:
    level += 1
    counted = current_time
    
  return current_time

#every other frame?
#SHIFT INCREASES OVER LEVELS
def obstacle_movement(obstacle_list):
  global blades, score, currency, level, timed, time_obstacle_counted, shifted, obstacle_rect_list, obstacle_chr_list
  corresponding_chr = 0
  if obstacle_list:
    for obstacle_rect in obstacle_list:
      obstacle_rect.y += 3 + int(level/2)
      if obstacle_rect.y < 500:
        if not shifted:
          if (player_rect.centerx-2-(level/2)) > obstacle_rect.centerx:
            obstacle_rect.x += 2
            obstacle_rect.x += int(level/2)
          elif (player_rect.centerx+2+(level/2)) < obstacle_rect.centerx:
            obstacle_rect.x -= 2
            obstacle_rect.x -= int(level/2)
      else:
        obstacle_rect.y += 2
        if obstacle_rect.y >= 600:
          blades += 1
          score += 1 + level
          currency += 1 + level
          index = obstacle_rect_list.index(obstacle_rect)
          obstacle_rect_list.remove(obstacle_rect)
          obstacle_chr_list.remove(obstacle_chr_list[index])
        
      letter_surf = test_font.render(chr(obstacle_chr_list[corresponding_chr]).upper(), False, (64, 64, 64))
      letter_rect = letter_surf.get_rect(bottomright = (obstacle_rect.x, obstacle_rect.y))
      pygame.draw.rect(screen, "#c0e8ec", letter_rect)
      screen.blit(weapon_surf, obstacle_rect)
      screen.blit(letter_surf, letter_rect)
      corresponding_chr += 1
    shifted = not shifted
    return obstacle_list
  return []

def collisions(player, obstacles):
  if obstacles:
    for obstacle_rect in obstacles:
      if player.colliderect(obstacle_rect): return False
  return True

def player_animation():
  global player_surf, player_index

  if player_pull > 0:
    player_surf = player_slide_r
  elif player_pull < 0:
    player_surf = player_slide_l
  else:
    player_index += 0.1
    if player_index >= len(player_walk): player_index = 0
    player_surf = player_walk[int(player_index)]

weapon_surf = pygame.image.load('sprites/weapons/axe.png')
weapon_surf = pygame.transform.scale(weapon_surf, (50, 50)).convert_alpha()
weapon_rect = weapon_surf.get_rect(midtop = (random.randint(0, 800), 0))

weapon_list = []
obstacle_rect_list = []
obstacle_chr_list = []

player_walk_1 = pygame.transform.scale(pygame.image.load('sprites/emiyasprite.png').convert_alpha(), (30, 45))
player_walk_2 = pygame.transform.scale(pygame.image.load('sprites/emiyasprite.png').convert_alpha(), (30, 45))
player_slide_l = pygame.transform.scale(pygame.image.load('sprites/emiyasprite.png').convert_alpha(), (30, 45))
player_slide_r = pygame.transform.scale(pygame.image.load('sprites/emiyasprite.png').convert_alpha(), (30, 45))
player_walk = [player_walk_1, player_walk_2]
player_index = 0

player_surf = (player_walk[player_index])
player_rect = player_surf.get_rect(center = (400, 500))

player_stand = pygame.image.load('sprites/emiyasprite.png').convert_alpha()
player_stand_rect = player_stand.get_rect(center=(400, 300))

game_name = test_font.render('UBW RUN', False, (64, 64, 64))
game_rect = game_name.get_rect(center = (400, 150))

game_message = test_font.render('Press space to start!', False, (64, 64, 64))
game_message_rect = game_message.get_rect(center = (400, 450))

spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, 1000 - (level*30))

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

    if game_active:
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT or event.key == pygame.K_LSHIFT:
          if player_rect.centerx == 400:
            player_pull = -25
          elif not doublejump:
            jumpamount = -20-player_pull
            if jumpamount > -5:
              jumpamount = -5
            elif jumpamount < -25:
              if player_rect.centerx > 400:
                jumpamount -= player_pull
              elif player_pull > 0 and player_pull/3 > -25:
                jumpamount -= int(player_pull/3)
              else:
                jumpamount = -20
            player_pull += jumpamount
            doublejump = True

        elif event.key == pygame.K_RIGHT or event.key == pygame.K_RSHIFT:
          if player_rect.centerx == 400:
            player_pull = 25
          elif not doublejump:
            jumpamount = 20-player_pull
            if jumpamount < 5:
              jumpamount = 5
            elif jumpamount > 25:
              if player_rect.centerx < 400 :
                jumpamount -= player_pull
              elif player_pull < 0 and player_pull/3 < 25:
                jumpamount -= int(player_pull/3)
              else:
                jumpamount = 20
            player_pull += jumpamount
            doublejump = True

        elif event.key in obstacle_chr_list:
          blades += 1
          score += 1 + level
          currency += 1 + level
          index = obstacle_chr_list.index(event.key)
          obstacle_chr_list.remove(event.key)
          obstacle_rect_list.remove(obstacle_rect_list[index])

      elif event.type == spawn_timer:
        x_loc = random.randint(0, 800)
        if random.randint(0, 2):
          obstacle_rect_list.append(weapon_surf.get_rect(midtop = (x_loc, 0)))
        else:
          #spawn other weapon skin? 2:38:00
          #save to a list of surfs?
          #need to generate random letter for 

          obstacle_rect_list.append(weapon_surf.get_rect(midtop = (x_loc, 0)))
        obstacle_chr_list.append(random.choice(alphabet_keys))
    else:
      #reset variables
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        game_active = True
        player_rect.centerx = 400
        player_pull = 0
        start_time = int(pygame.time.get_ticks() / 1000)
        level = 0
        score = 0
        currency = 0
        blades = 0
        counted = 0
        shifted = False
        obstacle_rect_list.clear()
        obstacle_chr_list.clear()
  
  if game_active:
    screen.blit(background, (0, 0))
    timed = display_time()

    obstacle_rect_list = obstacle_movement(obstacle_rect_list)

    if player_rect.centerx > 400 and player_pull >= -30: player_pull -= 1
    elif player_rect.centerx < 400 and player_pull <= 30: player_pull += 1

    player_rect.centerx += player_pull
    if player_rect.centerx <= (399+abs(player_pull)) and player_rect.centerx >= (401-abs(player_pull)):
      player_pull = 0
      player_rect.centerx = 400
      doublejump = False
    player_animation()
    screen.blit(player_surf, player_rect)

    game_active = collisions(player_rect, obstacle_rect_list)

  else:
    #check if game is in menu or ended
    screen.fill('Yellow')
    screen.blit(player_stand, player_stand_rect)
    
    score_message = test_font.render(f"You survived for {timed} seconds, dodged {blades} blades, and had a final score of {score}!", False, (64, 64, 64))
    score_message_rect = score_message.get_rect(center = (400, 500))
    screen.blit(game_name, game_rect)
    
    if timed == 0:
      screen.blit(game_message, game_message_rect)
    else:
      screen.blit(score_message, score_message_rect)
  pygame.display.update()
  clock.tick(60)