import pygame
import sys
from wall_manager import WallManager
from coin_manager import CoinManager
from health_manager import HealthManager
from enemy_manager import EnemyManager  # Import the EnemyManager

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
PORPOL = (160, 32, 240)
BACKGROUND_COLOR = (0, 0, 0)

# Player settings
player_size = 10
speed = 2.5

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D RPG")

# Load and scale the background image
background_image = pygame.image.load('background/images.png').convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Create instances of WallManager, CoinManager, HealthManager, and EnemyManager
wall_manager = WallManager()
coin_manager = CoinManager()
health_manager = HealthManager()
enemy_manager = EnemyManager()

# Walls
# Walls
wall_manager.add_wall(50, 50, 700, 10)    # Top wall
wall_manager.add_wall(50, 50, 10, 500)    # Left wall
wall_manager.add_wall(50, 540, 700, 10)   # Bottom wall
wall_manager.add_wall(740, 50, 10, 500)   # Right wall

# Inner walls creating a more complex maze
wall_manager.add_wall(200, 50, 10, 190)   # Vertical wall near top-left
wall_manager.add_wall(200, 300, 10, 230)  # Vertical wall near bottom-left
wall_manager.add_wall(400, 100, 10, 200)  # Vertical wall middle-top
wall_manager.add_wall(400, 400, 10, 140)  # Vertical wall middle-bottom
wall_manager.add_wall(600, 50, 10, 190)   # Vertical wall near top-right
wall_manager.add_wall(600, 300, 10, 240)  # Vertical wall near bottom-right
wall_manager.add_wall(50, 250, 300, 10)   # Horizontal wall middle-left
wall_manager.add_wall(440, 250, 300, 10)  # Horizontal wall middle-right
wall_manager.add_wall(50, 150, 140, 10)   # Horizontal wall near top-left
wall_manager.add_wall(250, 150, 150, 10)  # Horizontal wall middle-top
wall_manager.add_wall(450, 150, 150, 10)  # Horizontal wall middle-top right
wall_manager.add_wall(50, 450, 150, 10)   # Horizontal wall near bottom-left
wall_manager.add_wall(250, 450, 150, 10)  # Horizontal wall middle-bottom
wall_manager.add_wall(450, 450, 150, 10)  # Horizontal wall near bottom-right

# Coins
coin_manager.add_coin(100, 100)  # Top-left area
coin_manager.add_coin(300, 100)  # Top-middle-left area
coin_manager.add_coin(500, 100)  # Top-middle-right area
coin_manager.add_coin(700, 100)  # Top-right area
coin_manager.add_coin(100, 300)  # Middle-left area
coin_manager.add_coin(700, 300)  # Middle-right area
coin_manager.add_coin(100, 500)  # Bottom-left area
coin_manager.add_coin(300, 500)  # Bottom-middle-left area
coin_manager.add_coin(500, 500)  # Bottom-middle-right area
coin_manager.add_coin(700, 500)  # Bottom-right area

# Enemies
enemy_manager.add_enemy(350, 150, 1.0)  # Near the top-middle
enemy_manager.add_enemy(450, 350, 1.0)  # Near the bottom-middle
enemy_manager.add_enemy(150, 200, 1.0)  # Near the middle-left
enemy_manager.add_enemy(650, 200, 1.0)  # Near the middle-right
enemy_manager.add_enemy(350, 400, 1.0)  # Center of the maze

# Player
player_pos = [100, 100]  # Starting near the top-left corner


# Player
player_pos = [100, 500]  # Bottom-left corner


# Clock to control frame rate
clock = pygame.time.Clock()

# Score variable
score = 0

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos[1] -= speed
    if keys[pygame.K_s]:
        player_pos[1] += speed
    if keys[pygame.K_a]:
        player_pos[0] -= speed
    if keys[pygame.K_d]:
        player_pos[0] += speed

    # Boundary checking
    if player_pos[0] < 0:
        player_pos[0] = 0
    if player_pos[0] > WIDTH - player_size:
        player_pos[0] = WIDTH - player_size
    if player_pos[1] < 0:
        player_pos[1] = 0
    if player_pos[1] > HEIGHT - player_size:
        player_pos[1] = HEIGHT - player_size

    # Player's rectangle
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)

    # Handle collisions with walls
    wall_manager.handle_collisions(player_rect)

    # Handle coin collection
    collected_coins = coin_manager.handle_coin_collection(player_rect)
    score += collected_coins

    # Update enemies and handle collisions with the player and walls
    enemy_manager.update_enemies(player_rect, health_manager, wall_manager.walls)

    # Update player position after collision handling
    player_pos[0], player_pos[1] = player_rect.x, player_rect.y

    # Draw the scaled background image
    screen.blit(background_image, (0, 0))

    # Draw the walls
    wall_manager.draw_walls(screen)

    # Draw the coins
    coin_manager.draw_coins(screen)

    # Draw the enemies
    enemy_manager.draw_enemies(screen)

    # Draw the player
    pygame.draw.rect(screen, PORPOL, player_rect)

    # Draw the score in the top right corner
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 255, 255))
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    # Draw the health in the bottom left corner
    health_manager.draw_health(screen, font, WIDTH, HEIGHT)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
