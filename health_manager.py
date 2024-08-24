class HealthManager:
    def __init__(self):
        self.health = 100  # Start with 100 health points

    def decrease_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0  # Ensure health doesn't go below 0

    def increase_health(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100  # Ensure health doesn't go above 100

    def draw_health(self, screen, font, width, height):
        health_text = font.render(f"Health: {self.health}", True, (255, 0, 0))
        screen.blit(health_text, (10, height - health_text.get_height() - 10))  # Bottom left corner