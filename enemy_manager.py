import pygame
Enemy_speed=0.5
class Enemy:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 10, 10)  # The enemy is the same size as the player (10x10)
        self.speed = Enemy_speed

    def move_towards_player(self, player_rect):
        # Calculate the direction vector from the enemy to the player
        dx, dy = player_rect.x - self.rect.x, player_rect.y - self.rect.y
        dist = (dx**2 + dy**2) ** 0.5

        if dist != 0:  # Normalize the direction vector
            dx, dy = dx / dist, dy / dist

        # Move the enemy towards the player
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def check_collision_with_player(self, player_rect):
        return self.rect.colliderect(player_rect)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)  # Draw enemy as a red square

class EnemyManager:
    def __init__(self):
        self.enemies = []

    def add_enemy(self, x, y, speed):
        enemy = Enemy(x, y, speed)
        self.enemies.append(enemy)

    def update_enemies(self, player_rect, health_manager):
        for enemy in self.enemies:
            enemy.move_towards_player(player_rect)
            if enemy.check_collision_with_player(player_rect):
                health_manager.decrease_health(1)  # Decrease health by 10 on collision

    def draw_enemies(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
