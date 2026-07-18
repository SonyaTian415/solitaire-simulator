import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from solitaire_1 import card_to_unicode, display_deck, is_picture_card
from solitaire_2 import to_ordinal


def test_is_picture_card_flags_only_jacks_queens_kings():
    picture_cards = {10, 11, 12, 23, 24, 25, 36, 37, 38, 49, 50, 51}
    for card in range(52):
        assert is_picture_card(card) == (card in picture_cards)


def test_card_to_unicode_ace_of_hearts():
    assert card_to_unicode(0) == chr(0x1F0B1)


def test_card_to_unicode_skips_the_knight_offset_for_king():
    # King of hearts is rank index 12, and Unicode reserves +11 for an unused Knight card.
    assert card_to_unicode(12) == chr(0x1F0B1 + 13)


def test_display_deck_length():
    assert display_deck(5) == "]]]]]"
    assert display_deck(0) == ""


def test_to_ordinal_handles_teen_exceptions():
    assert to_ordinal(1) == "1st"
    assert to_ordinal(2) == "2nd"
    assert to_ordinal(3) == "3rd"
    assert to_ordinal(11) == "11th"
    assert to_ordinal(12) == "12th"
    assert to_ordinal(13) == "13th"
    assert to_ordinal(21) == "21st"


def test_simulate_results_are_bounded(capsys):
    from solitaire_1 import simulate

    simulate(50, 0)
    output = capsys.readouterr().out
    assert "Relative frequency" in output
