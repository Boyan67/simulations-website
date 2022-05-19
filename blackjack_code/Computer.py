from blackjack_code.Hand import Hand


class Computer:
    def __init__(self):
        self.hand = Hand()

    def reset_hand(self):
        self.hand = Hand()
