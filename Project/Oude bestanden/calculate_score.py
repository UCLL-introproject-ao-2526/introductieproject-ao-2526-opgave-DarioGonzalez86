# Dit was enkel nodig om de bug te vinden in de functie calculate_score(hand). Ik heb dit ondertusen in een aparte map gezet om de bestanden overzichtelijker te houden.

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['♠', '♥', '♦', '♣']
one_deck = [value + suit for value in cards for suit in suits]
decks = 4

# oude functie:


def calculate_score(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    print(aces_count)
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


# nieuwe functie met aanpassing van aces_count:
def calculate_score_new(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = sum(1 for card in hand if card[:-1] == 'A')
    print(aces_count)
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


hand = ["A♠", "9♦"]
hand2 = ["A♠", "9♦", "A♦"]
calculate_score(hand)
calculate_score_new(hand)
calculate_score(hand2)
calculate_score_new(hand2)
