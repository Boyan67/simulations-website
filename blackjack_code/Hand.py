class Hand:
    def __init__(self):
        self.cards = []
        self.total = 0
        self.bust = False
        self.ace_count = 0
        self.already_split = False
        self.bet = 0
        self.blackjack = False

    def check_blackjack(self):
        if self.total == 21:
            self.blackjack = True

    def add(self, card):
        self.cards.append(card)
        self.total += card.value

    def show_hand(self):
        for card in self.cards:
            card.show()

    def show_values(self):
        a = [x.value for x in self.cards]
        return str(a)

    def is_soft(self):
        count = 0
        for x in self.cards:
            if x.value == 11:
                count += 1
        if count == 1:
            return True
        elif count > 1:
            return False

    def draw(self, deck):
        drawn_card = deck.draw_card()
        self.cards.append(drawn_card)
        if drawn_card.value == 11:
            self.ace_count += 1
        if self.total + drawn_card.value > 21 and self.ace_count > 0:
            self.ace_count -= 1
            self.total -= 10
            self.total += drawn_card.value
        elif (self.total + drawn_card.value) > 21 and self.ace_count == 0:
            self.total += drawn_card.value
            self.bust = True
        else:
            self.total += drawn_card.value
        self.check_blackjack()
        return drawn_card

    def hit(self, deck):
        return self.draw(deck)

    def split(self, deck):
        a = self.cards.pop()
        self.total -= a.value
        if a.value == 11:
            self.total += 10
        self.draw(deck)
        self.check_blackjack()
        new_hand = Hand()
        new_hand.add(a)
        new_hand.draw(deck)
        new_hand.check_blackjack()
        return new_hand

    def return_cards(self):
        return self.cards
