from blackjack_code.Card import Card
import random


class Deck:
    def __init__(self, size):
        self.cards = []
        self.build(size)

    def build(self, size):
        for i in range(size):
            self.build_deck()

    def build_deck(self):
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for r in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]:
                if r.isdigit():
                    val = int(r)
                elif r == "Ace":
                    val = 11
                else:
                    val = 10
                self.cards.append(Card(r, s, val))

    def show(self):
        str_rep = [str(x) for x in self.cards]
        print(str_rep)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

    def size(self):
        if len(self.cards) < 52:
            return .5
        else:
            return round(len(self.cards) / 52)
