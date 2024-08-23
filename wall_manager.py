from wall import Wall

class WallManager:
    def __init__(self):
        self.walls = []

    def add_wall(self, x, y, width, height):
        wall = Wall(x, y, width, height)
        self.walls.append(wall)

    def draw_walls(self, screen):
        for wall in self.walls:
            wall.draw(screen)

    def handle_collisions(self, player_rect):
        for wall in self.walls:
            wall.handle_collision(player_rect)
