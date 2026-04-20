import pygame
import sys
from blackjack import start_blackjack_game
from players import check_player, save_player, get_correct_player_name

pygame.init()
pygame.mixer.init()

# Variables, constants, globals
WIDTH, HEIGHT = 1536, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame Blackjack!')
FONT = pygame.font.Font("Assets/Fonts/DejaVuSans.ttf", 42)
SMALLER_FONT = pygame.font.Font("Assets/Fonts/DejaVuSans.ttf", 34)

# Colors (via Adobe Color Palette with background as template)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKBLUE = (22, 45, 115)
DARKGREEN = (25, 64, 35)
YELLOW = (242, 192, 99)
RED = (217, 7, 7)

# Background image
try:
    BACKGROUND = pygame.image.load("Assets/Images/blackjack.png")
except:
    BACKGROUND = None


# Check and add player via class Player
def player_exists(name):
    if check_player(name):
        return False
    return True


def add_player(name):
    save_player(name)


#  Background music
def start_background_music():
    pygame.mixer.music.load("Assets/Music/AceOfSpades.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(0)  # -1 = infinite loop,  0 = no loop


def stop_background_music():
    pygame.mixer.music.stop()


# Help functions
def draw_background():
    if BACKGROUND:
        screen.blit(BACKGROUND, (0, 0))
    else:
        screen.fill(BLACK)


def draw_button(text, rect, hover):
    color = DARKBLUE if hover else DARKGREEN
    pygame.draw.rect(screen, color, rect, border_radius=10)

    label = SMALLER_FONT.render(text, True, YELLOW)
    screen.blit(label, (
        rect.x + (rect.width - label.get_width()) // 2,
        rect.y + (rect.height - label.get_height()) // 2
    ))


# Input screen, for both new and existing player
def text_input_screen(title_text, validator):
    input_text = ""
    error_message = ""
    active = True

    while active:
        draw_background()

        # Title
        title = FONT.render(title_text, True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        # Input box
        pygame.draw.rect(screen, WHITE, (568, 500, 400, 50), border_radius=8)
        label = SMALLER_FONT.render(input_text, True, BLACK)
        screen.blit(label, (568, 500))  # 578,505

        # Confirm button
        confirm_rect = pygame.Rect(618, 570, 300, 60)
        hover = confirm_rect.collidepoint(pygame.mouse.get_pos())
        draw_button("Confirm", confirm_rect, hover)

        # Error message
        if error_message:
            err = SMALLER_FONT.render(error_message, True, RED)
            screen.blit(err, (WIDTH // 2 - err.get_width() // 2, 640))

        pygame.display.flip()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    if len(input_text) < 15:
                        input_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hover:
                    valid, msg = validator(input_text.strip())
                    if valid:
                        return msg if msg else input_text.strip()
                    else:
                        error_message = msg


# Validate players names for new and existing players
def validate_new_player(name):
    if not name:
        return False, "Name cannot be empty"
    if player_exists(name):
        return False, "Player already exists!"
    add_player(name)
    return True, None


def validate_existing_player(name):
    correct_name = get_correct_player_name(name)
    if correct_name is None:
        return False, "Player does not exist!"
    return True, correct_name


#  Start screen - main program
def start_screen():
    start_background_music()

    while True:
        draw_background()
        mouse = pygame.mouse.get_pos()

        btn_new = pygame.Rect(443, 512, 300, 70)
        btn_existing = pygame.Rect(793, 512, 300, 70)
        hover_new = btn_new.collidepoint(mouse)
        hover_existing = btn_existing.collidepoint(mouse)

        draw_button("New player", btn_new, hover_new)
        draw_button("Returning player", btn_existing, hover_existing)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Add new player:
                if hover_new:
                    name = text_input_screen(
                        "Add New Player", validate_new_player)
                    stop_background_music()
                    start_blackjack_game(name)

                # Choose existing player:
                if hover_existing:
                    name = text_input_screen(
                        "Enter your name", validate_existing_player)
                    stop_background_music()
                    start_blackjack_game(name)


start_screen()
