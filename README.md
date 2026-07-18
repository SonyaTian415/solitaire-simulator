# Solitaire Simulator

Two single-player card game variants implemented in Python, each with a Monte Carlo
simulator that estimates win/loss probabilities across thousands of randomized games.

## Motivation

I wanted a small project to practice designing game logic around state machines and
using randomized simulation to answer a question that's hard to reason about
analytically: "what's the actual probability of winning this game?" Rather than just
writing the game, I added a `simulate()` mode to each variant so the answer comes from
running thousands of trials rather than guesswork.

## What's inside

- **`src/solitaire_1.py`** — *Picture Card Solitaire*. Deals a 4x4 layout from a shuffled
  52-card deck, repeatedly removes picture cards (J/Q/K) and refills the empty slots,
  across up to 4 reshuffled rounds. You win if all 12 picture cards are removed.
- **`src/solitaire_2.py`** — a second variant where cards build ascending/descending
  stacks by suit. Draws 3 cards at a time from the deck when no card can be placed, and
  includes an interactive post-game log viewer for replaying any range of the game's
  output line by line.

Both expose a `simulate(n, i)` function that runs `n` independent games — seeded
`i, i+1, ..., i+n-1` — and prints a relative-frequency table of outcomes.

## Running it

```bash
cd src
python3 solitaire_1.py     # play one interactive game (prompts for a seed)
python3 solitaire_2.py     # play the second variant
python3 -c "from solitaire_1 import simulate; simulate(5000, 0)"   # simulate 5,000 games
```

## Example output

A simulation of the second game over 5,000 seeded games — see
[`examples/sample_simulation_output.txt`](examples/sample_simulation_output.txt) for
the full relative-frequency table. Roughly 26% of games clear the board completely.

## Notes

Cards render as Unicode playing-card glyphs (🂡, 🂪, ...) rather than plain text — the
`card_to_unicode` helper maps the internal 0-51 card encoding to the correct code point,
accounting for the fact that Unicode inserts an unused "Knight" card between 10 and Queen.

## What I'd improve next

- Swap the `input()`-based CLI for `argparse`
- Add more unit tests around the deck-refill and stack-extension logic

## Tech

Pure Python 3 standard library (`random`, `itertools`, `collections`) — no external
dependencies.

## Author

Sonya Tian
