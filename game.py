# *************
# This file contains game states implementation
# *************

import numpy as np
from cards import Card
from shoe import Shoe


# global variables
goal = 55
dealer_stand = 50


def initial_state(DECK_SIZE) -> tuple:

    dealer_hand = []
    player_hand = []
    shoe = Shoe(DECK_SIZE)

    return (player_hand, dealer_hand, shoe)


def show_hand(hand: Card):
    stringofCards = ""
    for card in hand:
        stringofCards += card.rank + " "

    return stringofCards


def draw_cards(player_hand, dealer_hand, remaining_cards) -> tuple:
    # draw 5 cards for player and dealer
    for i in range(5):
        player_hand.append(remaining_cards.draw())
        dealer_hand.append(remaining_cards.draw())

    return (player_hand, dealer_hand, remaining_cards)


def compare_hands(player_hand, dealer_hand) -> int:
    if score(player_hand) > score(dealer_hand):
        return 1
    elif score(player_hand) < score(dealer_hand):
        return -1
    else:
        return 0


def score(hand: Card) -> int:
    sum = 0
    for card in hand:
        if card.rank == 'J':
            sum += 10
        elif card.rank == 'Q':
            sum += 10
        elif card.rank == 'K':
            sum += 10
        elif card.rank == 'A':
            sum += 11
        else:
            sum += int(card.rank)

    return sum


def FiftyFive(player_score, dealer_score):

    if player_score == 55 and dealer_score == 55:
        print("Draw")
        return True
    elif player_score == 55:
        print("Player wins")
        return True
    elif dealer_score == 55:
        print("Dealer wins")
        return True
    else:
        return False


def dealer_turn(player_hand, dealer_hand, shoe) -> tuple:

    while score(dealer_hand) < 50:
        dealer_hand.append(shoe.draw())
        print("Dealer hand: " + show_hand(dealer_hand))
        print("Dealer score: " + str(score(dealer_hand)))

    dealer_busted = busted(dealer_hand)
    if(dealer_busted):
        print("Dealer busted, player wins")
        return (True, (player_hand, dealer_hand, shoe))

    return (False, (player_hand, dealer_hand, shoe))


def play_turn(player_hand, dealer_hand, shoe) -> tuple:

    print("Hit or stay?")
    choice = input()
    player_busted = busted(player_hand)

    while (player_busted == False and choice == "hit"):
        player_hand.append(shoe.draw())
        print("Player hand: " + show_hand(player_hand))
        print("Player score: " + str(score(player_hand)))
        player_busted = busted(player_hand)
        if(player_busted):
            print("Player busted, dealer wins")
            return (True, (player_hand, dealer_hand, shoe))
        print("Hit or stay?")
        choice = input()

    if choice == "stay":
        while score(dealer_hand) < score(player_hand):
            dealer_turn(player_hand, dealer_hand, shoe)

        if (compare_hands(player_hand, dealer_hand)) == 1 and busted(player_hand) == False:
            print("Player wins!")
        elif (compare_hands(player_hand, dealer_hand)) == -1 and busted(dealer_hand) == False:
            print("Dealer wins!")
        elif(compare_hands(player_hand, dealer_hand) == 0):
            print("Draw!")
        else:
            print()

    return player_hand, dealer_hand, shoe


def busted(hand):
    if score(hand) > 55:
        return True
    else:
        return False


if __name__ == '__main__':

    player_busted = False
    dealer_busted = False

    print("Welcome to Blackjack!")
    print("The goal is to get as close to 55 as possible without going over.")
    print("The dealer will stand on 50.")
    print("How many decks would you like to use?")
    DECK_SIZE = int(input())

    game_state = initial_state(DECK_SIZE)
    game_state = draw_cards(game_state[0], game_state[1], game_state[2])

    player_hand = game_state[0]
    dealer_hand = game_state[1]
    remaining_cards = game_state[2]

    print()
    print("Player hand: " + show_hand(player_hand))
    print("Dealer hand: " + show_hand(dealer_hand))
    print("Remaining cards: " + str(remaining_cards.count()))
    print()

    player_score = score(player_hand)
    dealer_score = score(dealer_hand)

    # evaluate the first five cards
    if(FiftyFive(player_score, dealer_score)):
        print()
        print("Player score: " + str(score(player_hand)) +
              " Dealer score: " + str(score(dealer_hand)))
    else:
        print("Player score: " + str(player_score))
        print("Dealer score: " + str(dealer_score))
        print("Remaining cards: " + str(remaining_cards.count()))

        play_turn(game_state[0], game_state[1], game_state[2])

        print()
        print("Player score: " + str(score(player_hand)) +
              " Dealer score: " + str(score(dealer_hand)))
