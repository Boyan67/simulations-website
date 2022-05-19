from blackjack_code.Computer import Computer
from blackjack_code.Deck import Deck
from blackjack_code.no_bust_strategy import no_bust_strategy, mimic_dealer
from blackjack_code.strategy import basic_strategy


class Game:
    def __init__(self, strategy, num_decks, game_type, penetration, bet_size, card_counting):
        """
        Initialises the game class with all the simulation conditions.
        :param str strategy: specify one of mimic_dealer, never_bust or basic
        :param int num_decks: the number of decks for this game
        :param str game_type: S17 or H17
        :param double penetration: percentage of the deck is to be played (decimal between 0 and 1)
        :param str bet_size: what betting size to be used (i.e. true)
        :param dict card_counting: the card counting method to be used
        """
        self.deck = Deck(num_decks)
        self.computer = Computer()
        self.player_wins = 0
        self.computer_wins = 0
        self.ties = 0
        self.rounds = 1
        self.total_bets = 0
        self.num_decks = num_decks
        self.bj_pays = 1.5
        self.game_type = game_type
        self.split = True
        self.das = True
        self.cut = penetration
        self.running_count = 0
        self.true_count = 0
        self.bet_size = bet_size
        self.bet_history = []
        self.card_counting = card_counting
        self.strategy = strategy

    def update_running_count(self, card):
        """
        Updates the running count
        :param card: a card object
        """
        val = self.card_counting[card.rank]
        self.running_count += val

    def deal_cards(self, player):
        """
        Deals the player two cards and the dealer one card
        :param player: a player object
        """
        self.update_running_count(player.hand.draw(self.deck))
        self.update_running_count(self.computer.hand.draw(self.deck))
        self.update_running_count(player.hand.draw(self.deck))

    def check_win(self, hand, player):
        """
        Checks who won the round and updates the player bank accordingly
        :param hand: stores the player's cards
        :param player: the player to which the hand is connected to
        """
        if hand.total > 21:
            player.bank -= hand.bet
            self.computer_wins += 1
        elif self.computer.hand.total > 21:
            self.player_wins += 1
            if hand.total == 21:
                player.bank += hand.bet * self.bj_pays
            else:
                player.bank += hand.bet
        elif hand.total == self.computer.hand.total:
            self.ties += 1
        elif hand.total == 21:
            if len(hand.cards) == 2:
                self.player_wins += 1
                player.bank += hand.bet * self.bj_pays
            else:
                self.player_wins += 1
                player.bank += hand.bet
        elif self.computer.hand.total > hand.total:
            player.bank -= hand.bet
            self.computer_wins += 1
        else:
            player.bank += hand.bet
            self.player_wins += 1

    def penetration(self):
        if self.num_decks == 1 and self.cut == 0.75:
            return 18
        elif self.num_decks == 1 and self.cut == 0.9:
            return 15
        elif self.num_decks == 2 and self.cut == 0.9:
            return 19
        else:
            return (self.num_decks * 52) * (1 - self.cut)

    def computer_turn(self, computer, deck):
        # hits until it has a hard 17
        if self.game_type == "H17":
            while computer.hand.total < 17 or computer.hand.total == 17 and computer.hand.ace_count > 0:
                self.update_running_count(computer.hand.draw(deck))
        # stands on all 17s
        elif self.game_type == "S17":
            while computer.hand.total < 17:
                self.update_running_count(computer.hand.draw(deck))

    def decide_bet(self):
        """
        Decides how much to bet based on the true count and the betting system specified
        :return: the amount to bet
        """
        if self.bet_size == "true":
            if self.true_count <= 1:
                return 100
            elif 1 < self.true_count <= 15:
                return 100 * self.true_count
            else:
                return 100 * 15
        elif self.bet_size == "running":
            if self.running_count <= 1:
                return 100
            elif 1 < self.running_count <= 15:
                return 100 * self.running_count
            else:
                return 100 * 15
        elif self.bet_size == "true*2":
            if self.true_count * 2 <= 1:
                return 100
            elif 1 < self.true_count * 2 <= 15:
                return 100 * (self.true_count * 2)
            else:
                return 100 * 15
        elif self.bet_size == "true+2":
            if self.true_count + 2 <= 1:
                return 100
            elif 1 < self.true_count + 2 <= 15:
                return 100 * (self.true_count + 2)
            else:
                return 100 * 15
        elif self.bet_size == "true-2":
            if self.true_count - 2 <= 1:
                return 100
            elif 1 < self.true_count - 2 <= 15:
                return 100 * (self.true_count - 2)
            else:
                return 100 * 15
        else:
            return 100

    def play_basic_strategy(self, hand, up, deck, das):
        while not hand.bust:
            if self.strategy == "never_bust":
                turn = no_bust_strategy(hand, up, das)
            elif self.strategy == "mimic_dealer":
                turn = mimic_dealer(hand)
            else:
                turn = basic_strategy(hand, up, das)
            hands = []
            new_hand = 0
            if turn == "Y" and not hand.already_split:
                hand.already_split = True
                new_hand = hand.split(deck)
                self.update_running_count(hand.cards[1])
                self.update_running_count(new_hand.cards[1])
                new_hand.already_split = True
                new_hand.bet = hand.bet
                self.play_basic_strategy(hand, up, deck, das)
                self.play_basic_strategy(new_hand, up, deck, das)
            elif turn == "H":
                self.update_running_count(hand.hit(deck))
                self.play_basic_strategy(hand, up, deck, das)
            elif turn == "D" and len(hand.cards) == 2:
                hand.bet *= 2
                self.update_running_count(hand.hit(deck))

            hands.append(hand)
            if new_hand != 0:
                hands.append(new_hand)

            return hands

    def play_round(self, player):
        self.deal_cards(player)
        up = self.computer.hand.draw(self.deck)
        self.update_running_count(up)
        player.hand.bet = self.decide_bet()
        h = self.play_basic_strategy(player.hand, up.value, self.deck, self.das)
        self.computer_turn(self.computer, self.deck)

        for hand in h:
            self.bet_history.append(hand.bet)
            self.total_bets += hand.bet
            self.check_win(hand, player)

        player.reset_hand()
        self.computer.reset_hand()

    def play_game(self, player, rounds_limit):
        """
        Plays blackjack_code for the number of rounds specified and the simulation attributes specified in the Game instance
        :param player: a Player object
        :param rounds_limit: number of blackjack_code rounds to be played

        :return: a list of relevant results:
                    [final player money, total number of bets, number of wins for the player, number of ties,
                    computer wins, betting history, list of player's bankroll throughout each round.]

        """
        stack = [10000]
        player.bank = 10000
        while self.rounds <= rounds_limit:
            self.deck = Deck(self.num_decks)
            self.deck.shuffle()
            self.running_count = 0
            self.true_count = 0
            while len(self.deck.cards) > self.penetration():
                self.play_round(player)
                self.rounds += 1
                stack.append(player.bank)
                self.true_count = round((self.running_count / self.deck.size()) * 2) / 2
                if self.rounds > rounds_limit:
                    break
        return player.bank, self.total_bets, self.player_wins, self.ties, self.computer_wins, self.bet_history, stack
