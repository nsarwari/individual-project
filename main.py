import pygame
import time
import random
import datetime
import pandas as pd

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruitwinner")

BG = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80
PLAYER_VEL = 5

OPEN_MOUTH_IMG = pygame.image.load("open-mouth.png")
OPEN_MOUTH_IMG = pygame.transform.scale(OPEN_MOUTH_IMG, (PLAYER_WIDTH, PLAYER_HEIGHT))

STRAWBERRY_IMG = pygame.image.load("strawberry.png")
STRAWBERRY_WIDTH = 50
STRAWBERRY_HEIGHT = 50
STRAWBERRY_IMG = pygame.transform.scale(STRAWBERRY_IMG, (STRAWBERRY_WIDTH, STRAWBERRY_HEIGHT))
STRAWBERRY_VEL = 2  # Increased speed

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
MONSTER_VEL = 2  # Increased speed

GREEN_MONSTER_IMG = pygame.image.load("green_monster.png")
GREEN_MONSTER_WIDTH = 50
GREEN_MONSTER_HEIGHT = 50
GREEN_MONSTER_IMG = pygame.transform.scale(GREEN_MONSTER_IMG, (GREEN_MONSTER_WIDTH, GREEN_MONSTER_HEIGHT))

ORANGE_MONSTER_IMG = pygame.image.load("orange_monster.png")
ORANGE_MONSTER_WIDTH = 50
ORANGE_MONSTER_HEIGHT = 50
ORANGE_MONSTER_IMG = pygame.transform.scale(ORANGE_MONSTER_IMG, (ORANGE_MONSTER_WIDTH, ORANGE_MONSTER_HEIGHT))

CANDY_IMG = pygame.image.load("candy.png")
CANDY_WIDTH = 60
CANDY_HEIGHT = 60
CANDY_IMG = pygame.transform.scale(CANDY_IMG, (CANDY_WIDTH, CANDY_HEIGHT))

RECTANGLE_IMG = pygame.image.load("rectangle.png")

FONT = pygame.font.SysFont("arial", 24)
BIG_FONT = pygame.font.SysFont("arial", 40, bold=True)

# Feedback storage
feedbacks = []
game_results = []

def draw_button(text, font, color, box_color, x, y, padding=10):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    box_rect = pygame.Rect(x, y, text_rect.width + 2 * padding, text_rect.height + 2 * padding)
    text_rect.topleft = (x + padding, y + padding)
    pygame.draw.rect(WIN, box_color, box_rect)
    WIN.blit(text_surf, text_rect)
    return box_rect

def draw_rectangle_with_text(text, font, color, x, y, padding=20):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    rectangle_width = text_rect.width + 2 * padding
    rectangle_height = text_rect.height + 2 * padding
    rectangle_img = pygame.transform.scale(RECTANGLE_IMG, (rectangle_width, rectangle_height))
    rectangle_rect = rectangle_img.get_rect()
    rectangle_rect.topleft = (x, y)
    WIN.blit(rectangle_img, rectangle_rect.topleft)
    text_rect.center = rectangle_rect.center
    WIN.blit(text_surf, text_rect)
    return rectangle_rect

def draw_square_with_text(text, font, color, square_img, x, y):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    square_rect = pygame.Rect(x, y, text_rect.width + 20, text_rect.height + 20)
    WIN.blit(pygame.transform.scale(square_img, (square_rect.width, square_rect.height)), square_rect.topleft)
    text_rect.center = square_rect.center
    WIN.blit(text_surf, text_rect)

def draw_square_with_candy(square_img, candy_img, x, y):
    square_rect = pygame.Rect(x, y, candy_img.get_width() + 40, candy_img.get_height() + 40)
    WIN.blit(pygame.transform.scale(square_img, (square_rect.width, square_rect.height)), square_rect.topleft)
    WIN.blit(candy_img, (x + 20, y + 20))

def draw_initial_instructions():
    WIN.blit(BG, (0, 0))
    draw_rectangle_with_text("Catch the fruits & get your candy!", BIG_FONT, "white", WIDTH / 2 - 300, HEIGHT / 2 - 150)
    draw_rectangle_with_text("Use the left and right arrows to move your mouth and eat your fruits", FONT, "white", WIDTH / 2 - 350, HEIGHT / 2 - 50)
    draw_rectangle_with_text("If you miss 3 fruits you lose", FONT, "white", WIDTH / 2 - 200, HEIGHT / 2 + 50)
    pygame.display.update()
    time.sleep(5)  # Show the instructions for 5 seconds

def draw(player, elapsed_time, fruits, monsters, score, missed, level, monster_touches, candy_count):
    WIN.blit(BG, (0, 0))

    WIN.blit(OPEN_MOUTH_IMG, (player.x, player.y))

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

    draw_square_with_text(f"Time: {round(elapsed_time)}s", FONT, "white", RECTANGLE_IMG, 10, 10)
    draw_square_with_text(f"Score: {score}", FONT, "white", RECTANGLE_IMG, 10, 60)
    draw_square_with_text(f"Missed: {missed}", FONT, "white", RECTANGLE_IMG, 10, 110)
    draw_square_with_text(f"Level: {level}", FONT, "white", RECTANGLE_IMG, 10, 160)
    draw_square_with_text(f"Monster Touches: {monster_touches}/2", FONT, "white", RECTANGLE_IMG, 10, 210)
    draw_square_with_candy(RECTANGLE_IMG, CANDY_IMG, 10, 260)
    draw_square_with_text(f"{candy_count}", FONT, "white", RECTANGLE_IMG, 80, 260)

    pygame.display.update()

def draw_game_over(score):
    WIN.blit(BG, (0, 0))

    draw_rectangle_with_text("Game Over!", BIG_FONT, "white", WIDTH / 2 - 150, HEIGHT / 4)
    draw_rectangle_with_text(f"Your Score: {score}", FONT, "white", WIDTH / 2 - 150, HEIGHT / 2)

    restart_button = draw_button("Restart", FONT, (255, 255, 255), (0, 128, 0), WIDTH / 2 - 150, HEIGHT - 100)
    feedback_button = draw_button("Submit Feedback", FONT, (0, 0, 0), (173, 216, 230), 10, HEIGHT - 60)
    feedback_input_rect = pygame.Rect(10, HEIGHT - 110, 300, 50)
    pygame.draw.rect(WIN, (255, 255, 255), feedback_input_rect)
    pygame.draw.rect(WIN, (0, 0, 0), feedback_input_rect, 2)
    pygame.display.update()
    return restart_button, feedback_button, feedback_input_rect

def draw_candy(candy_count):
    WIN.blit(BG, (0, 0))
    WIN.blit(CANDY_IMG, (WIDTH / 2 - CANDY_WIDTH / 2, HEIGHT / 2 - CANDY_HEIGHT / 2))
    draw_rectangle_with_text(f"Candy Count: {candy_count}", BIG_FONT, "white", WIDTH / 2 - 150, HEIGHT / 2 - 150)
    draw_rectangle_with_text("Get 12 candies and a real winner gift candy set will be sent to you, so go get your fruits!", FONT, "white", WIDTH / 2 - 300, HEIGHT / 2 + 50)
    draw_rectangle_with_text("Congratulations, you won a candy treat!", FONT, "white", WIDTH / 2 - 300, HEIGHT / 2 + 100)
    
    play_again_button = draw_button("Play Again & Win Again", FONT, "white", (0, 128, 0), WIDTH / 2 - 150, HEIGHT - 100)

    feedback_button = draw_button("Submit Feedback", FONT, (0, 0, 0), (173, 216, 230), 10, HEIGHT - 60)
    feedback_input_rect = pygame.Rect(10, HEIGHT - 110, 300, 50)
    pygame.draw.rect(WIN, (255, 255, 255), feedback_input_rect)
    pygame.draw.rect(WIN, (0, 0, 0), feedback_input_rect, 2)
    pygame.display.update()
    return play_again_button, feedback_button, feedback_input_rect

def draw_level_up(level):
    WIN.blit(BG, (0, 0))
    draw_rectangle_with_text(f"Congrats, next level {level}!", BIG_FONT, "white", WIDTH / 2 - 200, HEIGHT / 2 - 50)

    pygame.display.update()
    pygame.time.delay(2000)  # Show the level up message for 2 seconds

def draw_warning():
    WIN.blit(BG, (0, 0))
    draw_rectangle_with_text("Don't touch the monsters, you will not survive!", BIG_FONT, "white", WIDTH / 2 - 300, HEIGHT / 2 - 50)

    pygame.display.update()
    pygame.time.delay(2000)  # Show the warning message for 2 seconds

def handle_feedback(feedback_input_rect, start_time, difficulty, end_time, score, won):
    feedback_text = ""
    font = pygame.font.SysFont("arial", 18)
    submitting_feedback = True

    while submitting_feedback:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    feedbacks.append((feedback_text, datetime.datetime.now()))
                    game_results.append({
                        "Start Time": start_time,
                        "End Time": end_time,
                        "Duration": end_time - start_time,
                        "Score": score,
                        "Difficulty": difficulty,
                        "Feedback": feedback_text
                    })
                    df = pd.DataFrame(game_results)
                    df.to_excel("game_results.xlsx", index=False)
                    submitting_feedback = False
                elif event.key == pygame.K_BACKSPACE:
                    feedback_text = feedback_text[:-1]
                else:
                    feedback_text += event.unicode

        WIN.blit(BG, (0, 0))
        pygame.draw.rect(WIN, (255, 255, 255), feedback_input_rect)
        pygame.draw.rect(WIN, (0, 0, 0), feedback_input_rect, 2)
        text_surface = font.render(feedback_text, True, (0, 0, 0))
        WIN.blit(text_surface, (feedback_input_rect.x + 5, feedback_input_rect.y + 5))
        feedback_button = draw_button("Submit Feedback", font, (0, 0, 0), (173, 216, 230), 10, HEIGHT - 60)
        pygame.display.flip()

    if won:
        play_again_button, feedback_button, feedback_input_rect = draw_candy(score // 40)
    else:
        restart_button, feedback_button, feedback_input_rect = draw_game_over(score)
    return play_again_button if won else restart_button

def main(fruit_vel_increment=0.05, candy_count=0):
    global STRAWBERRY_VEL, MONSTER_VEL, score
    run = True
    game_over = False
    level = 1
    show_warning = False

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    monster_add_increment = 5000
    monster_count = 0

    fruits = []
    monsters = []
    score = 0
    missed = 0
    monster_touches = 0
    fruit_spawn_delay = 2300  # Decreased delay for faster fruit spawning
    last_fruit_time = pygame.time.get_ticks()
    last_fruit_x = WIDTH // 2

    # Draw difficulty selection
    WIN.blit(BG, (0, 0))
    beginner_button = draw_rectangle_with_text("Beginner", BIG_FONT, "white", WIDTH / 2 - 150, HEIGHT / 2 - 150)
    intermediate_button = draw_rectangle_with_text("Intermediate", BIG_FONT, "white", WIDTH / 2 - 150, HEIGHT / 2)
    pro_button = draw_rectangle_with_text("Pro", BIG_FONT, "white", WIDTH / 2 - 150, HEIGHT / 2 + 150)
    pygame.display.update()

    difficulty_selected = False
    difficulty = ""
    while not difficulty_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                difficulty_selected = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if beginner_button.collidepoint(event.pos):
                    fruit_vel_increment = 0.05
                    difficulty = "Beginner"
                    difficulty_selected = True
                elif intermediate_button.collidepoint(event.pos):
                    fruit_vel_increment = 0.1
                    difficulty = "Intermediate"
                    difficulty_selected = True
                elif pro_button.collidepoint(event.pos):
                    fruit_vel_increment = 0.15
                    difficulty = "Pro"
                    difficulty_selected = True

    draw_initial_instructions()

    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time

        current_time = pygame.time.get_ticks()
        if not game_over:
            if current_time - last_fruit_time > fruit_spawn_delay:
                fruit_x = random.randint(max(0, last_fruit_x - 300), min(WIDTH - STRAWBERRY_WIDTH, last_fruit_x + 300))
                if level == 1:
                    fruit = pygame.Rect(fruit_x, -STRAWBERRY_HEIGHT, STRAWBERRY_WIDTH, STRAWBERRY_HEIGHT)
                elif level == 2:
                    fruit = pygame.Rect(fruit_x, -APPLE_HEIGHT, APPLE_WIDTH, APPLE_HEIGHT)
                else:
                    fruit = pygame.Rect(fruit_x, -ORANGE_HEIGHT, ORANGE_WIDTH, ORANGE_HEIGHT)
                fruits.append(fruit)
                last_fruit_x = fruit_x
                last_fruit_time = current_time

            if ((level == 1 and score >= 10) or (level == 2 and score < 34) or (level == 3 and score >= 34)) and current_time - monster_count > monster_add_increment:
                monster_x = random.randint(0, WIDTH - MONSTER_WIDTH)
                monster = pygame.Rect(monster_x, -MONSTER_HEIGHT, MONSTER_WIDTH, MONSTER_HEIGHT)
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
                    STRAWBERRY_VEL += fruit_vel_increment
                    if score % 3 == 0:
                        fruit_spawn_delay = max(800, fruit_spawn_delay - 100)
                    if score == 10 and not show_warning:
                        draw_warning()
                        show_warning = True
                    if score == 20:
                        level = 2
                        draw_level_up(level)
                    elif score == 34:
                        level = 3
                        draw_level_up(level)
                    elif score == 40:
                        candy_count += 1
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

            for fruit in fruits[:]:
                for monster in monsters[:]:
                    if fruit.colliderect(monster):
                        fruits.remove(fruit)
                        monsters.remove(monster)
                        break

            draw(player, elapsed_time, fruits, monsters, score, missed, level, monster_touches, candy_count)

        else:
            end_time = time.time()
            if score == 40:
                play_again_button, feedback_button, feedback_input_rect = draw_candy(candy_count)
            else:
                restart_button, feedback_button, feedback_input_rect = draw_game_over(score)

            feedback_text = ""
            font = pygame.font.SysFont("arial", 18)
            submitting_feedback = True
            while submitting_feedback:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        submitting_feedback = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if score == 40 and play_again_button.collidepoint(event.pos):
                            main(fruit_vel_increment + 0.1, candy_count)
                        elif feedback_button.collidepoint(event.pos):
                            if handle_feedback(feedback_input_rect, start_time, difficulty, end_time, score, score == 40) == "won":
                                play_again_button, feedback_button, feedback_input_rect = draw_candy(candy_count)
                            else:
                                restart_button, feedback_button, feedback_input_rect = draw_game_over(score)
                            submitting_feedback = False
                        elif score != 40 and restart_button.collidepoint(event.pos):
                            main()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if handle_feedback(feedback_input_rect, start_time, difficulty, end_time, score, score == 40) == "won":
                                play_again_button, feedback_button, feedback_input_rect = draw_candy(candy_count)
                            else:
                                restart_button, feedback_button, feedback_input_rect = draw_game_over(score)
                            submitting_feedback = False
                        elif event.key == pygame.K_BACKSPACE:
                            feedback_text = feedback_text[:-1]
                        else:
                            feedback_text += event.unicode

                WIN.blit(BG, (0, 0))
                if score == 40:
                    WIN.blit(CANDY_IMG, (WIDTH / 2 - CANDY_WIDTH / 2, HEIGHT / 2 - CANDY_HEIGHT / 2))
                    draw_rectangle_with_text(f"Candy Count: {candy_count}", BIG_FONT, "white", WIDTH / 2 - 150, HEIGHT / 2 - 150)
                    draw_rectangle_with_text("Get 12 candies and a real winner gift candy set will be sent to you, so go get your fruits!", FONT, "white", WIDTH / 2 - 300, HEIGHT / 2 + 50)
                    draw_rectangle_with_text("Congratulations, you won a candy treat!", FONT, "white", WIDTH / 2 - 300, HEIGHT / 2 + 100)
                    play_again_button = draw_button("Play Again & Win Again", FONT, "white", (0, 128, 0), WIDTH / 2 - 150, HEIGHT - 100)
                else:
                    draw_rectangle_with_text("Game Over!", BIG_FONT, "white", WIDTH / 2 - 150, HEIGHT / 4)
                    draw_rectangle_with_text(f"Your Score: {score}", FONT, "white", WIDTH / 2 - 150, HEIGHT / 2)
                    restart_button = draw_button("Restart", FONT, (255, 255, 255), (0, 128, 0), WIDTH / 2 - 150, HEIGHT - 100)

                pygame.draw.rect(WIN, (255, 255, 255), feedback_input_rect)
                pygame.draw.rect(WIN, (0, 0, 0), feedback_input_rect, 2)
                text_surface = font.render(feedback_text, True, (0, 0, 0))
                WIN.blit(text_surface, (feedback_input_rect.x + 5, feedback_input_rect.y + 5))
                feedback_button = draw_button("Submit Feedback", font, (0, 0, 0), (173, 216, 230), 10, HEIGHT - 60)
                pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

