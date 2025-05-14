import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 520, 360
FPS = 60

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (33, 33, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

# Load maze layout (1 = wall, 0 = path)
maze = [
    "1111111111111",
    "1000000000001",
    "1011110111101",
    "1010000010101",
    "1010111010101",
    "1000000010101",
    "1010011110101",
    "1000000000001",
    "1111111111111"
]

TILE_SIZE = 40

# Pac-Man class
class PacMan:
    def __init__(self):
        self.x, self.y = 1, 1  # grid position

    def move(self, dx, dy):
        if self.can_move(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def can_move(self, x, y):
        return maze[y][x] == '0'

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2 - 5)

# Dot class
class Dot:
    def __init__(self):
        self.positions = [(x, y) for y in range(len(maze)) for x in range(len(maze[0])) if maze[y][x] == '0']

    def draw(self):
        for x, y in self.positions:
            pygame.draw.circle(screen, WHITE, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 5)

# Ghost class
class Ghost:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.move_counter = 0
        self.move_delay = 20

    def can_move(self, x, y):
        return maze[y][x] == '0'

    def update(self, pacman_pos):
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return
        self.move_counter = 0

        path = self.find_path(pacman_pos)
        if path and len(path) > 1:
            # Move to the next step in the path
            self.x, self.y = path[1]

    def find_path(self, target):
        from collections import deque

        queue = deque()
        queue.append((self.x, self.y))
        visited = { (self.x, self.y): None }

        while queue:
            current = queue.popleft()
            if current == target:
                break

            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = current[0] + dx, current[1] + dy
                if (0 <= nx < len(maze[0]) and 0 <= ny < len(maze)) and maze[ny][nx] == '0':
                    if (nx, ny) not in visited:
                        visited[(nx, ny)] = current
                        queue.append((nx, ny))

        # Reconstruct path
        path = []
        node = target
        while node is not None and node in visited:
            path.insert(0, node)
            node = visited[node]

        return path if path and path[0] == (self.x, self.y) else None

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2 - 5)

# Game setup
pacman = PacMan()
dots = Dot()
ghost = Ghost(5, 5)  # Starting position of ghost

# Game loop
while True:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                pacman.move(1, 0)
            elif event.key == pygame.K_UP:
                pacman.move(0, -1)
            elif event.key == pygame.K_DOWN:
                pacman.move(0, 1)

    # Update ghost
    ghost.update((pacman.x, pacman.y))

    # Collision detection with ghost
    if (pacman.x, pacman.y) == (ghost.x, ghost.y):
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Draw maze
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == '1':
                pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw and update game objects
    pacman.draw()
    ghost.draw()
    dots.draw()

    # Remove eaten dots
    dots.positions = [pos for pos in dots.positions if pos != (pacman.x, pacman.y)]

    if not dots.positions:
        print("You Win!")
        pygame.time.delay(2000)  # Pause to show the win message
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(FPS)