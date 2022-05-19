from blackjack_code.Hand import Hand


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.bank = 10000

    def update_bank(self, amount):
        self.bank += amount

    def reset_hand(self):
        self.hand = Hand()
