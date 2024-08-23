import pygame

# Wall class definition
class Wall:
    def __init__(self, x, y, width, height, color=(100, 100, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def handle_collision(self, player_rect):
        if self.rect.colliderect(player_rect):
            if player_rect.right > self.rect.left and player_rect.left < self.rect.left:
                player_rect.right = self.rect.left
            elif player_rect.left < self.rect.right and player_rect.right > self.rect.right:
                player_rect.left = self.rect.right
            if player_rect.bottom > self.rect.top and player_rect.top < self.rect.top:
                player_rect.bottom = self.rect.top
            elif player_rect.top < self.rect.bottom and player_rect.bottom > self.rect.bottom:
                player_rect.top = self.rect.bottom
