import pygame
import random
import time
from start_screen import start_screen
from game_over import game_over_screen
from win_screen import win_screen
from player import Player
from boss import Boss
from enemy import Enemy
from bullet import Bullet
from powerup import PowerUp
from boss_bullet import BossBullet
from storage import get_highscore, save_player_score

# -------------------- Initialization --------------------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Blaster")

player_name = start_screen(screen, WIDTH, HEIGHT)

# -------------------- Load Assets --------------------
background = pygame.image.load("assets/background.png")

boss_images = [
    pygame.image.load("assets/boss1.png"),
    pygame.image.load("assets/boss2.png"),
    pygame.image.load("assets/boss3.png"),
    pygame.image.load("assets/boss4.png"),
    pygame.image.load("assets/boss5.png"),
    pygame.image.load("assets/boss6.png")
]

shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
boss_roar_sound = pygame.mixer.Sound("sounds/boss_roar.wav")
boss_fire_sound = pygame.mixer.Sound("sounds/boss_fire.wav")
boss_kill_sound = pygame.mixer.Sound("sounds/boss_kill.wav")
powerup_sound = pygame.mixer.Sound("sounds/powerup.wav")
death_sound = pygame.mixer.Sound("sounds/faaaah.wav")

shoot_sound.set_volume(0.4)
boss_roar_sound.set_volume(0.8)
boss_fire_sound.set_volume(0.6)
boss_kill_sound.set_volume(0.8)
powerup_sound.set_volume(0.6)
death_sound.set_volume(1.0)

clock = pygame.time.Clock()

player = Player(500, 600)
heart_img = pygame.image.load("assets/heart.png")

font = pygame.font.SysFont(None, 30)
digit_font = pygame.font.Font("assets/digital-7.ttf", 40)
large_font = pygame.font.SysFont(None, 80)

# -------------------- Game Variables --------------------
bullets = []
enemies = []
powerups = []
boss_bullets = []

boss = None

score = 0
highscore = get_highscore()

missed_enemies = 0
MAX_MISSED = 10
player_lives = 3

enemy_spawn_timer = 0
ENEMY_SPAWN_DELAY = 30

boss_fire_timer = 0
BOSS_FIRE_DELAY = 90

# -------------------- LEVEL SYSTEM --------------------
level = 1
#score = 1200
MAX_LEVEL = 6
BOSS_SCORE_INTERVAL = 200

level_text_timer = 0
LEVEL_TEXT_DURATION = 120

boss_warning_timer = 0
BOSS_WARNING_DURATION = 90

game_won = False

# -------------------- Screen Shake --------------------
shake_timer = 0
SHAKE_DURATION = 20
SHAKE_INTENSITY = 10

# Initial enemy
enemies.append(Enemy(random.randint(0, WIDTH-50), -50))

running = True

# -------------------- Main Loop --------------------
while running:
    clock.tick(60)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(player.shoot())
                shoot_sound.play()

    # PLAYER
    keys = pygame.key.get_pressed()
    player.move(keys)

    # Difficulty scaling
    ENEMY_SPAWN_DELAY = max(10, 30 - level * 2)

    # -------------------- Enemy Spawn --------------------
    if boss is None:
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= ENEMY_SPAWN_DELAY:
            if len(enemies) < 10:
                enemies.append(Enemy(random.randint(0, WIDTH-50), -50))
            enemy_spawn_timer = 0

    # -------------------- Boss Spawn --------------------
    if score >= BOSS_SCORE_INTERVAL * level and boss is None and level <= MAX_LEVEL:
        boss = Boss(300, 50, level=level)

        boss.image = boss_images[min(level-1, len(boss_images)-1)]
        boss.health = 20 + (level-1) * 10

        boss_roar_sound.play()
        shake_timer = SHAKE_DURATION
        boss_warning_timer = BOSS_WARNING_DURATION

    # -------------------- Bullets --------------------
    for bullet in bullets[:]:
        bullet.move()
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    # -------------------- Enemies --------------------
    for enemy in enemies[:]:
        enemy.move()

        if enemy.rect.top > HEIGHT:
            enemies.remove(enemy)
            missed_enemies += 1
            if missed_enemies >= MAX_MISSED:
                death_sound.play()
                pygame.time.wait(int(death_sound.get_length()*1000))
                running = False

        if enemy.rect.colliderect(player.rect):
            enemies.remove(enemy)
            player_lives -= 1
            if player_lives <= 0:
                death_sound.play()
                pygame.time.wait(int(death_sound.get_length()*1000))
                running = False

    # -------------------- Boss --------------------
    if boss:
        boss.move()

        boss_fire_timer += 1
        if boss_fire_timer >= BOSS_FIRE_DELAY:
            boss_bullets.append(BossBullet(boss.rect.centerx, boss.rect.bottom))
            boss_fire_sound.play()
            boss_fire_timer = 0

        for bullet in bullets[:]:
            if boss and bullet.rect.colliderect(boss.rect):
                boss.health -= 1
                bullets.remove(bullet)

                if boss.health <= 0:
                    boss_kill_sound.play()
                    boss = None
                    score += 50

                    # FINAL BOSS → WIN
                    if level >= MAX_LEVEL:
                        game_won = True
                        running = False
                    else:
                        level += 1
                        level_text_timer = LEVEL_TEXT_DURATION

        if boss and boss.rect.colliderect(player.rect):
            player_lives -= 1
            if player_lives <= 0:
                death_sound.play()
                pygame.time.wait(int(death_sound.get_length()*1000))
                running = False

    # -------------------- Boss Bullets --------------------
    for b_bullet in boss_bullets[:]:
        b_bullet.move()

        if b_bullet.rect.top > HEIGHT:
            boss_bullets.remove(b_bullet)

        elif b_bullet.rect.colliderect(player.rect):
            player_lives -= 1
            boss_bullets.remove(b_bullet)

            if player_lives <= 0:
                death_sound.play()
                pygame.time.wait(int(death_sound.get_length()*1000))
                running = False

    # -------------------- Bullet vs Enemy --------------------
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10

                if random.randint(1, 5) == 1:
                    powerups.append(PowerUp(enemy.rect.x, enemy.rect.y))
                break

    # -------------------- Powerups --------------------
    for p in powerups[:]:
        p.move()
        if p.rect.colliderect(player.rect):
            powerup_sound.play()
            if player_lives < 3:
                player_lives += 1
            powerups.remove(p)

    # -------------------- Screen Shake --------------------
    offset_x, offset_y = 0, 0
    if shake_timer > 0:
        offset_x = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
        offset_y = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
        shake_timer -= 1

    # -------------------- Draw --------------------
    screen.blit(background, (offset_x, offset_y))

    player.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    for p in powerups:
        p.draw(screen)

    for b_bullet in boss_bullets:
        b_bullet.draw(screen)

    if boss:
        boss.draw(screen)
        pygame.draw.rect(
            screen, (255, 0, 0),
            (
                boss.rect.x + offset_x,
                boss.rect.y - 10 + offset_y,
                boss.rect.width * (boss.health / (30 + (level-1)*20)),
                5
            )
        )

    # -------------------- HUD --------------------
    for i in range(player_lives):
        screen.blit(heart_img, (20 + i*40, 140))

    screen.blit(digit_font.render(f"Score: {score}", True, (0,255,0)), (20, 20))
    screen.blit(digit_font.render(f"High: {highscore}", True, (0,255,255)), (20, 60))
    screen.blit(font.render(f"Missed: {missed_enemies}/{MAX_MISSED}", True, (255,255,255)), (20,100))

    # LEVEL TEXT
    if level_text_timer > 0:
        level_text_timer -= 1
        txt = large_font.render(f"LEVEL {level}", True, (255,255,0))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))

    # BOSS WARNING
    if boss_warning_timer > 0:
        boss_warning_timer -= 1
        warn = large_font.render("BOSS INCOMING!", True, (255,50,50))
        screen.blit(warn, (WIDTH//2 - warn.get_width()//2, HEIGHT//3))

    pygame.display.update()

# -------------------- SAVE --------------------
save_player_score(player_name, score, level)

# -------------------- END SCREEN --------------------
if game_won:
    restart = win_screen(screen, WIDTH, HEIGHT, score, level, player_name)
else:
    restart = game_over_screen(screen, WIDTH, HEIGHT, score, highscore, level, player_name)

if restart:
    pygame.quit()
    import subprocess, sys
    subprocess.call([sys.executable, "main.py"])