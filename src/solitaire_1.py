from itertools import chain
from random import seed, shuffle
from collections import defaultdict

def card_to_unicode(card):
    # Suit bases: Hearts, Diamonds, Clubs, Spades
    suit_bases = [0x1F0B1, 0x1F0C1, 0x1F0D1, 0x1F0A1]
    suit_idx = card // 13
    rank_idx = card % 13  # 0 (Ace) to 12 (King)
    base = suit_bases[suit_idx]
    # Unicode skips standard J,Q,K by inserting a 'Knight' at offset 11.
    # We skip that offset if the rank is Jack (11) or higher.
    if rank_idx >= 11:
        return chr(base + rank_idx + 1)
    return chr(base + rank_idx)


def is_picture_card(card):
    """Check if a card is a picture card (Jack, Queen, or King)."""
    # Jacks: 10, 23, 36, 49
    # Queens: 11, 24, 37, 50
    # Kings: 12, 25, 38, 51
    if (card == 10 or card == 11 or card == 12 or 
        card == 23 or card == 24 or card == 25 or 
        card == 36 or card == 37 or card == 38 or 
        card == 49 or card == 50 or card == 51):
        return True
    return False


def display_deck(deck_size):
    """Display the deck as a sequence of ] characters."""
    return deck_size * ']'


def display_layout(layout):
    """Display the 4x4 layout of cards."""
    rows = []
    for i in range(4):
        row = []
        for j in range(4):
            idx = i * 4 + j
            if layout[idx] is not None:
                row.append(card_to_unicode(layout[idx]))
            else:
                row.append('')
        # no trailing empty character
        while (row[-1] == ''):
            row.pop(-1)
        rows.append('\t'+'\t'.join(row))
    return '\n'.join(rows)


def print_result(total_picture_cards_removed):
    print()
    if total_picture_cards_removed == 12:
        print("You removed all picture cards. You won! 😀")
    elif total_picture_cards_removed == 0:
        print("You removed no picture cards. You lost! 😞")
    else:
        if total_picture_cards_removed == 1:
            print("You removed only 1 picture card. You lost! 😞")
        else:
            print(f"You removed only {total_picture_cards_removed} picture cards. You lost! 😞")


def play_game(initial_seed, verbose=False):
    """
    Play a game and return the number of picture cards removed.
    
    Args:
        initial_seed: seed value for the first shuffle
        verbose: if True, print game output; if False, play silently
    
    Returns:
        Number of picture cards removed (0-12)
    """
    # Initialize deck
    deck = list(range(52))
    seed_value = initial_seed
    total_picture_cards_removed = 0
    round_number = 0
    
    # Game start. Print initial output if verbose.
    if verbose:
        print()
        print("Deck shuffled. Ready to start!")
        print(display_deck(52))
    
    # Play up to 4 rounds
    while round_number < 4 and total_picture_cards_removed < 12:
        round_number += 1
        
        # Shuffle before each round
        deck = sorted(deck)
        seed(seed_value)
        shuffle(deck)
        seed_value += 1
        
        # Round announcement if verbose
        if verbose:
            print()
            if round_number == 1:
                print("Starting the first round...")
            else:
                round_names = {2: "second", 3: "third", 4: "fourth"}
                print(f"After shuffling, starting the {round_names[round_number]} round...")
        
        # Initialize layout for the round
        layout = [None] * 16      
        # Draw initial 16 cards
        cards_to_draw = 16
        # Fill layout positions 0-15 in order
        for i in range(cards_to_draw):
            layout[i] = deck.pop(-1)

        if verbose:
            print()
            print(f"Drawing {cards_to_draw} cards:")
            print(display_deck(len(deck)))
            print(display_layout(layout))
        
        # Play the round - remove picture cards and fill vacant positions
        while True:
            # Find and remove picture cards
            picture_card_positions = [i for i in range(16) 
                                     if is_picture_card(layout[i])]
            
            if not picture_card_positions:
                # No picture cards, round ends
                break
            
            # Remove picture cards
            num_removed = len(picture_card_positions)
            total_picture_cards_removed += num_removed
            for pos in picture_card_positions:
                layout[pos] = None
                        
            # Print removal message if verbose
            if verbose:
                print()
                if num_removed == 1:
                    print("Removing 1 picture card:")
                else:
                    print(f"Removing {num_removed} picture cards:")
                print(display_layout(layout))
            
            # If we removed all 12 picture cards, we won
            if total_picture_cards_removed >= 12:
                break
            
            # Fill vacant positions with new cards from deck
            vacant_positions = [i for i in range(16) if layout[i] is None]
            cards_to_draw = len(vacant_positions)
            # Fill vacant positions in order (left to right, top to bottom)
            for i in range(cards_to_draw):
                pos = vacant_positions[i]
                layout[pos] = deck.pop(-1)
            
            # Print drawing message if verbose
            if verbose:
                print()
                if cards_to_draw == 1:
                    print("Drawing 1 card:")
                else:
                    print(f"Drawing {cards_to_draw} cards:")
                print(display_deck(len(deck)))
                print(display_layout(layout))
        
        # After round ends, combine with undealt cards to form new deck
        deck = layout + deck
    
    # Game end. Print game end message if verbose.
    if verbose:
        print_result(total_picture_cards_removed)
    
    return total_picture_cards_removed


def simulate(n, i):
    """
    Simulate n independent games and estimate probabilities.
    
    Args:
        n: number of games to simulate (strictly positive integer)
        i: initial seed (integer)
    
    For the g-th game (g=0,1,...,n-1), uses seed(i+g) before shuffling.
    """
    # Count picture cards removed for each game
    results = defaultdict(int) # New keys will automatically have a default value of 0.
    
    # Simulate n games
    for g in range(n):
        game_seed = i + g
        picture_cards_removed = play_game(game_seed, verbose=False)
        results[picture_cards_removed] += 1
    
    # Calculate relative frequencies and display table
    print("Number of picture cards removed | Relative frequency")
    print("----------------------------------------------------")
    
    # Sort by number of picture cards removed (decreasing order)
    sorted_results = sorted(results.items(), reverse=True)
    
    for num_removed, count in sorted_results:
        frequency = (count / n) * 100
        # Format: right-aligned number (31 chars), then " | " (3 chars), 
        # then right-aligned percentage (17 chars for number + 1 for % = 18 total)
        # Total line length: 31 + 3 + 18 = 52 characters
        # See https://www.geeksforgeeks.org/python/string-alignment-in-python-f-string/ for more details.
        print(f"{num_removed:>31} | {frequency:>17.2f}%")


# The main function that plays the game.
def main():
    # Get seed from user
    # print("Enter an integer to pass to the seed() function: ", end='')
    initial_seed = int(input())
    
    # Play the game with verbose output
    play_game(initial_seed, verbose=True)


if __name__ == '__main__':
    main()
