# black jack in python wth pygame!
import copy
import random
import pygame
import csv
import os
import sys


def load_players_csv(path="players.csv"):
    players = {}
    if not os.path.exists(path):
        return players
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            players[row["Name"]] = {
                "Win": int(row["Win"]),
                "Lose": int(row["Lose"]),
                "Draw": int(row["Draw"])
            }
    return players


def save_players_csv(players, path="players.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Win", "Lose", "Draw"])
        writer.writeheader()
        for name, stats in players.items():
            writer.writerow({
                "Name": name,
                "Win": stats["Win"],
                "Lose": stats["Lose"],
                "Draw": stats["Draw"]
            })


def start_blackjack_game(name):

    pygame.init()
    # game variables
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♠', '♥', '♦', '♣']
    one_deck = [value + suit for value in cards for suit in suits]
    decks = 4
    WIDTH = 1536
    HEIGHT = 1024
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('Pygame Blackjack!')
    fps = 60
    timer = pygame.time.Clock()
    font = pygame.font.Font("Assets/Fonts/DejaVuSans.ttf", 44)
    smaller_font = pygame.font.Font("Assets/Fonts/DejaVuSans.ttf", 36)

    #  kleuren via adobe colorpalette op basis van achtergrond
    darkblue = (22, 45, 115)
    darkgreen = (25, 64, 35)
    yellow = (242, 192, 99)
    red = (217, 7, 7)
    background = pygame.image.load("Assets/Images/blackjack.png")
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

    # spelers ophalen en scores te kunnen updaten later.
    players = load_players_csv()
    if name not in players:
        players[name] = {"Win": 0, "Lose": 0, "Draw": 0}

    records = [
        players[name]["Win"],
        players[name]["Lose"],
        players[name]["Draw"]
    ]

    # draw buttons:
    def draw_button(text, x, y, w, h, hover):
        color = darkblue if hover else darkgreen
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
        label = smaller_font.render(text, True, yellow)
        screen.blit(label, (x + (w - label.get_width()) // 2,
                            y + (h - label.get_height()) // 2))

    # deal cards by selecting randomly from deck, and make function for one card at a time

    def deal_cards(current_hand, current_deck):
        card = random.randint(0, len(current_deck))
        current_hand.append(current_deck[card - 1])
        current_deck.pop(card - 1)
        return current_hand, current_deck

    # draw scores for player and dealer on screen

    def draw_scores(player, dealer):
        # score speler
        text_player = smaller_font.render(f"Score: {player}", True, darkgreen)
        w = text_player.get_width()
        h = text_player.get_height()
        x, y = 350, 400

        pygame.draw.rect(screen, yellow, (x, y, w, h),
                         border_radius=10)
        screen.blit(text_player, (x + (w - text_player.get_width()) // 2,
                                  y + (h - text_player.get_height()) // 2))

        # score dealer
        if reveal_dealer:
            text_dealer = smaller_font.render(
                f"Score: {dealer}", True, darkgreen)
            w2 = text_dealer.get_width()
            h2 = text_dealer.get_height()
            x2, y2 = 350, 120

            pygame.draw.rect(screen, yellow,
                             (x2, y2, w2, h2), border_radius=10)
            screen.blit(text_dealer, (x2 + (w2 - text_dealer.get_width()) // 2,
                                      y2 + (h2 - text_dealer.get_height()) // 2))

    # draw cards visually onto screen

    def draw_cards(player, dealer, reveal):
        for i in range(len(player)):
            value = player[i][:-1]
            suit = player[i][-1]
            color = 'red' if suit in ['♥', '♦'] else 'black'
            pygame.draw.rect(screen, 'white', [
                70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
            screen.blit(smaller_font.render(value + suit, True,
                        color), (75 + 70 * i, 465 + 5 * i))
            screen.blit(smaller_font.render(value + suit, True,
                        color), (75 + 70 * i, 635 + 5 * i))
            if color == 'red':
                pygame.draw.rect(
                    screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)
            else:
                pygame.draw.rect(
                    screen, 'black', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

        # if player hasn't finished turn, dealer will hide one card
        for i in range(len(dealer)):
            value = dealer[i][:-1]
            suit = dealer[i][-1]
            color = 'red' if suit in ['♥', '♦'] else 'black'
            pygame.draw.rect(screen, 'white', [
                70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
            if i != 0 or reveal:
                screen.blit(smaller_font.render(
                    value + suit, True, color), (75 + 70 * i, 165 + 5 * i))
                screen.blit(smaller_font.render(
                    value + suit, True, color), (75 + 70 * i, 335 + 5 * i))
            else:
                screen.blit(smaller_font.render('???', True, 'black'),
                            (75 + 70 * i, 165 + 5 * i))
                screen.blit(smaller_font.render('???', True, 'black'),
                            (75 + 70 * i, 335 + 5 * i))
            if color == 'red':
                pygame.draw.rect(
                    screen, 'red', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)
            else:
                pygame.draw.rect(screen, 'black', [
                    70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)

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

    # draw game conditions and buttons
    def draw_game(act, record, result, name):
        button_list = []
        player_name = name
        # initially on startup (not active) only option is to deal new hand
        if not act:
            mouse = pygame.mouse.get_pos()
            deal = pygame.Rect(618, 80, 300, 100)
            hover_deal = deal.collidepoint(mouse)
            draw_button("Deal hand", 618, 80, 300, 100, hover_deal)
            button_list.append(deal)

        # once game started, shot hit and stand buttons and win/loss records
        else:
            mouse = pygame.mouse.get_pos()
            hit = pygame.Rect(10, 700, 300, 100)
            hover_hit = hit.collidepoint(mouse)
            draw_button("Hit", 10, 700, 300, 100, hover_hit)
            button_list.append(hit)
            stand = pygame.Rect(350, 700, 300, 100)
            hover_stand = stand.collidepoint(mouse)
            draw_button("Stand", 350, 700, 300, 100, hover_stand)
            button_list.append(stand)

            player_text = smaller_font.render(
                f"Game history of {player_name}:", True, "white")
            player_text_width = player_text.get_width()
            score_text = smaller_font.render(
                f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, "white")
            score_text_width = score_text.get_width()
            screen_width = screen.get_width()
            x1 = (screen_width - player_text_width) // 2
            x2 = (screen_width - score_text_width) // 2
            screen.blit(player_text, (x1, 20))
            screen.blit(score_text, (x2, 80))

        # if there is an outcome for the hand that was played, display a restart button and tell user what happened
        if result != 0:
            text_result = font.render(results[result], True, red)
            text_width = text_result.get_width()
            text_height = text_result.get_height()
            screen_width = screen.get_width()
            x = (screen_width - text_width) // 2

            pygame.draw.rect(
                screen, yellow, (x, 500, text_width, text_height), border_radius=10)
            screen.blit(text_result, (x, 500))

            mouse = pygame.mouse.get_pos()
            new_hand = pygame.Rect(150, 220, 300, 100)
            hover_new = new_hand.collidepoint(mouse)
            draw_button("New hand", 150, 220, 300, 100, hover_new)
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

    # main game loop
    run = True
    while run:
        # run game at our framerate and fill screen with bg color
        timer.tick(fps)
        screen.blit(background, (0, 0))
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
            draw_scores(player_score, dealer_score)
        buttons = draw_game(active, records, outcome, name)

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

        # Update CSV when hand is finished
        if outcome != 0 and not add_score:
            players[name]["Win"] = records[0]
            players[name]["Lose"] = records[1]
            players[name]["Draw"] = records[2]
            save_players_csv(players)

        pygame.display.flip()
    pygame.quit()
