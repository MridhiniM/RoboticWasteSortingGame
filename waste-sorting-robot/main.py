import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Waste Sorting Robot Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Object dimensions
WASTE_SIZE = 30
BIN_WIDTH = 100
BIN_HEIGHT = 60

# Waste categories and bins
categories = ['Plastic', 'Metal', 'Paper']
bins = {
    'Plastic': {'color': BLUE, 'x': 150, 'y': HEIGHT - BIN_HEIGHT},
    'Metal': {'color': GREEN, 'x': 350, 'y': HEIGHT - BIN_HEIGHT},
    'Paper': {'color': RED, 'x': 550, 'y': HEIGHT - BIN_HEIGHT}
}

# Waste class
class Waste:
    def __init__(self, category, x, y):
        self.category = category
        self.color = bins[category]['color']
        self.x = x
        self.y = y
        self.speed = random.randint(2, 5)
    
    def move(self):
        self.y += self.speed
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, WASTE_SIZE, WASTE_SIZE))

# Robot arm
robot_x, robot_y = WIDTH // 2, HEIGHT // 2
robot_speed = 10

# Game variables
waste_list = []
score = 0
font = pygame.font.Font(None, 36)
running = True

# Game loop
while running:
    screen.fill(WHITE)
    
    # Draw bins
    for category, bin_data in bins.items():
        pygame.draw.rect(screen, bin_data['color'], (bin_data['x'], bin_data['y'], BIN_WIDTH, BIN_HEIGHT))
        bin_label = font.render(category, True, BLACK)
        screen.blit(bin_label, (bin_data['x'] + 10, bin_data['y'] - 30))
    
    # Generate waste
    if random.randint(1, 50) == 1:
        category = random.choice(categories)
        x = random.randint(0, WIDTH - WASTE_SIZE)
        waste_list.append(Waste(category, x, 0))
    
    # Move and draw waste
    for waste in waste_list[:]:
        waste.move()
        waste.draw()
        if waste.y > HEIGHT:
            waste_list.remove(waste)
    
    # Draw robot arm
    pygame.draw.rect(screen, GRAY, (robot_x, robot_y, 60, 20))
    
    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle robot movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and robot_x > 0:
        robot_x -= robot_speed
    if keys[pygame.K_RIGHT] and robot_x < WIDTH - 60:
        robot_x += robot_speed
    if keys[pygame.K_UP] and robot_y > 0:
        robot_y -= robot_speed
    if keys[pygame.K_DOWN] and robot_y < HEIGHT - 20:
        robot_y += robot_speed
    
    # Check for sorting
    for waste in waste_list[:]:
        if (robot_x < waste.x < robot_x + 60 or robot_x < waste.x + WASTE_SIZE < robot_x + 60) and \
           (robot_y < waste.y < robot_y + 20 or robot_y < waste.y + WASTE_SIZE < robot_y + 20):
            if bins[waste.category]['x'] < robot_x < bins[waste.category]['x'] + BIN_WIDTH:
                score += 10
            else:
                score -= 5
            waste_list.remove(waste)
    
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
