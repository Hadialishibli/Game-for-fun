import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600  # Window size
FPS = 60  # Frames per second

# Colors
YELLOW = (255, 255, 0)

# Player settings
player_size = 10
player_pos = [WIDTH // 2, HEIGHT // 2]  # Start in the center
speed = 2.5
# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D RPG")

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

    # Fill screen with black
    screen.fill((0, 0, 0))

    # Draw the player (a yellow square)
    pygame.draw.rect(screen, YELLOW, (player_pos[0], player_pos[1], player_size, player_size))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
