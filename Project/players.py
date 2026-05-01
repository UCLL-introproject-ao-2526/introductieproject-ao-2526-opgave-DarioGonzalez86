import csv
import os


# [dn] Je file heet players.py. Het is normaal altijd enkelvoudig je dingen te benoemen, dus 'player.py". 
CSV_FILE = "players.csv"


def load_players_csv(path=CSV_FILE):
    players = {}
    if not os.path.exists(path):
        return players
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            players[row["Name"]] = {
                "Win": int(row["Win"]),
                "Lose": int(row["Lose"]),
                "Draw": int(row["Draw"])
            }
    return players


def save_players_csv(players, path=CSV_FILE):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Win", "Lose", "Draw"])
        writer.writeheader()
        for name, stats in players.items():
            writer.writerow({
                "Name": name,
                "Win": stats["Win"],
                "Lose": stats["Lose"],
                "Draw": stats["Draw"]
                #[dn] je hebt best wat duplicatie met de strings, bvb "Draw". Je kan best DRAW_STRING = "Draw" doen, dat is wat veiliger
            })

# Setup of player class


class Player:
    def __init__(self, name):
        self.name = name
        self.win = 0
        self.lose = 0
        self.draw = 0 #niet meteen duidelijk wat de variabelen zijn. amount_of_draws?

    @property
    def name(self):
        return self.__name

    @property
    def game_history(self):
        return (self.win, self.lose, self.draw)

    @name.setter
    def name(self, value):
        if len(value) <= 0:
            raise ValueError("Name is mandatory.")
        if len(value) > 20:
            raise ValueError("Name must be less than 20 characters.")
        self.__name = value

    @game_history.setter
    def game_history(self, value):
        if len(value) != 3:
            raise ValueError("Wrong format for game history")
        win, lose, draw = value
        if win < 0 or lose < 0 or draw < 0:
            raise ValueError(
                "The number of games won/lost/drawn can't be lower than 0")
        self.win = win
        self.lose = lose
        self.draw = draw

    def __str__(self):
        # w, l, d = self.__game_history
        return f"{self.name} — Won: {self.win} — Lost: {self.lose} — Drawn: {self.draw}"


# Functions to check and store player information in CSV file
def save_player(player):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow([player, 0, 0, 0])  # win, lose, draw


def check_player(player):
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            name = row[0].strip().lower()
            if name == player.strip().lower():
                return True
    return False


def get_correct_player_name(player):
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].strip().lower() == player.strip().lower():
                return row[0]
    return None
