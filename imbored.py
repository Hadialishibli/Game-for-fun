import pygame
import sys
from wall_manager import WallManager  # Import the WallManager class

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600  # Window size
FPS = 60  # Frames per second

# Colors
PORPOL = (160, 32, 240)

# Player settings
player_size = 10
player_pos = [WIDTH // 2, HEIGHT // 2]  # Start in the center
speed = 2.5

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D RPG")

# Load and scale the background image
background_image = pygame.image.load('backgrounds/images.png').convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Create an instance of WallManager
wall_manager = WallManager()

# Add walls to the manager
# Add these lines to the WallManager in your main game file

# Example maze
wall_manager.add_wall(50, 50, 10, 500)    # Vertical wall
wall_manager.add_wall(50, 50, 300, 10)    # Horizontal wall
wall_manager.add_wall(150, 150, 10, 300)  # Vertical wall
wall_manager.add_wall(150, 150, 300, 10)  # Horizontal wall
wall_manager.add_wall(300, 300, 10, 150)  # Vertical wall
wall_manager.add_wall(300, 300, 150, 10)  # Horizontal wall
wall_manager.add_wall(450, 150, 10, 300)  # Vertical wall
wall_manager.add_wall(450, 150, 200, 10)  # Horizontal wall
wall_manager.add_wall(600, 50, 10, 500)   # Vertical wall
wall_manager.add_wall(600, 250, 100, 10)  # Horizontal wall


# Clock to control frame rate
clock = pygame.time.Clock()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos[1] -= speed  # Move up
    if keys[pygame.K_s]:
        player_pos[1] += speed  # Move down
    if keys[pygame.K_a]:
        player_pos[0] -= speed  # Move left
    if keys[pygame.K_d]:
        player_pos[0] += speed  # Move right

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

    # Update player position after collision handling
    player_pos[0], player_pos[1] = player_rect.x, player_rect.y

    # Draw the scaled background image
    screen.blit(background_image, (0, 0))

    # Draw the walls
    wall_manager.draw_walls(screen)

    # Draw the player (a purple square)
    pygame.draw.rect(screen, PORPOL, player_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
