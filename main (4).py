"""
Lab4, Khilko Victoria, K-13, Variant 129
This program  is a console solitaire game.
"""
from collections import namedtuple
from game import Game



def move(move_fn):
    """
    Requests user input to move a card from one column to another.
    Checks for processing capability.
    Takes a move function as the 'move_fn' argument, which must be one of the move functions
    """
    i_from = input('Enter the number of the column from which you want to take a card:').strip()
    i_to = input('Enter the number of the column on which you want to place a card: ').strip()
    if i_from.isdigit() and i_to.isdigit():
        i_from = int(i_from) - 1
        i_to = int(i_to) - 1
        res = move_fn(i_from, i_to)
        if not res:
            print("Failed to move card.\n")
    else:
        print("Please enter an integer.")


def move_deck(move_fn):
    """
    Similar to 'move' but asks for user input to move a card from the deck to a column.
    """
    i_to = input('Enter the number of the column on which you want to place a card:').strip()
    if i_to.isdigit():
        i_to = int(i_to) - 1
        res = move_fn(i_to)
        if not res:
            print("Failed to move card.\n")
    else:
        print("Please enter an integer.")


def do_deck_play(game):
    """
    Functions of this type call 'move_deck'
    with a specified function as an argument.
    """
    move_deck(game.deck_play)

def do_deck_base(game):
    move_deck(game.deck_base)

def do_reserve_play(game):
    move(game.reserve_play)

def do_play_play(game):
    move(game.play_play)


def do_play_base(game):
    move(game.play_base)


def do_play_reserve(game):
    move(game.play_reserve)


def do_reserve_base(game):
    move(game.reserve_base)


def new(game):
    """
    Calls the new_game method on the game object to start a new game
    """
    game.new_game()

def show_rules(game):
    print("Rules of Solitaire.\n\
 The deck is thoroughly shuffled and 49 cards are dealt into 7\n\
 vertical play columns with 7 cards in each column.Above the dealt\n\
 cards, there are spaces for 7 reserve columns. On the right side,\n\
 there are spaces for 4 base columns where the starting cards\n\
 are the cards of the same value as the first card placed in any\n\
 base column. The remaining 3 cards are placed in the stock\n\
 pile. The goal is to collect all the cards on the base columns\n\
 in ascending sequential order in suit. Moving the top cards of play\n\
 columns from one play column to another is allowed in descending\n\
 sequential order in suit. Any cards from the play columns can be\n\
 moved to the reserve columns,and from the reserve columns to the\n\
 base columns. Each reserve column should contain no more than\n\
 one card. If any of the play columns are freed from cards,any card\n\
 from the stock pile can be placed in the empty space.\n\n\
 Solitaire is won when all cards are collected on the base\n\
 columns in ascending sequential order in suit.")


def set_menu():
    """
    Defines a menu for the game using a named tuple for each menu item.
    Returns a dictionary with the menu items as values and the keys as the menu options.
    """

    MenuItem = namedtuple('MenuItem', ['key', 'descr', 'action'])
    menu = {}
    item = MenuItem('new', 'Start a new game', new)
    menu[item.key] = item
    item = MenuItem('rules', 'View game rules', show_rules)
    menu[item.key] = item
    item = MenuItem('1', 'Move card from play column to play column', do_play_play)
    menu[item.key] = item
    item = MenuItem('2', 'Move card from play column to base column', do_play_base)
    menu[item.key] = item
    item = MenuItem('3', 'Move card from play column to reserve column', do_play_reserve)
    menu[item.key] = item
    item = MenuItem('4', 'Move card from reserve column to base column', do_reserve_base)
    menu[item.key] = item
    item = MenuItem('5', 'Move card from reserve column to game column', do_reserve_play)
    menu[item.key] = item
    item = MenuItem('6', 'Move card from deck to play column', do_deck_play)
    menu[item.key] = item
    item = MenuItem('7', 'Move card from deck to base column', do_deck_base)
    menu[item.key] = item
    item = MenuItem('stop', 'Stop the game', None)
    menu[item.key] = item
    return  menu

def print_menu(menu):
    for el in menu.values():
        print(f'{el.key:6}', el.descr)


def describe_game(game):
    print(game)


def ask_action(menu):
    """
    Displays a menu and asks the user for a command. If there is no command in the menu, then action = None
    """
    print_menu(menu)
    action = input('Enter one of the commands: ').strip()
    if action not in menu:
        action = None
    return action

def do_action(action, game, menu):
    """
    If action = None throws an error and returns True.
    If the command is in the menu, it executes and returns True, otherwise False
    """
    if action is None:
        print('You entered the wrong command, please try again')
        return True
    else:
        if menu[action].action:
            menu[action].action(game)
            return True
        else:
            return False

def one_step(game, menu):
    """
    Brings up the game. Asks the user to enter a command and using the ask_action function
    stores the result in the action variable. Executes a command using the do_action function
    and returns the execution result.
    """
    describe_game(game)
    action = ask_action(menu)
    return do_action(action, game, menu)


def main():
    """
    Сreates menu and game objects, then executes a one-step loop that runs until True is returned.
    If the cycle received False, the game ends
    Displays information about the author and the program.
    """
    menu = set_menu()
    game = Game()
    print(__doc__)
    while one_step(game, menu):
        pass
    describe_game(game)
    print('Game over. ')


try:
    main()
except KeyboardInterrupt:
    print('\nProgram aborted')
except BaseException as e:
    print('***** error')
    print('Smth went wrong, unable to recover.', e, sep='\n')
