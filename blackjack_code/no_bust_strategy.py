def no_bust_strategy(hand, up_card, das):
    choice = "S"
    if hand.total > 11:
        choice = "S"
    elif hand.total <= 11:
        choice = "H"
    return choice


def mimic_dealer(hand):
    choice = ""
    if hand.total < 17:
        choice = "H"
    elif hand.total >= 17:
        choice = "S"
    return choice
