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
# Updated PacMan class with smooth movement
class PacMan:
    def __init__(self):
        self.grid_x, self.grid_y = 1, 1  # Tile/grid coordinates
        self.x = self.grid_x * TILE_SIZE
        self.y = self.grid_y * TILE_SIZE
        self.speed = 2  # Pixels per frame
        self.direction = (0, 0)
        self.next_direction = (0, 0)

    def can_move(self, x, y):
        return (
            0 <= x < len(maze[0]) and
            0 <= y < len(maze) and
            maze[y][x] == '0'
        )

    def update(self):
        # Snap Pac-Man to grid when aligned
        if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
            self.grid_x = int(self.x // TILE_SIZE)
            self.grid_y = int(self.y // TILE_SIZE)

            # Try to apply the next direction (if allowed)
            next_x = self.grid_x + self.next_direction[0]
            next_y = self.grid_y + self.next_direction[1]
            if self.can_move(next_x, next_y):
                self.direction = self.next_direction

            # Check if current direction is blocked
            target_x = self.grid_x + self.direction[0]
            target_y = self.grid_y + self.direction[1]
            if not self.can_move(target_x, target_y):
                self.direction = (0, 0)

        # Move Pac-Man pixel-wise
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # Clamp position to the screen boundaries
        self.x = max(0, min(self.x, (len(maze[0]) - 1) * TILE_SIZE))
        self.y = max(0, min(self.y, (len(maze) - 1) * TILE_SIZE))

    def draw(self):
        draw_x = max(0, min(WIDTH - TILE_SIZE, int(self.x)))
        draw_y = max(0, min(HEIGHT - TILE_SIZE, int(self.y)))
        # pygame.draw.circle(screen, YELLOW, (int(self.x + TILE_SIZE // 2), int(self.y + TILE_SIZE // 2)), TILE_SIZE // 2 - 5)
        pygame.draw.circle(screen, YELLOW, (draw_x + TILE_SIZE // 2, draw_y + TILE_SIZE // 2), TILE_SIZE // 2 - 5)

    def handle_input(self, key):
        if key == pygame.K_LEFT:
            self.next_direction = (-1, 0)
        elif key == pygame.K_RIGHT:
            self.next_direction = (1, 0)
        elif key == pygame.K_UP:
            self.next_direction = (0, -1)
        elif key == pygame.K_DOWN:
            self.next_direction = (0, 1)

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
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
    #         sys.exit()
    #     elif event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_LEFT:
    #             pacman.move(-1, 0)
    #         elif event.key == pygame.K_RIGHT:
    #             pacman.move(1, 0)
    #         elif event.key == pygame.K_UP:
    #             pacman.move(0, -1)
    #         elif event.key == pygame.K_DOWN:
    #             pacman.move(0, 1)

    # Inside the main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pacman.handle_input(event.key)

    # Update Pac-Man and ghost
    pacman.update()
    # ghost.update()

    # Update ghost
    ghost.update((pacman.grid_x, pacman.grid_y))

    # Collision detection with ghost
    if (pacman.grid_x, pacman.grid_y) == (ghost.x, ghost.y):
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
    dots.positions = [pos for pos in dots.positions if pos != (pacman.grid_x, pacman.grid_y)]

    if not dots.positions:
        print("You Win!")
        pygame.time.delay(2000)  # Pause to show the win message
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(FPS)