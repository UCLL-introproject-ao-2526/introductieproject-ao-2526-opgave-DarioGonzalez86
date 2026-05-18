# black jack in python wth pygame!
import copy
import random
import pygame
import sys
import csv
import os

pygame.init()
pygame.mixer.init()

# Variables, constants, globals
WIDTH, HEIGHT = 1536, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame Blackjack!')
FONT = pygame.font.Font("Assets/Fonts/DejaVuSans.ttf", 42)
SMALLER_FONT = pygame.font.Font("Assets/Fonts/DejaVuSans.ttf", 34)
CSV_FILE = "players.csv"
WIN_STRING = "Win"
LOSE_STRING = "Lose"
DRAW_STRING = "Draw"

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['♠', '♥', '♦', '♣']
one_deck = [value + suit for value in cards for suit in suits]
decks = 4
fps = 60
timer = pygame.time.Clock()

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


# Help functions to load and save players from/to CSV file
def load_players_csv(path=CSV_FILE):
    players = {}
    if not os.path.exists(path):
        return players
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            players[row["Name"]] = {
                WIN_STRING: int(row[WIN_STRING]),
                LOSE_STRING: int(row[LOSE_STRING]),
                DRAW_STRING: int(row[DRAW_STRING])
            }
    return players


def save_players_csv(players, path=CSV_FILE):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["Name", WIN_STRING, LOSE_STRING, DRAW_STRING])
        writer.writeheader()
        for name, stats in players.items():
            writer.writerow({
                "Name": name,
                WIN_STRING: stats[WIN_STRING],
                LOSE_STRING: stats[LOSE_STRING],
                DRAW_STRING: stats[DRAW_STRING]
            })


# Functions to add a new player in the csv file
def add_new_player(player):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow([player, 0, 0, 0])  # win, lose, draw


# Functions to check if a player exists in  the csv file
def check_player(player):
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            name = row[0].strip().lower()
            if name == player.strip().lower():
                return True
    return False


# Function to get the correct name of the player (to show correct statistics if not the correct upper/lower case was used)
def get_correct_player_name(player):
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].strip().lower() == player.strip().lower():
                return row[0]
    return None


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


# Validate players names for new and existing players via Class Player
def validate_new_player(name):
    if not name:
        return False, "Name cannot be empty"
    if check_player(name):
        return False, f'Player with name "{name}" already exists!'
    add_new_player(name)
    return True, None


def validate_existing_player(name):
    correct_name = get_correct_player_name(name)
    if correct_name is None:
        return False, f'Player with name "{name}" does not exist!'
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


# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    return current_hand, current_deck


# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = sum(1 for card in hand if card[:-1] == 'A')
    for i in range(len(hand)):
        card_value = hand[i][:-1]
        # for 2,3,4,5,6,7,8,9 - just add the number to total
        for j in range(8):
            if card_value == cards[j]:
                hand_score += int(card_value)
        # for 10 and face cards, add 10
        if card_value in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces start by adding 11, we'll check if we need to reduce afterwards
        elif card_value == 'A':
            hand_score += 11
    # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score


# draw scores for player and dealer on screen
def draw_scores(player, dealer, reveal_dealer):
    # score player
    text_player = SMALLER_FONT.render(f"Score: {player}", True, DARKGREEN)
    w = text_player.get_width()
    h = text_player.get_height()
    x, y = 350, 400

    pygame.draw.rect(screen, YELLOW, (x, y, w, h),
                     border_radius=10)
    screen.blit(text_player, (x + (w - text_player.get_width()) // 2,
                              y + (h - text_player.get_height()) // 2))

    # score dealer
    if reveal_dealer:
        text_dealer = SMALLER_FONT.render(
            f"Score: {dealer}", True, DARKGREEN)
        w2 = text_dealer.get_width()
        h2 = text_dealer.get_height()
        x2, y2 = 350, 120

        pygame.draw.rect(screen, YELLOW,
                         (x2, y2, w2, h2), border_radius=10)
        screen.blit(text_dealer, (x2 + (w2 - text_dealer.get_width()) // 2,
                                  y2 + (h2 - text_dealer.get_height()) // 2))


# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        value = player[i][:-1]
        suit = player[i][-1]
        color = RED if suit in ['♥', '♦'] else BLACK
        pygame.draw.rect(screen, 'white', [
            70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(SMALLER_FONT.render(value + suit, True,
                    color), (75 + 70 * i, 465 + 5 * i))
        screen.blit(SMALLER_FONT.render(value + suit, True,
                    color), (75 + 70 * i, 635 + 5 * i))
        if color == RED:
            pygame.draw.rect(
                screen, RED, [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)
        else:
            pygame.draw.rect(
                screen, BLACK, [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

    # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        value = dealer[i][:-1]
        suit = dealer[i][-1]
        color = RED if suit in ['♥', '♦'] else BLACK
        pygame.draw.rect(screen, WHITE, [
            70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(SMALLER_FONT.render(
                value + suit, True, color), (75 + 70 * i, 165 + 5 * i))
            screen.blit(SMALLER_FONT.render(
                value + suit, True, color), (75 + 70 * i, 335 + 5 * i))
        else:
            screen.blit(SMALLER_FONT.render('???', True, BLACK),
                        (75 + 70 * i, 165 + 5 * i))
            screen.blit(SMALLER_FONT.render('???', True, BLACK),
                        (75 + 70 * i, 335 + 5 * i))
        if color == RED:
            pygame.draw.rect(
                screen, RED, [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)
        else:
            pygame.draw.rect(screen, BLACK, [
                70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)


# draw game conditions and buttons
def draw_game(act, record, results, outcome, name):
    button_list = []
    player_name = name
    # initially on startup (not active) only option is to deal new hand
    if not act:
        mouse = pygame.mouse.get_pos()
        deal = pygame.Rect(618, 80, 300, 100)
        hover_deal = deal.collidepoint(mouse)
        draw_button("Deal hand", deal, hover_deal)
        button_list.append(deal)

    # once game started, shot hit and stand buttons and win/loss records
    else:
        mouse = pygame.mouse.get_pos()
        hit = pygame.Rect(10, 700, 300, 100)
        hover_hit = hit.collidepoint(mouse)
        draw_button("Hit", hit, hover_hit)
        button_list.append(hit)
        stand = pygame.Rect(350, 700, 300, 100)
        hover_stand = stand.collidepoint(mouse)
        draw_button("Stand", stand, hover_stand)
        button_list.append(stand)

        player_text = SMALLER_FONT.render(
            f"Game history of {player_name}:", True, WHITE)
        player_text_width = player_text.get_width()
        score_text = SMALLER_FONT.render(
            f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, WHITE)
        score_text_width = score_text.get_width()
        screen_width = screen.get_width()
        x1 = (screen_width - player_text_width) // 2
        x2 = (screen_width - score_text_width) // 2
        screen.blit(player_text, (x1, 20))
        screen.blit(score_text, (x2, 80))

    # if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if outcome != 0:
        text_result = FONT.render(results[outcome], True, RED)
        text_width = text_result.get_width()
        text_height = text_result.get_height()
        screen_width = screen.get_width()
        x = (screen_width - text_width) // 2

        pygame.draw.rect(
            screen, YELLOW, (x, 500, text_width, text_height), border_radius=10)
        screen.blit(text_result, (x, 500))

        mouse = pygame.mouse.get_pos()
        new_hand = pygame.Rect(150, 220, 300, 100)
        hover_new = new_hand.collidepoint(mouse)
        draw_button("New hand", new_hand, hover_new)
        button_list.append(new_hand)

    return button_list


# check endgame conditions function
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # check end game scenarios is player has stood, busted or blackjacked
    # result 1- player bust, 2-win, 3-loss, 4-push
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add


# [dn] alles zit in start_blackjack_game, dus niet zeker waarom het 'start' is?
def start_blackjack_game(name):
    active = False
    # win, loss, draw/push
    records = [0, 0, 0]
    player_score = 0
    dealer_score = 0
    initial_deal = False
    my_hand = []
    dealer_hand = []
    outcome = 0
    reveal_dealer = False
    hand_active = False
    add_score = False
    results = ['', f'{name} BUSTED o_O',
               f'{name} WINS! :)', 'DEALER WINS :(', 'TIE GAME...']

    # Load players in a dictionary to update file later with new scores
    players = load_players_csv()
    if name not in players:
        players[name] = {WIN_STRING: 0, LOSE_STRING: 0, DRAW_STRING: 0}

    records = [
        players[name][WIN_STRING],
        players[name][LOSE_STRING],
        players[name][DRAW_STRING]
    ]

    # main game loop
    run = True
    while run:
        # run game at our framerate and fill screen with bg color
        timer.tick(fps)
        screen.blit(BACKGROUND, (0, 0))
        # initial deal to player and dealer
        if initial_deal:
            for i in range(2):
                my_hand, game_deck = deal_cards(my_hand, game_deck)
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            initial_deal = False
        # once game is activated, and dealt, calculate scores and display cards
        if active:
            player_score = calculate_score(my_hand)
            draw_cards(my_hand, dealer_hand, reveal_dealer)
            if reveal_dealer:
                dealer_score = calculate_score(dealer_hand)
                if dealer_score < 17:
                    dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            draw_scores(player_score, dealer_score, reveal_dealer)
        buttons = draw_game(active, records, results, outcome, name)

        # event handling, if quit pressed, then exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if not active:
                    if buttons[0].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        add_score = True
                else:
                    # if player can hit, allow them to draw a card
                    if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                        my_hand, game_deck = deal_cards(my_hand, game_deck)
                    # allow player to end turn (stand)
                    elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                        reveal_dealer = True
                        hand_active = False
                    # [dn] niet specifiek hier, maar we zitten hier wel echt diep in if's and while's
                    # probeer het wat op te splitsen in methods, of een andere manier om niet zoveel te nesten
                    elif len(buttons) == 3:
                        if buttons[2].collidepoint(event.pos):
                            active = True
                            initial_deal = True
                            game_deck = copy.deepcopy(decks * one_deck)
                            my_hand = []
                            dealer_hand = []
                            outcome = 0
                            hand_active = True
                            reveal_dealer = False
                            add_score = True
                            dealer_score = 0
                            player_score = 0

        # if player busts, automatically end turn - treat like a stand
        if hand_active and player_score >= 21:
            hand_active = False
            reveal_dealer = True

        outcome, records, add_score = check_endgame(
            hand_active, dealer_score, player_score, outcome, records, add_score)

        # Update CSV when hand is finished with the dictionary
        if outcome != 0 and not add_score:
            players[name][WIN_STRING] = records[0]
            players[name][LOSE_STRING] = records[1]
            players[name][DRAW_STRING] = records[2]
            save_players_csv(players)

        pygame.display.flip()
    pygame.quit()


start_screen()
