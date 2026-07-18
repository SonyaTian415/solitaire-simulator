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


def to_ordinal(n):
    # Handle the "teen" exceptions (11, 12, 13)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix_map = {1: "st", 2: "nd", 3: "rd"}
        suffix = suffix_map.get(n % 10, "th") 
    return f"{n}{suffix}"


def display_deck(deck):
    return len(deck) * ']'


def display_face_up(face_up):
    if not face_up:
        return ""        
    return "[" * (len(face_up)-1) + card_to_unicode(face_up[-1])


def display_stack(stack):
    if not stack:
        return ""
    return "[" * (len(stack) - 1) + card_to_unicode(stack[-1])


def display_stacks(stacks):
    # Preallocate a list of spaces (long enough to hold all suits)
    # 62 = 4 + 15 + 15 + 15 + 13
    line = list(" " * 62)
    
    for i in range(4): # 0:Hearts, 1:Diamonds, 2:Clubs, 3:Spades
        if not stacks[i]:
            continue
        # Rule: Position starts at 4, then every 15 chars
        start_pos = 4 + (i * 15)    
        # Create the stack string: [[...[ + Unicode Card
        current_stack = display_stack(stacks[i])
        # "Paint" each character into our preallocated line
        for j, char in enumerate(current_stack):
            line[start_pos + j] = char
                
    # Convert list back to string and remove trailing spaces
    return "".join(line).rstrip()


# main play game function
def play_game(initial_seed):
    # Initial shuffle, we only need once.
    deck = list(range(52))
    seed(initial_seed)
    shuffle(deck)
    
    logs = ["Deck shuffled. Ready to start!", display_deck(deck), ""]

    inc_stacks = [[] for _ in range(4)]
    dec_stacks = [[] for _ in range(4)]
    face_up = []
    round_no = 1
    
    while True:
        logs.append(f"Starting the {to_ordinal(round_no)} round...")
        logs.append("")
        
        cards_placed_this_round = 0
        while deck or face_up:
            # 1. Try to place the topmost face-up card
            if face_up:
                card = face_up[-1]
                suit, rank = card // 13, card % 13
                placed = False
                message = ""
                
                # Priorities: Start new > Extend Inc > Extend Dec
                if rank == 0:
                    inc_stacks[suit].append(face_up.pop())
                    placed = True
                    message = "Starting a stack."
                elif rank == 12:
                    dec_stacks[suit].append(face_up.pop())
                    placed = True
                    message = "Starting a stack."
                elif inc_stacks[suit] and rank == (inc_stacks[suit][-1] % 13) + 1:
                    inc_stacks[suit].append(face_up.pop())
                    placed = True
                    message = "Extending an increasing stack."
                elif dec_stacks[suit] and rank == (dec_stacks[suit][-1] % 13) - 1:
                    dec_stacks[suit].append(face_up.pop())
                    placed = True
                    message = "Extending a decreasing stack."
                
                if placed:
                    cards_placed_this_round += 1
                    logs.append(message)
                    logs.append(display_deck(deck))
                    logs.append(display_face_up(face_up))
                    logs.append(display_stacks(inc_stacks))
                    logs.append(display_stacks(dec_stacks))
                    logs.append("")
                    continue # Re-check new top card
            
            # 2. Draw 3 cards if no placement possible
            if deck:
                for _ in range(min(3, len(deck))):
                    face_up.append(deck[-1])
                    deck.pop()
                logs.append(display_deck(deck))
                logs.append(display_face_up(face_up))
                logs.append(display_stacks(inc_stacks))
                logs.append(display_stacks(dec_stacks))
                logs.append("")
            else: 
                break

        # check for win or loss
        total_placed = 0
        for s in inc_stacks:
            total_placed += len(s)
        for s in dec_stacks:
            total_placed += len(s)

        if total_placed == 52:
            return 0, logs
        if cards_placed_this_round == False:
            cards_left = 52 - total_placed
            return cards_left, logs

        # prepare for next round
        round_no += 1
        deck = face_up
        deck.reverse()
        face_up = []


# post-game logs interaction are here
def main():
    print("Enter an integer to pass to the seed() function: ", end='')
    initial_seed = int(input())    
    unplaced, logs = play_game(initial_seed)
    
    # trim the last empty line since we print extra line in above logs creation
    if logs[-1] == "":
        logs.pop()

    # print final result
    print()
    if unplaced == 0: 
        print("You placed all cards. You won!")
    else: 
        print(f"You could not place {unplaced} cards. You lost!")
    
    # print post-game interactions
    total = len(logs)
    print(f"\nThere are {total} lines of output. What do you want me to do?")
    
    while True:
        print("Enter: q to quit")
        print(f"       a last line number (between 1 and {total})")
        print(f"       a first line number (between 1 and -{total})")
        print(f"       a range of line numbers (of the form m--n with 1 < m <= n <= {total})")
        
        cmd = input("       ") # 7 spaces for alignment
        if cmd.strip() == 'q': 
            break
        
        print()
        lines_to_print = []
        # parse input
        try:
            if "--" in cmd:
                parts = cmd.split("--")
                # isdigit() is True only for pure digits (no '+' or internal spaces)
                if len(parts) == 2 and parts[0].strip().isdigit() and parts[1].strip().isdigit():
                    m, n = int(parts[0]), int(parts[1])
                    if 1 <= m <= n <= total:
                        lines_to_print = logs[m-1:n]
            elif cmd.strip().startswith("-"):
                # Negative case: -k
                 # Rule: No space allowed between '-' and digits
                if cmd.strip()[1:].isdigit():
                    k = int(cmd)
                    if -total <= k <= -1:
                        lines_to_print = logs[total + k:]
            elif cmd.strip().isdigit():
                # Positive case: k
                k = int(cmd)
                if 1 <= k <= total:
                    lines_to_print = logs[:k]
            # eligible lines to print
            for line in lines_to_print: 
                print(line)
            print()
        except: 
            pass # gnore incorrect input


def simulate(n, i):
    """
    Simulate n independent games (second solitaire) and estimate probabilities
    that a game ends with k cards left unplaced.
    """
    results = defaultdict(int)
    for g in range(n):
        game_seed = i + g
        unplaced, _ = play_game(i + g)
        results[unplaced] += 1

    # Calculate relative frequencies and display table
    print("Number of cards left | Relative frequency")
    print("-----------------------------------------")

    sorted_results = sorted(results.items(), reverse=True)
    for unplaced_cards, count in sorted_results:
        frequency = (count / n) * 100
        # 20 + 3 + 18 = 41 chars
        print(f"{unplaced_cards:>20} | {frequency:>17.2f}%")


if __name__ == "__main__":
    main()
