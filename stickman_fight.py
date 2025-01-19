import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Fight")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Stickman dimensions
STICKMAN_WIDTH = 10
STICKMAN_HEIGHT = 50

# Initialize fonts
font = pygame.font.SysFont("Arial", 24)

# Player class
class Stickman:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = STICKMAN_WIDTH
        self.height = STICKMAN_HEIGHT
        self.color = color
        self.health = 100
        self.vel = 5
        self.attack = False
        self.direction = 1  # 1 = right, -1 = left

    def draw(self):
        # Draw body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Draw head
        pygame.draw.circle(screen, self.color, (self.x + self.width // 2, self.y - 10), 10)
        # Draw attack (hand or leg)
        if self.attack:
            pygame.draw.line(screen, RED, (self.x + self.width // 2, self.y + 10),
                             (self.x + self.width // 2 + self.direction * 20, self.y + 10), 5)

    def move(self, keys, up, left, down, right):
        if keys[left]:
            self.x -= self.vel
            self.direction = -1
        if keys[right]:
            self.x += self.vel
            self.direction = 1
        if keys[up]:
            self.y -= self.vel
        if keys[down]:
            self.y += self.vel

        # Boundaries
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(50, min(HEIGHT - self.height, self.y))

    def attack_move(self):
        self.attack = True

    def reset_attack(self):
        self.attack = False

# CPU-controlled stickman
class CPUStickman(Stickman):
    def auto_move(self, player):
        if player.x > self.x:
            self.x += self.vel // 2
            self.direction = 1
        elif player.x < self.x:
            self.x -= self.vel // 2
            self.direction = -1

        if player.y > self.y:
            self.y += self.vel // 2
        elif player.y < self.y:
            self.y -= self.vel // 2

        # Boundaries
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(50, min(HEIGHT - self.height, self.y))

# Initialize player and CPU
player = Stickman(100, HEIGHT - 100, BLUE)
cpu = CPUStickman(WIDTH - 200, HEIGHT - 100, BLACK)

# Main game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Draw health bars
    pygame.draw.rect(screen, RED, (50, 20, player.health * 2, 20))
    pygame.draw.rect(screen, RED, (WIDTH - 250, 20, cpu.health * 2, 20))

    # Event handling
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    player.move(keys, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d)

    # Player attacks
    if keys[pygame.K_j]:
        player.attack_move()
    else:
        player.reset_attack()

    # CPU movement
    cpu.auto_move(player)

    # CPU attacks randomly
    if random.randint(0, 50) == 1:
        cpu.attack_move()
    else:
        cpu.reset_attack()

    # Collision detection for attacks
    if player.attack and abs(player.x - cpu.x) < 30 and abs(player.y - cpu.y) < 50:
        cpu.health -= 1

    if cpu.attack and abs(cpu.x - player.x) < 30 and abs(cpu.y - player.y) < 50:
        player.health -= 1

    # Draw stickmen
    player.draw()
    cpu.draw()

    # Check for game over
    if player.health <= 0 or cpu.health <= 0:
        winner = "Player" if player.health > 0 else "CPU"
        text = font.render(f"{winner} Wins!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        pygame.time.wait(3000)
        running = False

    # Update display
    pygame.display.update()

pygame.quit()

