from deck import Deck

class _AbstractColumn:
    """Abstract base class that contains a generic interface for columns"""
    def __init__(self):
        self.row = []

    def put(self, card):
        """Method adds a card to the column if possible and returns success"""
        if self.can_put(card):
            self._put(card)
            return True
        else:
            return False

    def can_put(self, card):
        """Abstract method that checks whether a card can be placed on a column"""
        raise NotImplementedError()

    def _put(self, card):
        """Protected method that adds a card to a column"""
        self.row.append(card)

    def __len__(self):
        return len(self.row)

    def top(self):
        """Method that returns the top card in the row."""
        if not self.row:
            return None
        return  self.row[-1]

    def away(self):
        """Undefined method that removes the top card from the row"""
        pass

    def __str__(self):
        raise NotImplementedError()

class _PlayColumn(_AbstractColumn):
    """Class of game columns that creates
    a column of 7 cards by removing them from the deck"""
    def __init__(self, playdeck):
        super().__init__()
        for _ in range(7):
            self._put(playdeck.top())
            playdeck.away()

    def can_put(self, card):
        return not self or self.top() > card

    def away(self):
        self.row.pop()

    def __str__(self):
        return f"[{' '.join(str(c) for c in self.row)}]"

class _ReserveColumn(_AbstractColumn):
    """Reserve column based on an abstract class"""
    def can_put(self, card):
        return not self

    def away(self):
        self.row.pop()

    def __str__(self):
        if not self.row:
            return f'[ ]'
        return f"[{str(self.top())}]"

class _BaseColumn(_AbstractColumn):
    """Base column based on an abstract class"""
    def can_put(self, card):
        return not self or \
            ((self and self.top().value + 1 == card.value) and (self.top().suit == card.suit))

    def full(self):
        """Checks if base stacks are full"""
        return len(self) == len(Deck.RANKS)

    def __str__(self):
        if not self.row:
            return f'[ ]'
        return f"[{str(self.top())}]"

class _PlayDeck:
    "Storing the deck and the last card drawn from it"
    def __init__(self, deck):
        self.deck = deck
        self.card = None
        self.away()

    def top(self):
        return self.card

    def __len__(self):
        return len(self.deck) + (self.card is not None)

    def away(self):
        "If the deck is not empty, calls a function to draw a card"
        if self.deck:
            self._away()
        else:
            self.card = None

    def _away(self):
        "Draws a card from the deck and sets it as a card "
        self.card = self.deck.deal()

    def put(self, card):
        "Does not include the possibility of adding cards to the deck"
        return False

    def __str__(self):
        if not self.card:
            return f'[-]'
        return f'{str(self.card)}'


class Row(tuple):
    """A tuple of fixed size.
     The constructor receives the number of elements and an iterable."""
    def __new__(cls, n, it):
        it = iter(it)
        obj = super().__new__(cls, (next(it) for _ in range(n)))
        return obj


class Game:
    """Сlass is responsible for the logic of the game"""
    N_BASE = 4
    N_PLAY = 7
    N_RESERVE=7

    def __init__(self):
        self._deck =None
        self._playdeck = None  # колода на столі
        self._reserve = None  # резервні стопки
        self._play = None  # гральні вертикальні ряди
        self._base = None  # базовий ряд
        self._start_card = None #стартова карта базового ряду
        self._if_play = False# чи триває гра
        self.new_game() #нова гра

    def new_game(self):
        """Method to create a new game,
        a new deck, shuffles it, creates a base, reserve and playing columns"""
        self._deck = Deck()
        self._deck.shuffle()
        self._playdeck = _PlayDeck(self._deck)
        self._base = Row(self.N_BASE, iter(lambda: _BaseColumn(), None))
        self._reserve = Row(self.N_RESERVE, iter(lambda: _ReserveColumn(), None))
        self._play = Row(self.N_PLAY, iter(lambda: _PlayColumn(self._playdeck), None))
        self._start_card = None
        self._if_play = True

    def win(self):
        """Method of verifying the victory of the game"""
        res = all(stack.full() for stack in self._base.row)
        self._if_play = not res
        return res

    @staticmethod
    def move(stack_from, stack_to):
        """Static method for moving a card from one stack to another"""
        card = stack_from.top()
        if card is None:
            return False
        res = stack_to.put(card)
        if not res:
            return False
        stack_from.away()
        return True

    def _base_check(self, stack_from, stack_to):
        """Sets the starting card.
        And if the pile is empty, it checks whether the value matches the starting card"""
        card= stack_from.top()
        if card and not stack_to.top():
            if all(not stack for stack in self._base):
                self._start_card = card.value
            return self._start_card == card.value
        return True

    def play_play(self, i_from, i_to):
        """Functions of this type make checks, call another function that rearranges the cards
        and returns whether the action was successfully performed"""
        if (0 <= i_from < len(self._play))and (0 <= i_to < len(self._play)):
            if i_from != i_to:
                return self.move(self._play[i_from], self._play[i_to])
            return True
        return False


    def play_base(self, i_from, i_to):
        if (0 <= i_from < len(self._play)) and (0 <= i_to < len( self._base)):
            if self._base_check(self._play[i_from], self._base[i_to]):
                return self.move(self._play[i_from], self._base[i_to])
        return False

    def play_reserve(self, i_from, i_to):
        if (0 <= i_from < len(self._play)) and (0 <= i_to < len(self._reserve)):
            return self.move(self._play[i_from], self._reserve[i_to])
        return False

    def reserve_base(self, i_from, i_to):
        if (0 <= i_from < len(self._reserve)) and (0 <= i_to < len( self._base)):
            if self._base_check(self._reserve[i_from], self._base[i_to]):
                return self.move(self._reserve[i_from], self._base[i_to])
        return False

    def reserve_play(self, i_from, i_to):
        if (0 <= i_from < len(self._reserve)) and (0 <= i_to < len(self._play)):
            return self.move(self._reserve[i_from], self._play[i_to])
        return False

    def deck_play(self, i_to):
        if (0 <= i_to < len(self._play)):
            if not self._play[i_to]:
                return self.move(self._playdeck, self._play[i_to])
        return False

    def deck_base(self, i_to):
        if (0 <= i_to < len(self._base)):
            if self._base_check(self._playdeck, self._base[i_to]):
                return self.move(self._playdeck, self._base[i_to])
        return False

    def __str__(self):
        s = '==============\n'
        s += f"Deck on table:  {self._playdeck}\n"
        s += f"\nPlay columns:\n"
        for i, playcol in enumerate(self._play):
            s += f"{i + 1}. {playcol}\n"
        s += f"\nBase columns:\n"
        for i, basecol in enumerate(self._base):
            s += f"{i + 1}. {basecol}\n"
        s += f"\nReserve columns:\n"
        for i, rescol in enumerate(self._reserve):
            s += f"{i + 1}. {rescol}\n"
        s += "=============="
        return s
