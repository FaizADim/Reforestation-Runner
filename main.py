import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen Settings
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reforestation Runner")
clock = pygame.time.Clock()
FPS = 60

# Colors
SKY_BLUE = (135, 206, 235)
GROUND_BROWN = (101, 67, 33)
GRASS_GREEN = (34, 139, 34)
PLAYER_GREEN = (46, 204, 113)
TRUNK_BROWN = (139, 69, 19)
FIRE_ORANGE = (230, 126, 34)
LOG_DARK = (92, 51, 23)
WATER_BLUE = (52, 152, 219)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont("Arial", 24, bold=True)
big_font = pygame.font.SysFont("Arial", 48, bold=True)

# Ground Level
GROUND_Y = 320

def reset_game():
    return {
        "player_rect": pygame.Rect(100, GROUND_Y - 50, 35, 50),
        "vel_y": 0,
        "is_jumping": False,
        "obstacles": [],
        "collectibles": [],
        "trees_planted": 0,
        "distance": 0,
        "speed": 6,
        "spawn_timer": 0,
        "game_over": False
    }

state = reset_game()
GRAVITY = 0.8
JUMP_STRENGTH = -15

# Main Game Loop
while True:
    screen.fill(SKY_BLUE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not state["game_over"] and not state["is_jumping"]:
                    state["vel_y"] = JUMP_STRENGTH
                    state["is_jumping"] = True
                elif state["game_over"]:
                    state = reset_game()

    if not state["game_over"]:
        # Player Physics
        state["vel_y"] += GRAVITY
        state["player_rect"].y += state["vel_y"]

        if state["player_rect"].bottom >= GROUND_Y:
            state["player_rect"].bottom = GROUND_Y
            state["is_jumping"] = False

        # Increase Distance & Speed Gradually
        state["distance"] += 0.1
        state["speed"] = 6 + int(state["distance"] // 50)

        # Spawn Obstacles & Water Drops
        state["spawn_timer"] += 1
        if state["spawn_timer"] > random.randint(55, 100):
            state["spawn_timer"] = 0
            choice = random.choice(["fire", "log", "water", "water"])
            if choice == "fire":
                # Wildfire hazard
                state["obstacles"].append(("fire", pygame.Rect(WIDTH, GROUND_Y - 35, 30, 35)))
            elif choice == "log":
                # Fallen timber / logging hazard
                state["obstacles"].append(("log", pygame.Rect(WIDTH, GROUND_Y - 25, 45, 25)))
            else:
                # Water drop collectible (plants a tree)
                y_pos = random.choice([GROUND_Y - 30, GROUND_Y - 90])
                state["collectibles"].append(pygame.Rect(WIDTH, y_pos, 20, 20))

        # Move & Check Obstacles
        for obs_type, rect in state["obstacles"][:]:
            rect.x -= state["speed"]
            if rect.right < 0:
                state["obstacles"].remove((obs_type, rect))
            if state["player_rect"].colliderect(rect):
                state["game_over"] = True

        # Move & Check Collectibles
        for drop in state["collectibles"][:]:
            drop.x -= state["speed"]
            if drop.right < 0:
                state["collectibles"].remove(drop)
            elif state["player_rect"].colliderect(drop):
                state["collectibles"].remove(drop)
                state["trees_planted"] += 1

    # Draw Background Trees (Visual progress based on trees planted!)
    for i in range(min(state["trees_planted"], 15)):
        tree_x = 40 + (i * 50)
        pygame.draw.rect(screen, TRUNK_BROWN, (tree_x + 10, GROUND_Y - 40, 10, 40))
        pygame.draw.circle(screen, GRASS_GREEN, (tree_x + 15, GROUND_Y - 50), 20)

    # Draw Ground
    pygame.draw.rect(screen, GRASS_GREEN, (0, GROUND_Y, WIDTH, 15))
    pygame.draw.rect(screen, GROUND_BROWN, (0, GROUND_Y + 15, WIDTH, HEIGHT - GROUND_Y))

    # Draw Player (Eco-Ranger)
    pygame.draw.rect(screen, PLAYER_GREEN, state["player_rect"], border_radius=5)

    # Draw Obstacles
    for obs_type, rect in state["obstacles"]:
        if obs_type == "fire":
            pygame.draw.polygon(screen, FIRE_ORANGE, [
                (rect.left, rect.bottom),
                (rect.centerx, rect.top),
                (rect.right, rect.bottom)
            ])
        else:
            pygame.draw.rect(screen, LOG_DARK, rect, border_radius=4)

    # Draw Water Drops
    for drop in state["collectibles"]:
        pygame.draw.circle(screen, WATER_BLUE, drop.center, 10)

    # Draw UI / Scoreboard
    trees_text = font.render(f"Trees Planted: {state['trees_planted']}", True, BLACK)
    dist_text = font.render(f"Distance: {int(state['distance'])}m", True, BLACK)
    screen.blit(trees_text, (20, 20))
    screen.blit(dist_text, (20, 50))

    # Game Over Screen
    if state["game_over"]:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        over_text = big_font.render("FOREST LOST!", True, WHITE)
        score_text = font.render(f"You restored {state['trees_planted']} trees over {int(state['distance'])}m", True, WHITE)
        restart_text = font.render("Press SPACE to Plant Again", True, PLAYER_GREEN)

        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, 120))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 185))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 235))

    pygame.display.flip()
    clock.tick(FPS)
