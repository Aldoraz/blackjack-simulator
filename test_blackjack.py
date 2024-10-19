import unittest
from unittest.mock import patch
from blackjack import *

class TestBlackjack(unittest.TestCase):

    def test_create_deck(self):#
        # Deck should have 52 cards and no duplicates
        deck = create_deck()
        self.assertEqual(len(deck), 52)
        self.assertEqual(len(set(deck)), 52)

    def test_shuffle_deck(self):
        # Deck should still have 52 cards and different order
        # If this fails, despite correct implementations ... congrats?
        # You just witnessed a event less likely than 5 back to back lottery wins.
        # 1 / 52! if you are curious.
        deck = create_deck()
        deck_before = deck.copy()
        shuffle_deck(deck)
        self.assertEqual(len(deck), 52)  
        self.assertNotEqual(deck, deck_before)  

    def test_sum_hand(self):
        # Should sum the hand correctly for any hand and properly handle aces
        self.assertEqual(sum_hand(["Ace of Spades", "10 of Hearts"]), 21)
        self.assertEqual(sum_hand(["Ace of Spades", "Ace of Hearts", "9 of Diamonds"]), 21)
        self.assertEqual(sum_hand(["2 of Hearts", "3 of Clubs", "4 of Diamonds"]), 9)
        self.assertEqual(sum_hand(["King of Spades", "Queen of Hearts"]), 20)
        self.assertEqual(sum_hand(["Ace of Spades", "Ace of Hearts"]), 12)
        self.assertEqual(sum_hand(["Ace of Spades", "Ace of Hearts", "Ace of Diamonds"]), 13)
        self.assertEqual(sum_hand(["Ace of Spades", "Ace of Hearts", "Ace of Diamonds", "Ace of Clubs"]), 14)
        self.assertEqual(sum_hand(["Ace of Spades", "9 of Hearts"]), 20)
        self.assertEqual(sum_hand(["Ace of Spades", "9 of Hearts", "2 of Clubs"]), 12)
        self.assertEqual(sum_hand(["Ace of Spades", "9 of Hearts", "King of Diamonds"]), 20)
        self.assertEqual(sum_hand(["Ace of Spades", "Ace of Hearts", "9 of Diamonds"]), 21)
        self.assertEqual(sum_hand(["Jack of Clubs", "Queen of Hearts"]), 20)
        self.assertEqual(sum_hand(["King of Spades", "King of Diamonds", "2 of Hearts"]), 22)
        self.assertEqual(sum_hand(["10 of Hearts", "7 of Spades", "5 of Clubs"]), 22)
        self.assertEqual(sum_hand(["Ace of Spades", "Ace of Hearts", "9 of Diamonds", "10 of Clubs"]), 21)  # 1 + 1 + 9 + 10

    @patch('builtins.input', side_effect=['h'])
    def test_player_input_hit(self, mock_input):
        # Should return 'h' for "hit"
        result = player_input()
        self.assertEqual(result, 'h')  
    @patch('builtins.input', side_effect=['stand'])
    def test_player_input_stand(self, mock_input):
        # Should return 's' for "stand" and handle case insensitivity
        result = player_input()
        self.assertEqual(result, 's')  
    @patch('builtins.input', side_effect=['StAnd' ])
    def test_player_case_insensitivity(self, mock_input):
        # Should work with any case
        result = player_input()
        self.assertEqual(result, 's') 
    @patch('builtins.input', side_effect=['  h  '])
    def test_player_case_strip(self, mock_input):
        # Should remove whitespace
        result = player_input()
        self.assertEqual(result, 'h')  
    @patch('builtins.input', side_effect=['ewfcdwd', 'hello?', 'stand' ])
    def test_player_case_proper_input(self, mock_input):
        # Should keep asking until it gets a valid 'h', 'hit', 's', or 'stand'
        result = player_input()
        self.assertEqual(result, 's')  

    def test_check_blackjack(self):
        player = ["Ace of Spades", "10 of Hearts"]
        dealer = ["9 of Clubs", "Queen of Diamonds"]
        with self.assertRaises(SystemExit):
            check_blackjack(player, dealer)  # Player should win and quit

        player = ["Ace of Spades", "10 of Hearts"]
        dealer = ["Ace of Clubs", "Queen of Diamonds"]
        with self.assertRaises(SystemExit):
            check_blackjack(player, dealer)  # Should tie and quit

    def test_determine_winner(self):
        player = ["10 of Hearts", "8 of Diamonds"]
        dealer = ["7 of Clubs", "9 of Spades"]
        result = determine_winner(player, dealer)
        self.assertEqual(result, "You win!")  # Player total: 18, Dealer total: 16
        player = ["5 of Hearts", "7 of Diamonds"]
        dealer = ["King of Clubs", "7 of Spades"]
        result = determine_winner(player, dealer)
        self.assertEqual(result, "House wins!")  # Player total: 12, Dealer total: 17
        player = ["10 of Diamonds", "Jack of Clubs"]
        dealer = ["King of Spades", "Queen of Hearts"]
        result = determine_winner(player, dealer)
        self.assertEqual(result, "It's a tie!")  # Both totals: 20
        player = ["Ace of Spades", "10 of Hearts"]
        dealer = ["Queen of Diamonds", "King of Clubs"]
        result = determine_winner(player, dealer)
        self.assertEqual(result, "You win!")  # Player total: 21 (Blackjack), Dealer total: 20

if __name__ == '__main__':
    unittest.main()
