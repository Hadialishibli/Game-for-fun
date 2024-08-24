import pygame
enemy_speed = 1
class Enemy:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 10, 10)  # The enemy is the same size as the player (10x10)
        self.speed = enemy_speed

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

    def check_collision_with_wall(self, wall_rect):
        return self.rect.colliderect(wall_rect)

    def check_collision_with_enemy(self, other_enemy):
        return self.rect.colliderect(other_enemy.rect)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)  # Draw enemy as a red square

class EnemyManager:
    def __init__(self):
        self.enemies = []

    def add_enemy(self, x, y, speed):
        enemy = Enemy(x, y, speed)
        self.enemies.append(enemy)

    def handle_collisions(self, walls):
        for enemy in self.enemies:
            for wall in walls:
                if enemy.check_collision_with_wall(wall.rect):
                    self.handle_wall_collision(enemy, wall)
            for other_enemy in self.enemies:
                if other_enemy != enemy and enemy.check_collision_with_enemy(other_enemy):
                    self.handle_enemy_collision(enemy, other_enemy)

    def handle_wall_collision(self, enemy, wall):
        # Resolve wall collision by adjusting enemy's position
        if enemy.rect.right > wall.rect.left and enemy.rect.left < wall.rect.left:
            enemy.rect.right = wall.rect.left
        if enemy.rect.left < wall.rect.right and enemy.rect.right > wall.rect.right:
            enemy.rect.left = wall.rect.right
        if enemy.rect.bottom > wall.rect.top and enemy.rect.top < wall.rect.top:
            enemy.rect.bottom = wall.rect.top
        if enemy.rect.top < wall.rect.bottom and enemy.rect.bottom > wall.rect.bottom:
            enemy.rect.top = wall.rect.bottom

    def handle_enemy_collision(self, enemy, other_enemy):
        # Resolve enemy collision by separating them
        if enemy.rect.right > other_enemy.rect.left and enemy.rect.left < other_enemy.rect.left:
            enemy.rect.right = other_enemy.rect.left
        if enemy.rect.left < other_enemy.rect.right and enemy.rect.right > other_enemy.rect.right:
            enemy.rect.left = other_enemy.rect.right
        if enemy.rect.bottom > other_enemy.rect.top and enemy.rect.top < other_enemy.rect.top:
            enemy.rect.bottom = other_enemy.rect.top
        if enemy.rect.top < other_enemy.rect.bottom and enemy.rect.bottom > other_enemy.rect.bottom:
            enemy.rect.top = other_enemy.rect.bottom

    def update_enemies(self, player_rect, health_manager, walls):
        for enemy in self.enemies:
            enemy.move_towards_player(player_rect)
            if enemy.check_collision_with_player(player_rect):
                health_manager.decrease_health(0.5)  # Decrease health by 10 on collision

        # Handle collisions after movement
        self.handle_collisions(walls)

    def draw_enemies(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)
