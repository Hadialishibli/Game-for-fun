import pygame

# Define the fixed size for the coins
COIN_SIZE = 20

class CoinManager:
    def __init__(self):
        self.coins = []
    
    def add_coin(self, x, y):
        self.coins.append(pygame.Rect(x, y, COIN_SIZE, COIN_SIZE))
    
    def draw_coins(self, screen):
        for coin in self.coins:
            pygame.draw.rect(screen, (255, 215, 0), coin)  # Draw coins as yellow squares
    
    def handle_coin_collection(self, player_rect):
        collected_coins = []
        for coin in self.coins:
            if player_rect.colliderect(coin):
                collected_coins.append(coin)
        for coin in collected_coins:
            self.coins.remove(coin)
        return len(collected_coins)  # Return the number of coins collected
