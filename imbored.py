import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600  # Window size
FPS = 60  # Frames per second

# Colors
PORPOL = (160, 32, 240)
WALL_COLOR = (100, 100, 100)  # Color of the wall

# Player settings
player_size = 10
player_pos = [WIDTH // 2, HEIGHT // 2]  # Start in the center
speed = 2.5

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D RPG")

# Load and scale the background image
background_image = pygame.image.load('backgrounds\images.png').convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Wall class definition
class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, WALL_COLOR, self.rect)

# Create a wall object (you can add more walls as needed)
wall = Wall(200, 200, 200, 20)  # Wall placed at (300, 200) with width 200 and height 20
wall2 = Wall(50, 150, 20, 40)
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

    # Collision detection with the wall
    if player_rect.colliderect(wall.rect) or player_rect.colliderect(wall2.rect):
        # Undo the movement
        if keys[pygame.K_w]:
            player_pos[1] += speed
        if keys[pygame.K_s]:
            player_pos[1] -= speed
        if keys[pygame.K_a]:
            player_pos[0] += speed
        if keys[pygame.K_d]:
            player_pos[0] -= speed

    # Draw the scaled background image
    screen.blit(background_image, (0, 0))

    # Draw the wall
    wall.draw(screen)
    wall2.draw(screen)

    # Draw the player (a purple square)
    pygame.draw.rect(screen, PORPOL, player_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
