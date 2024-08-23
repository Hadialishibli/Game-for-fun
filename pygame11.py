import pygame
import random
import math

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Game")

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Player settings
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 10
player_speed = 5
last_direction = 'UP'
player_health = 100

# Bullet settings
bullets = []
bullet_speed = 7

# Box settings
box_size = 20
boxes = [[random.randint(0, WIDTH-box_size), random.randint(0, HEIGHT-box_size)] for _ in range(10)]

# Enemy settings
enemy_pos = [(0, 0), (WIDTH - 10, 0), (0, HEIGHT - 10), (WIDTH - 10, HEIGHT - 10)]
enemy_bullets = []
enemy_bullet_speed = 5
enemy_shoot_interval = 100  # Lower value means more frequent shooting

# Score settings
score = 0
level = 1
font = pygame.font.Font(None, 36)

# Game state
game_over = False
winner = False

clock = pygame.time.Clock()

def move_player(keys, player_pos):
    global last_direction
    if keys[pygame.K_w]:
        player_pos[1] -= player_speed
        last_direction = 'UP'
    if keys[pygame.K_s]:
        player_pos[1] += player_speed
        last_direction = 'DOWN'
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
        last_direction = 'LEFT'
    if keys[pygame.K_d]:
        player_pos[0] += player_speed
        last_direction = 'RIGHT'

    # Teleport player to the opposite side if they go out of bounds
    if player_pos[0] < 0:
        player_pos[0] = WIDTH
    elif player_pos[0] > WIDTH:
        player_pos[0] = 0
    if player_pos[1] < 0:
        player_pos[1] = HEIGHT
    elif player_pos[1] > HEIGHT:
        player_pos[1] = 0

def shoot_bullet(player_pos):
    bullet_pos = player_pos[:]
    bullets.append((bullet_pos, last_direction))

def move_bullets():
    for bullet in bullets:
        pos, direction = bullet
        if direction == 'UP':
            pos[1] -= bullet_speed
        elif direction == 'DOWN':
            pos[1] += bullet_speed
        elif direction == 'LEFT':
            pos[0] -= bullet_speed
        elif direction == 'RIGHT':
            pos[0] += bullet_speed

        if pos[0] < 0 or pos[0] > WIDTH or pos[1] < 0 or pos[1] > HEIGHT:
            bullets.remove(bullet)

def check_collisions():
    global score, game_over, player_health, winner
    for bullet in bullets:
        pos, _ = bullet
        for box in boxes:
            if (box[0] < pos[0] < box[0] + box_size) and (box[1] < pos[1] < box[1] + box_size):
                boxes.remove(box)
                bullets.remove(bullet)
                score += 1
                if score >= 20:
                    winner = True
                break

    if not boxes:
        respawn_boxes()

    for bullet in enemy_bullets:
        if (player_pos[0] - player_size < bullet[0] < player_pos[0] + player_size) and (player_pos[1] - player_size < bullet[1] < player_pos[1] + player_size):
            player_health -= 10
            enemy_bullets.remove(bullet)
            if player_health <= 0:
                game_over = True

def respawn_boxes():
    global boxes
    boxes = [[random.randint(0, WIDTH-box_size), random.randint(0, HEIGHT-box_size)] for _ in range(10)]

def shoot_enemy_bullets():
    for pos in enemy_pos:
        direction = get_direction_to_player(pos)
        enemy_bullets.append([pos[0] + 5, pos[1] + 5, direction[0], direction[1]])

def get_direction_to_player(pos):
    dx = player_pos[0] - pos[0]
    dy = player_pos[1] - pos[1]
    dist = math.hypot(dx, dy)
    return dx / dist, dy / dist

def move_enemy_bullets():
    for bullet in enemy_bullets:
        bullet[0] += bullet[2] * enemy_bullet_speed
        bullet[1] += bullet[3] * enemy_bullet_speed

        if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
            enemy_bullets.remove(bullet)

def reset_game(next_level=False):
    global player_pos, bullets, boxes, enemy_bullets, score, game_over, player_health, winner, enemy_shoot_interval, level
    player_pos = [WIDTH // 2, HEIGHT // 2]
    bullets = []
    enemy_bullets = []
    score = 0
    player_health = 100
    game_over = False
    winner = False
    if next_level:
        enemy_shoot_interval -= 5
        level += 1
        if enemy_shoot_interval <= 0:
            game_over = True
    else:
        enemy_shoot_interval = 100
        level = 1
    respawn_boxes()

def draw_button(text, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, GREEN, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, BLUE, (x, y, w, h))

    button_text = font.render(text, True, WHITE)
    screen.blit(button_text, (x + (w / 2 - button_text.get_width() / 2), y + (h / 2 - button_text.get_height() / 2)))

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                shoot_bullet(player_pos)
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            reset_game()
        if event.type == pygame.MOUSEBUTTONDOWN and winner:
            reset_game(next_level=True)

    if not game_over and not winner:
        keys = pygame.key.get_pressed()
        move_player(keys, player_pos)
        move_bullets()
        move_enemy_bullets()
        check_collisions()

        if random.randint(0, enemy_shoot_interval) == 0:
            shoot_enemy_bullets()

        pygame.draw.circle(screen, RED, player_pos, player_size)
        for bullet in bullets:
            pygame.draw.circle(screen, GREEN, bullet[0], 5)
        for box in boxes:
            pygame.draw.rect(screen, BLUE, (*box, box_size, box_size))
        for pos in enemy_pos:
            pygame.draw.circle(screen, ORANGE, pos, 10)
        for bullet in enemy_bullets:
            pygame.draw.circle(screen, YELLOW, bullet[:2], 5)

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Display health
        health_text = font.render(f"Health: {player_health}", True, WHITE)
        screen.blit(health_text, (WIDTH - 150, 10))

        # Display enemy shoot interval
        interval_text = font.render(f"Enemy Shoot Interval: {enemy_shoot_interval}", True, WHITE)
        screen.blit(interval_text, (WIDTH // 2 - interval_text.get_width() // 2, 10))

        # Display level
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (WIDTH - 150, HEIGHT - 40))
    elif winner:
        # Display winner screen
        winner_text = font.render("WINNER!", True, WHITE)
        screen.blit(winner_text, (WIDTH // 2 - 50, HEIGHT // 2 - 20))
        draw_button("Next Level", WIDTH // 2 - 80, HEIGHT // 2 + 20, 160, 40, action=lambda: reset_game(next_level=True))
    else:
        # Display death screen
        death_text = font.render("You Died!", True, WHITE)
        screen.blit(death_text, (WIDTH // 2 - 50, HEIGHT // 2 - 20))
        reset_text = font.render("Click to Restart",)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()