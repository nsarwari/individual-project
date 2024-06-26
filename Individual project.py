import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruitwinner")

BG = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 80  # Adjust to match the basket image size
PLAYER_HEIGHT = 80  # Adjust to match the basket image size
PLAYER_VEL = 5

# Load and resize the images
BASKET_IMG = pygame.image.load("basket.png")
BASKET_IMG = pygame.transform.scale(BASKET_IMG, (PLAYER_WIDTH, PLAYER_HEIGHT))

STRAWBERRY_IMG = pygame.image.load("strawberry.png")
STRAWBERRY_WIDTH = 50
STRAWBERRY_HEIGHT = 50
STRAWBERRY_IMG = pygame.transform.scale(STRAWBERRY_IMG, (STRAWBERRY_WIDTH, STRAWBERRY_HEIGHT))
STRAWBERRY_VEL = 1

APPLE_IMG = pygame.image.load("green_apple.png")
APPLE_WIDTH = 50
APPLE_HEIGHT = 50
APPLE_IMG = pygame.transform.scale(APPLE_IMG, (APPLE_WIDTH, APPLE_HEIGHT))

ORANGE_IMG = pygame.image.load("orange.png")
ORANGE_WIDTH = 50
ORANGE_HEIGHT = 50
ORANGE_IMG = pygame.transform.scale(ORANGE_IMG, (ORANGE_WIDTH, ORANGE_HEIGHT))

MONSTER_IMG = pygame.image.load("monster.png")
MONSTER_WIDTH = 50
MONSTER_HEIGHT = 50
MONSTER_IMG = pygame.transform.scale(MONSTER_IMG, (MONSTER_WIDTH, MONSTER_HEIGHT))
MONSTER_VEL = 1

GREEN_MONSTER_IMG = pygame.image.load("green_monster.png")
GREEN_MONSTER_WIDTH = 50
GREEN_MONSTER_HEIGHT = 50
GREEN_MONSTER_IMG = pygame.transform.scale(GREEN_MONSTER_IMG, (GREEN_MONSTER_WIDTH, GREEN_MONSTER_HEIGHT))

ORANGE_MONSTER_IMG = pygame.image.load("orange_monster.png")
ORANGE_MONSTER_WIDTH = 50
ORANGE_MONSTER_HEIGHT = 50
ORANGE_MONSTER_IMG = pygame.transform.scale(ORANGE_MONSTER_IMG, (ORANGE_MONSTER_WIDTH, ORANGE_MONSTER_HEIGHT))

CANDY_IMG = pygame.image.load("candy.png")
CANDY_WIDTH = 100
CANDY_HEIGHT = 100
CANDY_IMG = pygame.transform.scale(CANDY_IMG, (CANDY_WIDTH, CANDY_HEIGHT))

# Use a nicer font from Pygame's default fonts
FONT = pygame.font.SysFont("arial", 24)
BIG_FONT = pygame.font.SysFont("arial", 40)

def draw_text_with_box(text, font, color, box_color, x, y, padding=10):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    box_rect = pygame.Rect(x, y, text_rect.width + 2 * padding, text_rect.height + 2 * padding)
    text_rect.topleft = (x + padding, y + padding)
    pygame.draw.rect(WIN, box_color, box_rect)
    WIN.blit(text_surf, text_rect)

def draw_button(text, font, color, box_color, x, y, padding=10):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    box_rect = pygame.Rect(x, y, text_rect.width + 2 * padding, text_rect.height + 2 * padding)
    text_rect.topleft = (x + padding, y + padding)
    pygame.draw.rect(WIN, box_color, box_rect)
    WIN.blit(text_surf, text_rect)
    return box_rect

def draw(player, elapsed_time, fruits, monsters, score, missed, level, monster_touches, candy_count):
    WIN.blit(BG, (0, 0))

    draw_text_with_box(f"Time: {round(elapsed_time)}s", FONT, "white", (173, 216, 230), 10, 10)
    draw_text_with_box(f"Score: {score}", FONT, "white", (173, 216, 230), WIDTH - 200, 10)
    draw_text_with_box(f"Missed: {missed}", FONT, "white", (173, 216, 230), WIDTH - 200, 50)
    draw_text_with_box(f"Level: {level}", FONT, "white", (173, 216, 230), WIDTH - 200, 90)
    draw_text_with_box(f"Monster Touches: {monster_touches}/2", FONT, "white", (173, 216, 230), WIDTH - 240, 130)
    draw_text_with_box(f"Candies: {candy_count}", FONT, "white", (173, 216, 230), WIDTH - 240, 170)

    WIN.blit(BASKET_IMG, (player.x, player.y))

    for fruit in fruits:
        if level == 1:
            WIN.blit(STRAWBERRY_IMG, (fruit.x, fruit.y))
        elif level == 2:
            WIN.blit(APPLE_IMG, (fruit.x, fruit.y))
        else:
            WIN.blit(ORANGE_IMG, (fruit.x, fruit.y))

    for monster in monsters:
        if level == 1:
            WIN.blit(MONSTER_IMG, (monster.x, monster.y))
        elif level == 2:
            WIN.blit(GREEN_MONSTER_IMG, (monster.x, monster.y))
        else:
            WIN.blit(ORANGE_MONSTER_IMG, (monster.x, monster.y))

    pygame.display.update()

def draw_game_over(score):
    WIN.blit(BG, (0, 0))

    draw_text_with_box("Game Over!", BIG_FONT, "white", (173, 216, 230), WIDTH / 2 - 150, HEIGHT / 4)
    draw_text_with_box(f"Your Score: {score}", FONT, "white", (173, 216, 230), WIDTH / 2 - 150, HEIGHT / 2)
    draw_text_with_box("Press R to Restart", FONT, "white", (173, 216, 230), WIDTH / 2 - 150, HEIGHT - 100)

    pygame.display.update()

def draw_candy(candy_count):
    WIN.blit(BG, (0, 0))
    WIN.blit(CANDY_IMG, (WIDTH / 2 - CANDY_WIDTH / 2, HEIGHT / 2 - CANDY_HEIGHT / 2))
    draw_text_with_box(f"Candy Count: {candy_count}", BIG_FONT, "white", (173, 216, 230), WIDTH / 2 - 150, HEIGHT / 2 - 150)
    play_again_button = draw_button("Play Again & Win Again", FONT, "white", (0, 128, 0), WIDTH / 2 - 150, HEIGHT - 100)
    draw_text_with_box("Get 12 candies and a real winner gift candy set will be sent to you, so go get your fruits!", FONT, "white", (173, 216, 230), WIDTH / 2 - 300, HEIGHT / 2 + 100)
    pygame.display.update()
    return play_again_button

def draw_level_up(level):
    WIN.blit(BG, (0, 0))
    draw_text_with_box(f"Congrats, next level {level}!", BIG_FONT, "white", (173, 216, 230), WIDTH / 2 - 200, HEIGHT / 2 - 50)
    pygame.display.update()
    pygame.time.delay(2000)  # Show the level up message for 2 seconds

def draw_warning():
    WIN.blit(BG, (0, 0))
    draw_text_with_box("Don't touch the monsters, you will not survive!", BIG_FONT, "white", (173, 216, 230), WIDTH / 2 - 300, HEIGHT / 2 - 50)
    pygame.display.update()
    pygame.time.delay(2000)  # Show the warning message for 2 seconds

def main(fruit_vel_multiplier=1, candy_count=0):
    global STRAWBERRY_VEL, MONSTER_VEL
    run = True
    game_over = False
    level = 1
    show_warning = False

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    monster_add_increment = 5000  # Add a delay for monsters to spawn less frequently
    monster_count = 0

    fruits = []
    monsters = []
    score = 0
    missed = 0
    monster_touches = 0
    fruit_vel_increment = 0.05 * fruit_vel_multiplier  # Speed increase per fruit collected
    fruit_spawn_delay = 2300  # Delay in milliseconds between fruits
    last_fruit_time = pygame.time.get_ticks()  # Track the time when the last fruit was added

    while run:
        clock.tick(60)  # Ensure the game runs at 60 FPS
        elapsed_time = time.time() - start_time

        current_time = pygame.time.get_ticks()
        if not game_over:
            if current_time - last_fruit_time > fruit_spawn_delay:
                fruit_x = random.randint(0, WIDTH - STRAWBERRY_WIDTH)
                if level == 1:
                    fruit = pygame.Rect(fruit_x, -STRAWBERRY_HEIGHT, STRAWBERRY_WIDTH, STRAWBERRY_HEIGHT)
                elif level == 2:
                    fruit = pygame.Rect(fruit_x, -APPLE_HEIGHT, APPLE_WIDTH, APPLE_HEIGHT)
                else:
                    fruit = pygame.Rect(fruit_x, -ORANGE_HEIGHT, ORANGE_WIDTH, ORANGE_HEIGHT)
                fruits.append(fruit)
                last_fruit_time = current_time

            if ((level == 1 and score >= 10) or (level == 2) or (level == 3 and score < 75)) and current_time - monster_count > monster_add_increment:
                monster_x = random.randint(0, WIDTH - MONSTER_WIDTH)
                if level == 1:
                    monster = pygame.Rect(monster_x, -MONSTER_HEIGHT, MONSTER_WIDTH, MONSTER_HEIGHT)
                elif level == 2:
                    monster = pygame.Rect(monster_x, -GREEN_MONSTER_HEIGHT, GREEN_MONSTER_WIDTH, GREEN_MONSTER_HEIGHT)
                else:
                    monster = pygame.Rect(monster_x, -ORANGE_MONSTER_HEIGHT, ORANGE_MONSTER_WIDTH, ORANGE_MONSTER_HEIGHT)
                monsters.append(monster)
                monster_count = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
            if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
                player.x += PLAYER_VEL

            for fruit in fruits[:]:
                fruit.y += STRAWBERRY_VEL
                if fruit.y > HEIGHT:
                    fruits.remove(fruit)
                    missed += 1
                    if missed >= 3:
                        game_over = True
                elif fruit.colliderect(player):
                    fruits.remove(fruit)
                    score += 1
                    STRAWBERRY_VEL += fruit_vel_increment  # Increase speed
                    if score == 10 and not show_warning:
                        draw_warning()
                        show_warning = True
                    if score == 20:
                        level = 2  # Transition to level 2
                        draw_level_up(level)
                    elif score == 34:
                        level = 3  # Transition to level 3
                        draw_level_up(level)
                    elif score == 40:
                        candy_count += 1
                        play_again_button = draw_candy(candy_count)
                        game_over = True

            for monster in monsters[:]:
                monster.y += MONSTER_VEL
                if monster.y > HEIGHT:
                    monsters.remove(monster)
                elif monster.colliderect(player):
                    monsters.remove(monster)
                    monster_touches += 1
                    if monster_touches >= 2:
                        game_over = True

            # Check for collisions between fruits and monsters
            for fruit in fruits[:]:
                for monster in monsters[:]:
                    if fruit.colliderect(monster):
                        fruits.remove(fruit)
                        monsters.remove(monster)
                        break

            draw(player, elapsed_time, fruits, monsters, score, missed, level, monster_touches, candy_count)

        else:
            while game_over and candy_count > 0:
                play_again_button = draw_candy(candy_count)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        game_over = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if play_again_button.collidepoint(event.pos):
                            main(fruit_vel_multiplier + 0.1, candy_count)  # Increase the speed of the fruits
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_r]:
                        main()

    pygame.quit()

if __name__ == "__main__":
    main()
















