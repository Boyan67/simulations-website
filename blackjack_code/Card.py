class Card:
    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.value = value

    def show(self):
        print("{} of {} | value: {}".format(self.rank, self.suit, self.value))

    def __str__(self):
        return f"{self.rank} of {self.suit}"
