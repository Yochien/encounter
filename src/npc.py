from abc import ABC, abstractmethod
from typing import Type


class NPC(ABC):
    def __init__(self, name: str, maxHP: int, ac: int):
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
        if maxHP < 1:
            raise ValueError("HP must be at least 1.")
        if ac < 0:
            raise ValueError("AC must be at least 0.")

        # Value assignment
        self.name = name
        self.maxHP = maxHP
        self.ac = int(ac)

    def __str__(self):
        return self.name

    @abstractmethod
    def detailedInfo(self) -> str:
        raise NotImplementedError("This methods needs a comcrete implementation.")


class BookNPC(NPC):
    def __init__(self, name: str, maxHP: int, ac: int, description: str | None = None):
        super().__init__(name, maxHP, ac)
        self.description = description

    def detailedInfo(self) -> str:
        info = ""
        info += f"NAME: {self.name}\n"
        info += f"MAX HP: {self.maxHP}\n"
        info += f"AC: {self.ac}"
        if self.description is not None:
            info += f"\nDESCRIPTION: {self.description}"
        return info


class CombatNPC(NPC):
    def __init__(self, name: str, maxHP: int, ac: int, nick: str | None = None):
        super().__init__(name, maxHP, ac)
        if nick is not None:
            if len(nick) < 1:
                raise ValueError("Nickname must be at least length 1.")
            if nick.isspace():
                raise ValueError("Nickname must not be blank.")
        self.nick = nick
        self.marked = False
        self.note = ""
        self.currentHP = self.maxHP
        self.maxRank = self.currentRank = 0

    def __str__(self):
        rank = f"({self.currentRank}) " if (self.currentRank > 0) else ""
        name = self.name if (self.nick is None) else self.nick
        mark = "*" if self.marked else ""
        is_dead = " [X]" if (self.currentHP == 0) else ""

        return f"{rank}{name}{mark}{is_dead}"

    def __lt__(self, other):
        return self.currentRank < other.currentRank

    def detailedInfo(self) -> str:
        name = self.name if (self.nick is None) else f"{self.nick} ({self.name})"
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


class NPCList:
    def __init__(self, names: list[str], npc_type: Type[NPC]):
        # Error Checking
        if type(names) != list:
            raise TypeError("Names must be a list of strings.")
        if len(names) < 1:
            raise ValueError("List must contain at least one entry.")
        if not issubclass(npc_type, NPC):
            raise TypeError(f"Must store a type of NPC. but was {type(npc_type)}")

        # Value assignment
        self.names = names
        self.name = names[0]
        self.data: list = []

    def __len__(self):
        return len(self.data)

    def toMenu(self):
        info = self.name.upper() + ":\n"

        if len(self.data) == 0:
            info += "EMPTY"
            return info
        else:
            for i in self.data:
                info += f"{self.data.index(i) + 1} {i}\n"

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
