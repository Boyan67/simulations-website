import csv
import random

from blackjack_code.Game import Game
from blackjack_code.Player import Player
import numpy as np
import scipy.stats as st
import statistics as stat

random.seed(25)
player = Player('Josh')
final_player_stack = []
final_bet_history = []
total_bets = []
total_player_win = 0
total_ties = 0
total_computer_win = 0


def print_hi():
    print("HELLOOOOOO WORLD!!!!!")


def output_report(player_stack):
    """
    Calculates and returns information for the simulation results
    :param player_stack: list of the player's bankroll after each round
    :return: A list of information on the results from the simulation
    """
    casino_advantage = round((10000 - np.mean(player_stack)) / np.mean(total_bets) * 100, 2)
    ci_l, ci_h = st.norm.interval(alpha=0.95, loc=np.mean(player_stack),
                                  scale=st.sem(player_stack))
    player_final_stack_test = [1 if i > 10000 else 0 for i in player_stack]
    mean = round(stat.mean(player_stack), 2)
    std_dev = round(stat.stdev(player_stack), 2)
    ci95 = round(ci_l, 2), (round(ci_h, 2))
    profit_realized = round((sum(player_final_stack_test) / len(player_final_stack_test)) * 100, 2)
    median = np.percentile(player_stack, 50)
    q1 = np.percentile(player_stack, 25)
    q3 = np.percentile(player_stack, 75)
    percent95 = np.percentile(player_stack, 95)
    percent5 = np.percentile(player_stack, 5)
    min_bankroll = min(player_stack)
    max_bankroll = max(player_stack)
    bet_mean = round(stat.mean(final_bet_history), 2)
    bet_median = np.percentile(final_bet_history, 50)
    max_bet = max(final_bet_history)
    return [mean, std_dev, ci95, profit_realized, casino_advantage, total_player_win, total_ties, total_computer_win,
            median, q1, q3, min_bankroll, max_bankroll, bet_mean, bet_median, max_bet, percent5, percent95]


# All card counting methods that will be used for the simulations_website
hi_lo = {
    "name": "Hi-Lo", "2": 1, "3": 1, "4": 1, "5": 1, "6": 1, "7": 0, "8": 0, "9": 0, "10": -1,
    "Jack": -1, "Queen": -1, "King": -1, "Ace": -1}
kiss = {
    "name": "KISS3", "2": 0, "3": 1, "4": 1, "5": 1, "6": 1, "7": 1, "8": 0, "9": 0, "10": -1,
    "Jack": -1, "Queen": -1, "King": -1, "Ace": -1}
zen = {
    "name": "ZEN", "2": 1, "3": 1, "4": 2, "5": 2, "6": 2, "7": 1, "8": 0, "9": 0, "10": -2,
    "Jack": -2, "Queen": -2, "King": -2, "Ace": -1}
hi_opt_2 = {
    "name": "Hi-Opt 2", "2": 1, "3": 1, "4": 2, "5": 2, "6": 1, "7": 1, "8": 0, "9": 0, "10": -2,
    "Jack": -2, "Queen": -2, "King": -2, "Ace": 0}
wong_halves = {
    "name": "Wong Halves", "2": 0.5, "3": 1, "4": 1, "5": 1.5, "6": 1, "7": .5, "8": 0, "9": -0.5, "10": -1,
    "Jack": -1, "Queen": -1, "King": -1, "Ace": -1}
revere_RAPC = {
    "name": "Revere RAPC", "2": 2, "3": 3, "4": 3, "5": 4, "6": 3, "7": 2, "8": 0, "9": -1, "10": -3,
    "Jack": -3, "Queen": -3, "King": -3, "Ace": -4}
no_card_counting = {
    "name": "no_card_counting", "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0,
    "Jack": 0, "Queen": 0, "King": 0, "Ace": 0}
decimal_counting2 = {
    "name": "decimal_counting", "2": 3.8, "3": 4.6, "4": 6.1, "5": 8, "6": 4.6, "7": 2.9, "8": -0.1,
    "9": -2, "10": -4.9, "Jack": -4.9, "Queen": -4.9, "King": -4.9, "Ace": -5.8}
practical = {"name": "practical", '2': 1, '3': 1, '4': 2, '5': 2, '6': 1, '7': 1, '8': 0, '9': -1, '10': -1, 'Jack': -1,
             'Queen': -1, 'King': -1, 'Ace': -2}


def single_simulation(strategy, decks, game_type, penetration, bet_size, counting_method):
    """
    Simulates a single simulation under specified conditions and creates
    a csv file with the player bankroll at each round.
    """
    file = open('blackjack_code/bankroll/TEST.csv', 'w')
    stack = []
    w = csv.writer(file)
    i = 0

    while i < 10000:
        i += 1
        game_set = Game(strategy, decks, game_type, penetration, bet_size, counting_method)
        result = game_set.play_game(player, 100)
        stack.append(result[-1])
        w.writerow(result[-1])
        final_player_stack.append(result[0])
    return round((stat.mean(final_player_stack)-10000) / 100, 2)


# single_simulation()
