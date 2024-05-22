import random

class Card:
    """This is a class representing a card that is hashed in the deck."""
    def __init__(self, suit: str, rank: str):
        self._suit = None
        self._rank = None
        self._init_check(suit, rank)

    def _init_check(self, suit, rank):
        """Checks that suit and rank are valid values."""
        if (suit not in Deck.SUITS) or (rank not in Deck.RANKS):
            raise ValueError('No such card')
        self._suit = suit
        self._rank = rank

    def __str__(self):
        return f"{self.rank}-{self.suit}"

    def __repr__(self):
       return f"{self.__class__.__name__}('{self.suit}', '{self.rank}')"

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    @property
    def value(self):
        return Deck.VALUES[self.rank]

    def __hash__(self):
        return hash((self._suit, self._rank))

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        return self.suit == other.suit and self.value < other.value


class Deck:
    """Deck class that can be iterated over"""
    SUITS = ('C', 'S', 'H', 'D')
    RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
    VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12,
              'K': 13}

    def __init__(self):
        self._cards = [Card(suit, rank) for suit in self.SUITS for rank in self.RANKS]

    def shuffle(self):
        """Method that shuffles the cards in the deck"""
        random.shuffle(self._cards)

    def deal(self):
        """Method that removes cards from the deck"""
        if not self._cards:
            return None
        return self._cards.pop()

    def __len__(self):
        return len(self._cards)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self) == 0:
            raise StopIteration
        else:
            return self.deal()