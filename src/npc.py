from typing import Optional


class NPC:
    def __init__(self, name: str, maxHP: int, ac: int, nick: str | None = None):
        # Type assertions
        if type(name) != str:
            raise TypeError("Name must be a string.")
        if type(maxHP) != int:
            raise TypeError("HP must be an integer.")
        if type(ac) != int:
            raise TypeError("AC must be an integer.")

        # Value assertions
        if len(name) < 1:
            raise ValueError("Name must be at least length 1.")
        if name.isspace():
            raise ValueError("Name must not be blank.")
        if nick is not None and len(nick) < 1:
            raise ValueError("Nickname must be at least length 1.")
        if nick is not None and nick.isspace():
            raise ValueError("Nickname must not be blank.")
        if maxHP < 1:
            raise ValueError("HP must be at least 1.")
        if ac < 0:
            raise ValueError("AC must be at least 0.")

        # Value assignment
        self.marked = False
        self.note = ""
        self.name = name
        self.nick = name if (nick is None) else nick
        self.maxHP = self.currentHP = maxHP
        self.ac = int(ac)
        self.maxRank = self.currentRank = 0

    def __str__(self):
        rank = f"({self.currentRank}) " if (self.currentRank > 0) else ""
        name = self.name if (self.nick == self.name) else self.nick
        mark = "*" if self.marked else ""
        is_dead = " [X]" if (self.currentHP == 0) else ""

        return f"{rank}{name}{mark}{is_dead}"

    def __lt__(self, other):
        return self.currentRank < other.currentRank

    def equals(self: "NPC", other: Optional["NPC"]) -> bool:
        if self == other:
            return True
        if other is None:
            return False
        if self.name != other.name:
            return False
        if self.nick != other.nick:
            return False
        if self.maxHP != other.maxHP:
            return False
        if self.currentHP != other.currentHP:
            return False
        if self.ac != other.ac:
            return False
        if self.note != other.note:
            return False
        if self.maxRank != other.maxRank:
            return False
        if self.currentRank != other.currentRank:
            return False
        return True

    def combatStatus(self) -> str:
        name = (self.name if (self.nick == self.name)
                else f"{self.nick} ({self.name})")
        health = " [Dead]" if (self.currentHP == 0) else f" [{self.currentHP}/{self.maxHP}]"

        if self.marked:
            note = "\n> Note: "
            if not self.note.isspace() and len(self.note) > 0:
                note += self.note
            else:
                note += "EMPTY"
        else:
            note = ""

        return f"{name}{health}{note}"

    def detailedInfo(self) -> str:
        info = ""
        info += "NAME: " + str(self.name) + "\n"
        info += "MAX HP: " + str(self.maxHP) + "\n"
        info += "AC: " + str(self.ac)
        return info


class NPCList:
    def __init__(self, names: list[str]):
        # Error Checking
        if type(names) != list:
            raise TypeError("Names must be a list of strings.")

        if len(names) < 1:
            raise ValueError("List must contain at least one entry.")

        # Value assignment
        self.names = names
        self.name = names[0]
        self.data: list[NPC] = []

    def __len__(self):
        return len(self.data)

    def toMenu(self):
        info = self.name.upper() + ":\n"

        if len(self.data) == 0:
            info += "EMPTY"
            return info
        else:
            for i in self.data:
                info += str(self.data.index(i) + 1) + " " + str(i) + "\n"

        return info[:-1]


def findList(name: str, referenceLists: list[NPCList]) -> NPCList | None:
    name = name.lower()
    for list in referenceLists:
        if name in list.names:
            return list
    return None


if __name__ == "__main__":
    print("Something seems wrong, this file is not meant to be executed.")
    print("Did you mean to run encounter instead?")
