import pygame
import sys
from wall_manager import WallManager
from coin_manager import CoinManager
from health_manager import HealthManager

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
player_pos = [WIDTH // 2, HEIGHT // 2]
speed = 2.5

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D RPG")

# Load and scale the background image
background_image = pygame.image.load('background/images.png').convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Create instances of WallManager, CoinManager, and HealthManager
wall_manager = WallManager()
coin_manager = CoinManager()
health_manager = HealthManager()

# Add walls to the WallManager
wall_manager.add_wall(50, 50, 10, 500)
wall_manager.add_wall(50, 50, 300, 10)
wall_manager.add_wall(150, 150, 10, 300)
wall_manager.add_wall(150, 150, 300, 10)
wall_manager.add_wall(300, 300, 10, 150)
wall_manager.add_wall(300, 300, 150, 10)
wall_manager.add_wall(450, 150, 10, 300)
wall_manager.add_wall(450, 150, 200, 10)
wall_manager.add_wall(600, 50, 10, 500)
wall_manager.add_wall(600, 250, 100, 10)

# Add coins to the CoinManager
coin_manager.add_coin(100, 100)
coin_manager.add_coin(200, 200)
coin_manager.add_coin(300, 300)
coin_manager.add_coin(400, 400)
coin_manager.add_coin(500, 500)

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

    # Update player position after collision handling
    player_pos[0], player_pos[1] = player_rect.x, player_rect.y

    # Simulate a condition where health decreases (e.g., touching a certain wall or enemy)
    # For now, decrease health by 1 if the player moves
    if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
        health_manager.decrease_health(0.05)

    # Draw the scaled background image
    screen.blit(background_image, (0, 0))

    # Draw the walls
    wall_manager.draw_walls(screen)

    # Draw the coins
    coin_manager.draw_coins(screen)

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
