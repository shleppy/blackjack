#!/usr/bin/env python3
import os
from random import shuffle


def suits():
    return ['S', 'C', 'H', 'D']


def ranks():
    return ['2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K', 'A']


class Card:
    """Playing card representation"""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return self.suit + self.rank

    def __str__(self):
        return self.suit + self.rank

    def __lt__(self, other):
        return self.suit < other.suit

    def __gt__(self, other):
        return self.suit > other.suit


class Deck:
    """Deck of cards"""
    def __init__(self):
        self.cards = sorted([Card(suit, rank) for rank in ranks() for suit in suits()])

    def shuffle_cards(self):
        shuffle(self.cards)

    def return_card(self, card):
        self.cards.insert(0, card)

    def draw(self):
        return self.cards.pop()

    @staticmethod
    def print_original():
        fresh_deck = sorted([Card(suit, rank) for rank in ranks() for suit in suits()])
        result = ''
        suit = ''
        for card in fresh_deck:
            if suit != card.suit:
                result += '\n'
            result += str(card)
            result += ' '
            suit = card.suit
        return result


class Hand:
    def __init__(self):
        self.cards = []

    def __getitem__(self, item):
        return self.cards[item]

    def deal(self, card):
        self.cards.append(card)

    def value(self):
        total = 0
        non_aces = [card for card in self.cards if card.rank != 'A']
        aces = [card for card in self.cards if card.rank == 'A']

        for card in non_aces:
            total += 10 if card.rank in 'JQK' else int(card.rank)

        for card in aces:
            total += 11 if total < 10 else 1

        return total


class Score:
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def __str__(self):
        return '[W: ' + str(self.wins) + '] [L: ' + str(self.losses) + '] [D: ' + str(self.draws) + ']'


def play_again():
    choice = input('Would you like to play again? (Y/n): ')
    return False if choice == 'n' else True


def play():
    score = Score()

    playing = True
    while playing:
        deck = Deck()
        deck.shuffle_cards()

        player = Hand()
        dealer = Hand()

        player.deal(deck.draw())
        dealer.deal(deck.draw())
        player.deal(deck.draw())
        dealer.deal(deck.draw())

        standing = False
        first_hand = True

        while round:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print('%%           BlackJack           %%')
            print('%%-------------------------------%%')
            print('%%      ' + str(score) + '     %%')
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n')
            dealer_score = dealer.value()
            player_score = player.value()

            if standing:
                print('Dealer Cards: [{}] ({})'.format(']['.join(str(x) for x in dealer), dealer_score))
            else:
                print('Dealer Cards: [{}][?]'.format(dealer[0]))

            print('Your Cards:   [{}] ({})'.format(']['.join(str(x) for x in player), player_score))
            print('')

            if standing:
                if dealer_score > 21:
                    print('Dealer busted, You Win!')
                    score.wins += 1
                elif player_score == dealer_score:
                    print('Push, nobody won!')
                    score.draws += 1
                elif player_score > dealer_score:
                    print('You beat the dealer, You Won!')
                    score.wins += 1
                else:
                    print('You lost :(')
                    score.losses += 1

                break

            if first_hand and player_score == 21:
                print('Blackjack! You Won!')
                score.wins += 1
                break

            if player_score > 21:
                print('You busted!')
                score.losses += 1
                break

            print('What would you like to do?')
            print(' [1] Hit')
            print(' [2] Stand')

            print('')
            choice = input('Your choice: ')
            print('')

            if choice == '1':
                player.deal(deck.draw())
            elif choice == '2':
                standing = True
                while dealer.value() <= 16:
                    dealer.deal(deck.draw())

        if play_again():
            continue
        else:
            exit(0)


play()
