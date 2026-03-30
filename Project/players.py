# Algemene Class aangemaakt voor de spelers

class Player:
    def __init__(self, name):
        self.__name = name
        self.__game_history = [0, 0, 0]

    @property
    def name(self):
        return self.__name

    @property
    def game_history(self):
        return self.__game_history

    @name.setter
    def name(self, value):
        if len(value) <= 0:
            raise ValueError("Naam is verplicht")
        if len(value) > 20:
            raise ValueError("Naam mag maximum 20 characters lang zijn.")
        self.__name = value

    @game_history.setter
    def game_history(self, value):
        if len(value) != 3:
            raise ValueError("Verkeerde formaat voor game history")
        win, loss, draw = value
        if win < 0 or loss < 0 or draw < 0:
            raise ValueError(
                "Aantal van winst/verlies/gelijk kan niet negatief zijn.")
        self.__game_history[0] = win
        self.__game_history[1] = loss
        self.__game_history[2] = draw

    def __str__(self):
        w, l, d = self.__game_history
        return f"{self.__name} — Winst: {w} — Verloren: {l} — Gelijk: {d}"


# Code voor het wegschrijven en controleren van de spelerinformatie in het text bestand

def bewaar_speler(player):
    with open("players_history.txt", "a", encoding="utf-8") as output_file:
        output_file.write(f'{player.name},{player.game_history}\n')


def controleer_speler(player):
    with open("players_history.txt", "r", encoding="utf-8)") as input_file:
        for line in input_file:
            name, win, loss, draw = line.split(",")
            if player.name.lower() == name.lower():
                return False
    return True


def controleer_en_bewaar_speler(value):
    if controleer_speler(value):
        bewaar_speler(value)
    else:
        raise ValueError(
            f"De speler met de naam \"{value.name}\" bestaat reeds!")


# voorlopige code om te testen of de Class reageert zoals ik wou
dario = Player("Dario Gonzalez")
marco = Player("Marco Langone")
joey = Player("Joey Reynaerts")

# dario.game_history = [10, 1, 1]
# print(dario)

controleer_en_bewaar_speler(marco)
controleer_en_bewaar_speler(dario)
controleer_en_bewaar_speler(joey)

print(dario)
print(joey)
print(marco)
