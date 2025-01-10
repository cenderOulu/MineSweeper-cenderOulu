"""import module here

for this project I used modified sweeperlib.py """

import random
import datetime
import sweeperlib


state = {
    "row": 0,
    "col": 0,
    "bombs": 0,
    "field": [],
    "game_over": False,
    "bombs_counts": 0,
    "opened": 0,
    "won": False,
    "setting": False,
    "time": 0,
    "playing": False,
    "registered": False,
    "leaderboard": False,
    "clicks": 0,
}


def file_check():
    """check if leaderboard.csv exists"""
    try:
        with open("leaderboard.csv", "r", encoding="utf-8") as f:
            if f != 0:
                pass
            return True
    except FileNotFoundError:
        print("History not found, finish a game to create one")
        return False


def won(states):
    """
    Records the game outcome (win or lose), time spent, and bombs left to the leaderboard CSV file.

    Args:
        states (dict): A dictionary containing the game's current state, including player progress,
                       timer, and win/loss status.
    """
    if not states["registered"]:
        time_in_minutes = states["time"] // 60
        outcome = "Won" if states["won"] else "Lost"
        bombs_left = 0
        if not states["won"]:
            bombs_left = states["bombs_counts"]
        timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_string = (
            f"{timenow};{outcome};{time_in_minutes} minutes, "
            f"{int(state['time']) - time_in_minutes * 60} seconds;"
            f"{bombs_left};"
            f"{state['clicks']}\n"
        )
        with open("leaderboard.csv", "a", encoding="utf-8") as f:
            f.write(formatted_string)
        state["registered"] = True


def leaderboard():
    """
    Renders the leaderboard on the screen, displaying previous game results.
    """

    cols, rows = 15, 10
    sweeperlib.resize_window(600, 450)
    sweeperlib.draw_background()
    board = []
    with open("leaderboard.csv", "r", encoding="utf-8") as f:
        for line in f:
            row = line.strip().split(";")
            if len(row) == 5:
                datetime_str, outcome, time_in_minutes, bombs_left, clicks = row
                board.append(
                    (datetime_str, outcome, time_in_minutes, bombs_left, clicks)
                )
    sweeperlib.draw_text(
        "------History------",
        (int(cols * 40) / 2) - 200,
        rows * 40 + 10,
        (0, 0, 0, 255),
        "arial",
    )
    sweeperlib.draw_text("L to exit", 0, rows * 40 + 20, (0, 0, 0, 255), "arial", 10)
    i = 0
    while i < len(board) and i < 27:
        datetime_str, outcome, time_in_minutes, bombs_left, clicks = board[i]
        display_text = (
            f"Date: {datetime_str}, Outcome: {outcome}, "
            f"Time: {time_in_minutes}, Bombs Left: {bombs_left}, "
            f"Clicks: {clicks}"
        )
        sweeperlib.draw_text(
            display_text,
            (int(cols * 40) / 2) - 300,
            rows * 40 - (15 * i),
            (0, 0, 0, 255),
            "arial",
            9,
        )
        i += 1


def change_field(states):
    """
    Allows the user to adjust game dimensions and bomb count.

    Args:
        states (dict): A dictionary containing the game's current state.
    """
    e = 0
    while e < 2 or e > 24:
        try:
            e = int(input("Please input how many rows you want:"))
            if e < 2 or e > 24:
                print("number of rows cannot be smaller than 2 or bigger than 24")
        except ValueError:
            print("invalid input")
            e = 0
        except KeyboardInterrupt:
            return
    states["row"] = e
    e = 0
    while e < 2 or e > 48:
        try:
            e = int(input("Please input how many columns you want:"))
            if e < 2 or e > 48:
                print("number of columns cannot be smaller than 2 or bigger than 48")
        except ValueError:
            print("invalid input")
            e = 0
        except KeyboardInterrupt:
            return
    states["col"] = e

    e = 0
    while e < 1 or e > state["row"] * state["col"]:
        try:
            e = int(input("Please input how many bombs you want:"))
            if e < 1 or e > state["row"] * state["col"]:
                print(
                    "number of bombs cannot be smaller than 1 or bigger than the size of the field"
                )
        except ValueError:
            print("invalid input")
            e = 0
        except KeyboardInterrupt:
            return
    states["bombs"] = e
    reset_button(states)


def setting_window():
    """
    Draws the settings menu with options and instructions for the player.
    """
    col, row = 15, 10
    sweeperlib.resize_window(600, 450)
    sweeperlib.draw_background()
    sweeperlib.draw_text(
        "Minesweeper",
        int((col * 40) / 2) - 50,
        row * 40 + 20,
        (255, 200, 100, 255),
        "arial",
        20,
    )
    sweeperlib.draw_text(
        "Game by cender (Cat Vo) for Elementary Programming of University of Oulu",
        5,
        410,
        (0, 0, 0, 255),
        "arial",
        10,
    )
    sweeperlib.draw_text("press P to play", 5, 295, (0, 0, 0, 255), "arial", 10)
    sweeperlib.draw_text(
        "press X to change size of the play field and the amount of bombs",
        5,
        280,
        (0, 0, 0, 255),
        "arial",
        10,
    )
    sweeperlib.draw_text(
        "press Esc to quit the game", 5, 265, (0, 0, 0, 255), "arial", 10
    )
    sweeperlib.draw_text(
        "press R or the smiley face symbol to play new game",
        5,
        250,
        (0, 0, 0, 255),
        "arial",
        10,
    )
    sweeperlib.draw_text(
        "press M or the gear go back to menu", 5, 235, (0, 0, 0, 255), "arial", 10
    )
    sweeperlib.draw_text("press L to show history", 5, 220, (0, 0, 0, 255), "arial", 10)


def reset_button(states):
    """
    Resets the game state, initializes the field, and places mines randomly.

    Args:
        states (dict): A dictionary containing the game's current state.
    """
    field = []
    for _ in range(states["row"]):
        field.append([])
        for col in range(states["col"]):
            cols = col
            cols += 1
            field[-1].append(" ")
    states["field"] = field
    available = []
    for x in range(states["col"]):
        for y in range(states["row"]):
            available.append((x, y))
    states["game_over"] = False
    states["won"] = False
    states["opened"] = 0
    states["bombs_counts"] = state["bombs"]
    states["time"] = 0
    states["playing"] = False
    states["registered"] = False
    states["leaderboard"] = False
    states["clicks"] = 0
    place_mines(states["field"], available, states["bombs"])


def tiles_opening(y, x, states):
    """
    Opens tiles by using stack, stops on numbered tiles, and ends the game if a bomb is opened.

    Args:
        y (int): The row index of the tile being opened.
        x (int): The column index of the tile being opened.
        states (dict): A dictionary containing the game's current state.
    """
    if states["field"][x][y][0] != " ":
        return

    stack = [(x, y)]
    while stack:
        current_x, current_y = stack.pop()

        if states["field"][current_x][current_y][0] == " ":
            states["field"][current_x][current_y] = states["field"][current_x][
                current_y
            ].replace(" ", "")
            states["opened"] += 1

        if states["field"][current_x][current_y] == "x":
            states["game_over"] = True
            states["playing"] = False
            won(state)
            return

        if states["field"][current_x][current_y] == "0":
            directions = [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ]
            rows = len(states["field"])
            cols = len(states["field"][0]) if rows > 0 else 0
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if states["field"][nx][ny][0] == " ":
                        stack.append((nx, ny))


def playing(x, y, button, states):
    """
    Handles player interactions with the game field based on mouse inputs, updating the game state.

    Args:
        x (int): The x-coordinate of the mouse click.
        y (int): The y-coordinate of the mouse click.
        button (int): The mouse button pressed (e.g., left or right click).
        states (dict): A dictionary containing the game's current state.
    """
    grid_x, grid_y = int(y / 40), int(x / 40)

    if button == 1:
        tile = states["field"][grid_x][grid_y]

        if len(tile) != 1:
            tiles_opening(grid_y, grid_x, states)
        elif tile.isdigit():
            surrounding_flags = count_flags(grid_y, grid_x, states["field"])
            if surrounding_flags == int(tile):
                directions = [
                    (-1, -1),
                    (-1, 0),
                    (-1, 1),
                    (0, -1),
                    (0, 1),
                    (1, -1),
                    (1, 0),
                    (1, 1),
                ]
                rows = len(states["field"])
                cols = len(states["field"][0]) if rows > 0 else 0
                for dx, dy in directions:
                    nx, ny = grid_x + dx, grid_y + dy
                    if (
                        0 <= nx < rows
                        and 0 <= ny < cols
                        and states["field"][nx][ny][0] == " "
                    ):
                        tiles_opening(ny, nx, states)
    elif button == 4:
        tile = states["field"][grid_x][grid_y]

        if tile[0] != "f" and len(tile) > 1:
            states["field"][grid_x][grid_y] = tile.replace(" ", "f")
            states["bombs_counts"] -= 1
        elif tile[0] == "f":
            states["field"][grid_x][grid_y] = tile.replace("f", " ")
            states["bombs_counts"] += 1

    if (
        states["opened"] == states["row"] * states["col"] - states["bombs"]
        and not states["game_over"]
    ):
        states["won"] = True
        states["playing"] = False
        won(states)


def handle_mouse(x, y, button, modifier):
    """
    Handles mouse clicks to interact with the game field or reset the game.

    Args:
        x (int): The x-coordinate of the mouse click.
        y (int): The y-coordinate of the mouse click.
        button (int): The mouse button pressed.
        modifier (int): Modifier keys held during the mouse click.
    """
    modifier += 1
    if not state["setting"] and not state["leaderboard"]:
        if 0 < x < state["col"] * 40 and 0 < y < state["row"] * 40:
            if not state["game_over"] and not state["won"]:
                state["clicks"] += 1
                state["playing"] = True
                playing(x, y, button, state)
            else:
                reset_button(state)
                state["setting"] = True
        if (
            int((state["col"] * 40) / 2) < x < int((state["col"] * 40) / 2) + 50
            and state["row"] * 40 < y < state["row"] * 40 + 50
        ):
            reset_button(state)
        if (
            state["col"] * 40 - 50 < x < state["col"] * 40
            and state["row"] * 40 < y < state["row"] * 40 + 50
        ):
            if state["won"] or state["game_over"]:
                reset_button(state)
            state["setting"] = True


def handle_keyboard_access_menu(sym, handler):
    """
    Handles keyboard inputs to control the game state and access menus.

    Args:
        sym (int): The key symbol of the pressed key.
        handler (function): A callback function to handle the input action.
    """
    handler += 1
    if sym == 112:
        state["setting"] = False
    elif sym == 120:
        change_field(state)
    elif sym == 65307:
        sweeperlib.close()
    elif sym == 109:
        state["setting"] = True
    elif sym == 114:
        reset_button(state)
    elif sym == 108:
        if state["leaderboard"]:
            state["leaderboard"] = False
        else:
            if file_check():
                state["leaderboard"] = True


def time_handler(elapsed):
    """
    Updates the game timer if the game is active and not over.

    Args:
        elapsed (float): The time elapsed since the last timer update.
    """
    if not state["game_over"] and not state["won"] and state["playing"]:
        state["time"] += elapsed


def place_mines(field, av, amount):
    """
    Places the specified number of mines randomly on the game field.

    Args:
        field (list): A 2D list representing the game field.
        av (list): A list of available positions for placing mines.
        amount (int): The number of mines to place.
    """
    mines = random.sample(av, amount)
    for x, y in mines:
        field[y][x] = " x"
    for i in enumerate(field):
        for j in enumerate(field[i[0]]):
            if field[i[0]][j[0]] != " x":
                count_bombs(j[0], i[0], field)


def count_bombs(y, x, room):
    """
    Counts the number of bombs surrounding a given tile and updates the tile with the count.

    Args:
        y (int): The row index of the tile.
        x (int): The column index of the tile.
        room (list): A 2D list representing the game field.
    """
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    ninja_count = 0
    rows = len(room)
    cols = len(room[0]) if rows > 0 else 0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and room[nx][ny] == " x":
            ninja_count += 1
    room[x][y] = " " + str(ninja_count)


def count_flags(y, x, room):
    """
    Counts the number of flagged tiles surrounding a given tile.

    Args:
        y (int): The row index of the tile.
        x (int): The column index of the tile.
        room (list): A 2D list representing the game field.
    """
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    ninja_count = 0
    rows = len(room)
    cols = len(room[0]) if rows > 0 else 0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and room[nx][ny][0] == "f":
            ninja_count += 1
    return ninja_count


def draw_field():
    """
    Renders the game field, UI elements, and game outcome messages.
    """

    try:
        sweeperlib.clear_window()
        sweeperlib.draw_background()
        for i in range(len(state["field"])):
            for j in range(len(state["field"][i])):
                sweeperlib.prepare_sprite(state["field"][i][j][0], j * 40, i * 40)
        if state["won"]:
            sweeperlib.prepare_rectangle(
                int(state["col"] * 40 * (1 / 2) - 250),
                int(state["row"] * 40 * (2 / 4)),
                500,
                100,
                (0, 255, 0, 255),
            )
        sweeperlib.draw_sprites()
        sweeperlib.draw_text(
            "⚑: " + str(state["bombs_counts"]),
            0,
            state["row"] * 40,
            (0, 0, 0, 255),
            "arial",
            20,
        )
        icon = (
            ("☺", (255, 255, 0, 255))
            if not state["game_over"]
            else ("☹", (255, 0, 0, 255))
        )
        icon = ("🏆", (0, 255, 0, 255)) if state["won"] else icon
        sweeperlib.draw_text(
            icon[0],
            int((state["col"] * 40) / 2) - 5,
            state["row"] * 40 - 5,
            icon[1],
            "Segoe UI Symbol",
            40,
        )
        sweeperlib.draw_text(
            "⚙",
            state["col"] * 40 - 40,
            state["row"] * 40,
            (0, 0, 0, 255),
            "Segoe UI Symbol",
            25,
        )
        sweeperlib.draw_text(
            f"⏲: {int(state['time'])}",
            100,
            state["row"] * 40,
            (0, 0, 0, 255),
            "Segoe UI Symbol",
            20,
        )
        if state["won"] or state["game_over"] and not state["leaderboard"]:
            sweeperlib.prepare_rectangle(
                int(state["col"] * 40 * (1 / 2) - 250),
                int(state["row"] * 40 * (2 / 4)),
                500,
                100,
                (0, 255, 0, 255) if state["won"] else (255, 0, 0, 255),
            )
            sweeperlib.draw_text(
                "You Won" if state["won"] else "You lost",
                int(state["col"] * 40 * (1 / 2) - 70),
                int(state["row"] * 40 * (2 / 4) + 50),
                (0, 0, 0, 255),
                "arial",
            )
            sweeperlib.draw_text(
                "press on play field to get back to menu",
                int(state["col"] * 40 * (1 / 2) - 100),
                int(state["row"] * 40 * (2 / 4) + 20),
                (0, 0, 0, 255),
                "arial",
                10,
            )

        if state["setting"] and not state["leaderboard"]:
            setting_window()
        elif state["leaderboard"]:
            leaderboard()
        else:
            sweeperlib.resize_window(state["col"] * 40, state["row"] * 40 + 50)
    except KeyboardInterrupt:
        sweeperlib.close()


def main():
    """
    Initializes the game window, sets up event handlers, and starts the game.
    """
    sweeperlib.create_window(state["col"] * 40, state["row"] * 40 + 50)
    sweeperlib.set_mouse_handler(handle_mouse)
    sweeperlib.set_draw_handler(draw_field)
    sweeperlib.set_keyboard_handler(handle_keyboard_access_menu)
    sweeperlib.set_interval_handler(time_handler)
    sweeperlib.start()


if __name__ == "__main__":
    sweeperlib.load_sprites("sprites")
    state["row"] = 10
    state["col"] = 15
    state["bombs"] = 20
    state["setting"] = True
    reset_button(state)
    main()
