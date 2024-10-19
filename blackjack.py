import random

all_suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
all_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] # Ace is handled seperately

def create_deck():
    # First element is top of deck
    deck = [f"{rank} of {suit}" for suit in all_suits for rank in all_ranks]
    return deck    
        
def shuffle_deck(deck):
    return random.shuffle(deck)

def sum_hand(hand):
    # Get the ranks of the cards
    ranks = [card.split()[0] for card in hand]
    
    # Remove aces as they are counted last
    num_aces = ranks.count("Ace")
    if num_aces > 0:
        ranks = [rank for rank in ranks if rank != "Ace"]
        
    # Sum the values of the cards (w/o ace)
    hand_total = sum([card_values[all_ranks.index(rank)] for rank in ranks])
    
    # Add aces
    for _ in range(num_aces):
        if hand_total + 11 > 21:
            hand_total += 1
        else:
            hand_total += 11
    return hand_total    

def print_hand(hand):
    print("\n".join(hand))
    print("Value: ", sum_hand(hand), "\n")

def print_hands(player, dealer):
    print("Your hand:")
    print_hand(player)
    print("Dealer's hand:")
    print_hand(dealer)

def player_input():
    choice = ""
    while choice not in ["h", "hit", "s", "stand"]:
        choice = input("Would you like to hit (h) or stand (s)? ").lower().strip()
    return choice[0]

def check_blackjack(player, dealer):
    total_player = sum_hand(player)
    total_dealer = sum_hand(dealer)

    if total_player == 21 and total_dealer != 21:
        print("Blackjack! You win!")
        exit()
    elif total_player == 21 and total_dealer == 21:
        print("Blackjack! It's a tie!")
        exit()

def determine_winner(player, dealer):
    print("\nFinal hands:")
    print_hands(player, dealer)
    
    total_player = sum_hand(player)
    total_dealer = sum_hand(dealer)
    if total_player > total_dealer:
        return ("You win!")
    elif total_player < total_dealer:
        return ("House wins!")
    else:
        return ("It's a tie!")
    
def play_blackjack():
    deck = create_deck()
    shuffle_deck(deck)
    
    # Deal the cards
    player = [deck.pop(0), deck.pop(0)]
    dealer = [deck.pop(0), deck.pop(0)]
    
    # Player's turn
    is_dealers_turn = False
    while not is_dealers_turn:
        print_hands(player, dealer[:1])
        
        if len(player) == 2:
            check_blackjack(player, dealer)
        
        choice = player_input()
        
        if choice == "h":
            player.append(deck.pop(0))
            if sum_hand(player) > 21:
                print_hand(player)
                print("You busted! House wins!")
                return
        else:
            is_dealers_turn = True
    
    # Dealer draws until total >= 17
    while sum_hand(dealer) < 17:
        dealer.append(deck.pop(0))
        if sum_hand(dealer) > 21:
                print("Dealer's hand:")
                print_hand(dealer)
                print("House busted! You win!")
                return
    
    # Determine winner
    winner = determine_winner(player, dealer)
    print(winner)

if __name__ == "__main__":
    play_blackjack()
    