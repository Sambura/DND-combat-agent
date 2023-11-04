from .utils import to_tuple, get_random_coords
from .game_board import DnDBoard
from .units import Unit

def print_game(game: DnDBoard, unit_to_color: dict[Unit, str]) -> None:
    COLORS = {
        "Red": "\033[91m",
        "Green": "\033[92m",
        "Blue": "\033[94m",
        "Purple": "\033[95m",
        "Orange": "\033[93m",
        "Cyan": "\033[96m",
        "Magenta": "\033[95m",
        "Reset": "\033[0m",
    }

    num_rows, num_cols = game.board.shape
    number_padding = 2

    print(f'Units alive: {len(game.units)}')
    print(f'Players: {len(game.players_to_units)}:')
    for player_id in game.players_to_units:
        units = game.players_to_units[player_id]
        print(f'\tPlayer #{player_id} ({len(units)} units): ', end='')
        for unit in units:
            color = unit_to_color[unit]
            print(f'`{COLORS[color]}{unit.name} ({unit.health} HP){COLORS["Reset"]}`', end=', ')
        print("\b\b  ")
    print(f'\t')

    print(" " * (number_padding + 1), end="")  # Offset for y-axis numbering
    for j in range(num_cols):
        print(f"{j:>{number_padding}}", end="")

    print()

    # Print the matrix with numbering on both axes, "empty," and compact grid
    for i in range(num_rows):
        # Print y-axis numbering on the left without colons
        print(f"{i:>{number_padding}} ", end="")

        for j in range(num_cols):
            unit = game.board[i, j]
            if unit is None:
                formatted_value = "  "  # Represents "empty" with two space characters
            else:
                color = unit_to_color[unit]
                formatted_value = f"{COLORS[color]}██{COLORS['Reset']}"  # Colorize # characters
            print(formatted_value, end="")

        print(f"{i:>{number_padding}} ")

    # Print x-axis numbering at the bottom
    print(" " * (number_padding + 1), end="")  # Offset for y-axis numbering
    for j in range(num_cols):
        print(f"{j:>{number_padding}}", end="")

    print('\n')

    unit, player_id = game.get_current_unit()
    color = unit_to_color[unit]
    print(f'Next move is by player #{player_id}: `{COLORS[color]}{unit.name}{COLORS["Reset"]}`')

def take_turn(game, new_coords, action, unit_to_color, agent=False, prnt_game=True, print_move=True):
    COLORS = {
        "Red": "\033[91m",
        "Green": "\033[92m",
        "Blue": "\033[94m",
        "Purple": "\033[95m",
        "Orange": "\033[93m",
        "Cyan": "\033[96m",
        "Magenta": "\033[95m",
        "Reset": "\033[0m",
    }

    unit, player_id = game.get_current_unit()
    color = unit_to_color[unit]
    if print_move: print(f'Turn made by player #{player_id}: `{COLORS[color]}{unit.name}{COLORS["Reset"]}`:')
    old_coords = to_tuple(game.get_unit_position(unit))
    new_coords = to_tuple(new_coords)
    if print_move: print(f'\tUnit {"moves" if old_coords != new_coords else "does not move"}: {old_coords} -> {new_coords};')
    if print_move:
        if action is None:
            print('\tAnd does not take any action!')
        else:
            print(f'\tAnd takes aciton `{action.action.name}` with attributes: {({key: str(value) for key, value in action.kwargs.items()})}')

    reward, game_over = game.take_turn(new_coords, action, skip_illegal=agent)

    if prnt_game: 
        print()
        print_game(game, unit_to_color)

    return reward, game_over

def place_unit_randomly(game: DnDBoard, unit: Unit, player_id: int):
    while True:
        coords = get_random_coords(*game.board_shape)
        if game.is_occupied(coords): continue

        game.place_unit(unit, coords, player_id)
        return