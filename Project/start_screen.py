import pygame
import sys
import csv
import os
from blackjack import start_blackjack_game

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1536, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame Blackjack!')
background = pygame.image.load("Assets/Images/blackjack.png")
font = pygame.font.Font("Assets/Fonts/DejaVuSans.ttf", 42)
smaller_font = pygame.font.Font("Assets/Fonts/DejaVuSans.ttf", 34)

# standaardkleuren, herbekijken zodra nieuwe kleuren toegevoegd zijn:
white = (255, 255, 255)
black = (0, 0, 0)
gray = (180, 180, 180)
green = (0, 200, 0)
blue = (0, 120, 255)

#  kleuren via adobe colorpalette op basis van achtergrond
darkblue = (22, 45, 115)
green = (45, 115, 62)
darkgreen = (25, 64, 35)
yellow = (242, 192, 99)
red = (217, 7, 7)


# Alles voor de CSV file:
CSV_FILE = "players.csv"


def player_exists(name):
    if not os.path.exists(CSV_FILE):
        return False

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].lower() == name.lower():
                return True
    return False


def add_player(name):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, 0, 0, 0])  # win, lose, draw


#  Achtergrondmuziek
def start_background_music():
    pygame.mixer.music.load("Assets/Music/AceOfSpades.mp3")
    pygame.mixer.music.set_volume(0.4)  # 0.0 - 1.0
    pygame.mixer.music.play(0)  # -1 = infinite loop,  0 = geen loop


def stop_background_music():
    pygame.mixer.music.stop()


# --- Achtergrond laden ---
try:
    background = pygame.image.load("Assets/Images/blackjack.png")
except:
    background = None


#  Scherm voor nieuwe speler toe te voegen
def new_player_screen():
    input_text = ""
    error_message = ""
    active = True

    while active:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass  # Enter doet niets, Confirm‑knop doet het werk
                else:
                    if len(input_text) < 15:
                        input_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Confirm‑knop
                if confirm_button.collidepoint(mx, my):
                    if input_text.strip() == "":
                        error_message = "Name cannot be empty"
                    elif player_exists(input_text):
                        error_message = "Player already exists!"
                    else:
                        add_player(input_text)
                        return input_text

        # --- TEKENEN ---
        title = font.render("Add New Player", True, yellow)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

        # Inputveld
        pygame.draw.rect(screen, white, (568, 500, 400, 50), border_radius=8)
        name_label = smaller_font.render(input_text, True, black)
        screen.blit(name_label, (568, 500))

        # Confirm‑knop
        confirm_button = pygame.Rect(618, 570, 300, 60)
        draw_button("Confirm", 618, 570, 300, 60,
                    confirm_button.collidepoint(pygame.mouse.get_pos()))

        # Foutmelding
        if error_message:
            err = smaller_font.render(error_message, True, red)
            screen.blit(err, (WIDTH//2 - err.get_width()//2, 630))

        pygame.display.flip()

# Scherm voor bestaande speler op te vragen:


def existing_player_screen():
    input_text = ""
    error_message = ""
    active = True

    while active:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass  # Enter doet niets, Confirm‑knop doet het werk
                else:
                    if len(input_text) < 15:
                        input_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Confirm‑knop
                if confirm_button.collidepoint(mx, my):
                    if input_text.strip() == "":
                        error_message = "Name cannot be empty"
                    elif not player_exists(input_text):
                        error_message = "Player doesn't exists!"
                    else:
                        return input_text

        # --- TEKENEN ---
        title = font.render("Enter your name", True, yellow)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

        # Inputveld
        pygame.draw.rect(screen, white, (568, 500, 400, 50), border_radius=8)
        name_label = smaller_font.render(input_text, True, black)
        screen.blit(name_label, (568, 500))

        # Confirm‑knop
        confirm_button = pygame.Rect(618, 570, 300, 60)
        draw_button("Confirm", 618, 570, 300, 60,
                    confirm_button.collidepoint(pygame.mouse.get_pos()))

        # Foutmelding
        if error_message:
            err = smaller_font.render(error_message, True, red)
            screen.blit(err, (WIDTH//2 - err.get_width()//2, 630))

        pygame.display.flip()


def draw_button(text, x, y, w, h, hover):
    color = darkblue if hover else darkgreen
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    label = smaller_font.render(text, True, yellow)
    screen.blit(label, (x + (w - label.get_width()) // 2,
                        y + (h - label.get_height()) // 2))


def text_input(prompt):
    input_text = ""
    active = True

    while active:

        label = smaller_font.render(prompt, True, white)
        screen.blit(label, (50, 200))

        box = pygame.Rect(50, 260, 700, 50)
        pygame.draw.rect(screen, white, box, 2)

        text_surface = smaller_font.render(input_text, True, white)
        screen.blit(text_surface, (60, 270))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text.strip()

                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

                else:
                    input_text += event.unicode


def start_screen():
    start_background_music()
    while True:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # Knoppen
        mouse = pygame.mouse.get_pos()
        # click = pygame.mouse.get_pressed()

        btn_new = pygame.Rect(443, 512, 300, 70)
        btn_existing = pygame.Rect(793, 512, 300, 70)

        hover_new = btn_new.collidepoint(mouse)
        hover_existing = btn_existing.collidepoint(mouse)

        draw_button("New player", 443, 512, 300, 70, hover_new)
        draw_button("Returning player", 793, 512, 300, 70, hover_existing)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # --- NEW PLAYER ---
                if hover_new:
                    name = new_player_screen()
                    stop_background_music()
                    start_blackjack_game(name)

                # --- RETURNING PLAYER ---
                if hover_existing:
                    # name = text_input("Geef je spelersnaam:")
                    # if player_exists(name):
                    #     return load_player(name)
                    # else:
                    #     continue
                    name = existing_player_screen()
                    stop_background_music()
                    start_blackjack_game(name)


start_screen()
