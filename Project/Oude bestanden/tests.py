from blackjack import calculate_score


def test_single_ace_with_9():
    hand = ["A♠", "9♦"]
    expected = 20
    actual = calculate_score(hand)
    assert expected == actual


def test_ace_becomes_one():
    hand = ["A♠", "9♦", "8♣"]  # 11 + 9 + 8 = 28 → A moet 1 worden → 18
    expected = 18
    actual = calculate_score(hand)
    assert expected == actual


def test_two_aces():
    hand = ["A♠", "A♦"]  # 11 + 11 = 22 → één A wordt 1 → 12
    expected = 12
    actual = calculate_score(hand)
    assert expected == actual


def test_three_aces():
    hand = ["A♠", "A♦", "A♣"]  # 11 + 11 + 11  = 33 → twee A's worden 1 → 13
    expected = 13
    actual = calculate_score(hand)
    assert expected == actual


def test_two_aces_with_9():
    hand = ["A♠", "A♦", "9♣"]  # 11 + 11 + 9 = 31 → één A wordt 1 → 21
    expected = 21
    actual = calculate_score(hand)
    assert expected == actual


def test_face_cards():
    hand = ["K♠", "Q♦"]
    expected = 20
    actual = calculate_score(hand)
    assert expected == actual


def test_mixed_hand():
    hand = ["A♠", "5♦", "K♣"]  # 11 + 5 + 10 = 26 → A wordt 1 → 16
    expected = 16
    actual = calculate_score(hand)
    assert expected == actual
