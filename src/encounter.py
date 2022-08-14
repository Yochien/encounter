from abc import ABC, abstractmethod


class NPC:
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
        if maxHP < 1:
            raise ValueError("HP must be at least 1.")
        if ac < 0:
            raise ValueError("AC must be at least 0.")

        # Value assignment
        self.name = name
        self.maxHP = self.currentHP = maxHP
        self.ac = int(ac)

    def __str__(self):
        if self.currentHP > 0:
            return self.name
        else:
            return self.name + " [X]"

    def equals(self, other):
        if self == other:
            return True
        if other is None:
            return False
        if self.name != other.name:
            return False
        if self.maxHP != other.maxHP:
            return False
        if self.currentHP != other.currentHP:
            return False
        if self.ac != other.ac:
            return False
        return True

    def combatStatus(self) -> str:
        if self.currentHP > 0:
            return self.name + " [" + str(self.currentHP) + "/" + str(self.maxHP) + "]"
        else:
            return self.name + " [Dead]"

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
            raise TypeError("Argument names must be a list of strings.")

        if len(names) < 1:
            raise ValueError("Argument names must contain at least one entry.")

        # Value assignment
        self.names = names
        self.name = names[0]
        self.data: list[NPC] = []

    def toMenu(self):
        info = self.name.upper() + ":\n"

        if len(self.data) == 0:
            info += "EMPTY"
        else:
            for i in self.data[:-1]:
                info += str(self.data.index(i) + 1) + " " + str(i) + "\n"
            info += str(self.data.index(self.data[-1]) + 1) + " " + str(self.data[-1])

        info += "\n"
        return info


def findList(name: str, referenceLists: list[NPCList]) -> NPCList | None:
    name = name.lower()
    for list in referenceLists:
        if name in list.names:
            return list
    return None


class Command(ABC):
    def __init__(self):
        self.names: list[str] = ['Command', 'Test']
        self.description: str = "This Command has no defined description yet."
        self.usageStr: str = "This command has no defined usage yet."

    def usage(self) -> None:
        print("Usage: " + self.usageStr)

    @abstractmethod
    def execute(self, args = []) -> None:
        raise NotImplementedError("This command has not been implemented yet.")


class load(Command):
    def __init__(self, bestiary):
        super().__init__()
        self.names = ['load']
        self.bestiary = bestiary
        self.description = "Replaces the default bestiary."
        self.usageStr = "load <file_name>"

    def execute(self, args = []):
        numArgs = len(args)

        if numArgs == 1:
            try:
                bestiaryFile = open(args[0])
            except FileNotFoundError:
                print("Selected bestiary file could not be found.")
                if len(self.bestiary.data) == 0:
                    print("Loading placeholder bestiary.")
                    self.bestiary.data.append(NPC("Human", 5, 12))
                    self.bestiary.data.append(NPC("Animal", 3, 10))
                    self.bestiary.data.append(NPC("Enemy", 10, 13))
            else:
                self.bestiary.data.clear()
                for line in bestiaryFile:
                    if not line.startswith("#"):
                        line = line.rstrip("\n").split(",")
                        npc = NPC(line[0], int(line[1]), int(line[2]))
                        self.bestiary.data.append(npc)
                bestiaryFile.close()
                print("Bestiary loaded.")
        else:
            self.usage()


class displayHelp(Command):
    def __init__(self, commands: list[Command]):
        super().__init__()
        self.names = ['help', '?']
        self.commands = commands
        self.description = "Prints a list of availible commands."
        self.usageStr = "help [command_name]"

    def execute(self, args = []):
        numArgs = len(args)

        if numArgs == 1:
            if args[0].lower() in ["quit", "q", "exit"]:
                print("Exits the program.")
                print("Usage: {quit | q | exit}")
            else:
                found = False
                for command in self.commands:
                    if args[0].lower() in command.names:
                        print(command.description)
                        command.usage()
                        found = True
                        break

                if not found:
                    print("Unrecognized command.")
                    print("Type help or ? to learn how to use availible commands.")
        else:
            if numArgs == 0:
                spacing = 0
                for command in self.commands:
                    if len(command.names[0]) > spacing:
                        spacing = len(command.names[0])
                print("quit".ljust(spacing) + ": " + "Exits the program.")
                for command in self.commands:
                    print(command.names[0].ljust(spacing) + ": " + command.description)
                print("")
                print("For more detailed information > Usage: " + self.usageStr)
            else:
                self.usage()


class displayMenu(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.names = ['list', 'display', 'show']
        self.referenceLists = referenceLists
        self.description = "Displays a list of NPCs."
        self.usageStr = "list [all | bestiary | encounter]"

    def execute(self, args = []):
        numArgs = len(args)

        if numArgs == 1 and args[0] != "all":
            list = findList(args[0], self.referenceLists)

            if list is not None:
                print(list.toMenu())
            else:
                print("Unknown list selected.")
        else:
            if numArgs == 0 or args[0] == "all":
                for list in self.referenceLists:
                    print(list.toMenu())
            else:
                self.usage()


def isInt(string: str) -> bool:
    if string.isnumeric():
        return True
    else:
        try:
            int(string)
        except ValueError:
            return False
        else:
            return True


def isValidInt(selector: str, list: list[NPC]) -> bool:
    selected = selector.split(",")
    for index in selected:
        if not isInt(index) or int(index) <= 0 or int(index) > len(list):
            print("One or more inputs are invalid in this context.")
            return False
    return True


def copyNPC(bestiaryList, index: int, list: list[NPC]) -> None:
    name = bestiaryList[index - 1].name
    hp = bestiaryList[index - 1].maxHP
    ac = bestiaryList[index - 1].ac
    npc = NPC(name, hp, ac)
    list.append(npc)


class addNPC(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.names = ['add']
        self.referenceLists = referenceLists
        self.description = "Adds an NPC to the encounter."
        self.usageStr = "add <bestiary_index,...>"

    def execute(self, args = []):
        bestiary = findList("bestiary", self.referenceLists)
        encounter = findList("encounter", self.referenceLists)

        if len(args) == 1:
            selected = args[0].split(",")

            for index in selected:
                if not isInt(index) or int(index) > len(bestiary.data) or int(index) <= 0:
                    self.usage()
                    return

            for index in selected:
                copyNPC(bestiary.data, int(index), encounter.data)
            print(encounter.toMenu())
        else:
            self.usage()


class clearNPCList(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.names = ['clear']
        self.referenceLists = referenceLists
        self.description = "Clears a list of NPCs."
        self.usageStr = "clear {all | bestiary | encounter}"

    def execute(self, args = []):
        if len(args) == 1:
            if args[0].lower() == "all":
                for list in self.referenceLists:
                    list.data.clear()
                    print(list.toMenu())
            else:
                list = findList(args[0], self.referenceLists)

                if list is not None:
                    list.data.clear()
                    print(list.toMenu())
                else:
                    print("Unknown list selected.")
        else:
            self.usage()


class removeNPC(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ['remove']
        self.encounter = encounter
        self.description = "Removes an NPC from the encounter."
        self.usageStr = "remove <index,...>"

    def execute(self, args = []):
        if len(args) == 1:
            if args[0] == "all":
                self.encounter.data.clear()
                print(self.encounter.toMenu())
            else:
                selected = args[0].split(",")

                for index in selected:
                    if not isValidInt(index, self.encounter.data):
                        return

                # Remove duplicates and reverse sort the input
                selected = sorted(list(set(selected)), reverse = True)

                for index in selected:
                    self.encounter.data.pop(int(index) - 1)
                print(self.encounter.toMenu())
        else:
            self.usage()


def areAllDefeated(encounter):
    for npc in encounter:
        if npc.currentHP > 0:
            return False
    return True


class attack(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ['attack']
        self.encounter = encounter
        self.description = "Initiantiates D&D like combat with an NPC."
        self.usageStr = "attack <index> [hit] [damage]"

    def execute(self, args = []):
        lenArgs = len(args)
        npc = None

        if lenArgs > 3 or lenArgs < 1:
            self.usage()
            return

        if not isValidInt(args[0], self.encounter.data):
            self.usage()
            return

        npc = self.encounter.data[int(args[0]) - 1]
        if npc.currentHP <= 0:
            print("Enemy already defeated.")
            return

        if lenArgs == 3:
            if not isInt(args[1]) or not isInt(args[2]):
                self.usage()
                return

            if int(args[1]) >= npc.ac:
                npc.currentHP = max(0, npc.currentHP - int(args[2]))
                print(npc.name + " took " + args[2] + " damage.")
            else:
                print("Attack misses " + npc.name + ".")
        elif lenArgs == 2:
            if not isInt(args[1]):
                self.usage()
                return

            if int(args[1]) >= npc.ac:
                damage = input("Roll for damage: ")
                if damage.isnumeric() is True:
                    amt = int(damage)
                    npc.currentHP = max(0, npc.currentHP - amt)
                    print(npc.name + " took " + damage + " damage.")
                else:
                    print("Damage must be a number.")
            else:
                print("Attack misses " + npc.name + ".")
        elif lenArgs == 1:
            accuracy = input("Roll for hit: ")
            if accuracy.isnumeric() is True:
                accuracy = int(accuracy)
                if accuracy >= npc.ac:
                    damage = input("Roll for damage: ")
                    if damage.isnumeric() is True:
                        amt = int(damage)
                        npc.currentHP = max(0, npc.currentHP - amt)
                        print(npc.name + " took " + damage + " damage.")
                    else:
                        print("Damage must be a number.")
                else:
                    print("Attack misses " + npc.name + ".")
            else:
                print("Accuracy must be a number.")

        if npc is not None:
            if npc.currentHP <= 0:
                print(npc.name + " has been defeated.")
                if areAllDefeated(self.encounter.data):
                    print("Party has defeated all enemies.")


class damage(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ['damage']
        self.encounter = encounter
        self.description = "Directly subtracts from an NPC's health."
        self.usageStr = "damage <index> <amount>"

    def execute(self, args = []):
        if len(args) == 2:
            if not isInt(args[1]):
                self.usage()
                return
            if isValidInt(args[0], self.encounter.data) is True:
                npc = self.encounter.data[int(args[0]) - 1]

                if npc.currentHP <= 0:
                    print("Enemy already defeated.")
                    return

                npc.currentHP = max(0, npc.currentHP - int(args[1]))
                if npc.currentHP <= 0:
                    print(npc.name + " has been defeated.")
                    if areAllDefeated(self.encounter.data):
                        print("Party has defeated all enemies.")
        else:
            self.usage()


class smite(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ['smite', 'kill']
        self.encounter = encounter
        self.description = "Immediately kills an NPC."
        self.usageStr = "smite <bestiary_index>"

    def execute(self, args = []):
        if len(self.encounter.data) > 0:
            if len(args) == 1:
                if isValidInt(args[0], self.encounter.data) is True:
                    npc = self.encounter.data[int(args[0]) - 1]
                    if npc.currentHP <= 0:
                        print("Enemy already defeated.")
                        return
                    else:
                        npc.currentHP = 0
                        print(npc.name + " was defeated.")

                        if areAllDefeated(self.encounter.data):
                            print("Party has defeated all enemies.")
            else:
                self.usage()
        else:
            print("Encounter is empty. There is no one to smite.")


class heal(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ['heal']
        self.encounter = encounter
        self.description = "Directly adds to an NPC's health."
        self.usageStr = "heal <index> <amount>"

    def execute(self, args = []):
        if len(args) == 2:
            if not isInt(args[1]):
                self.usage()
                return
            if isValidInt(args[0], self.encounter.data):
                npc = self.encounter.data[int(args[0]) - 1]
                origHP = npc.currentHP

                npc.currentHP = npc.currentHP + int(args[1])

                if npc.currentHP > npc.maxHP:
                    npc.currentHP = npc.maxHP

                healedAmt = npc.currentHP - origHP

                print(npc.name + " was healed " + str(healedAmt) + " points.")
        else:
            self.usage()


class status(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ['status']
        self.encounter = encounter
        self.description = "Displays an NPC's current stats."
        self.usageStr = "status <index>"

    def execute(self, args = []):
        if len(args) == 1:
            if isinstance(args[0], str) and args[0].lower() == "all":
                print("Status:")
                for npc in self.encounter.data:
                    print(npc.combatStatus())
            elif isValidInt(args[0], self.encounter.data):
                npc = self.encounter.data[int(args[0]) - 1]
                print("Status:")
                print(npc.combatStatus())
            else:
                self.usage()
        else:
            self.usage()


class info(Command):
    def __init__(self, bestiary):
        super().__init__()
        self.names = ['info', 'details']
        self.bestiary = bestiary
        self.description = "Displays detailed stats for a bestiary entry."
        self.usageStr = "info <index>"

    def execute(self, args = []):
        if len(args) == 1:
            if isInt(args[0]):
                if isValidInt(args[0], self.bestiary.data):
                    print("INFO:")
                    print(self.bestiary.data[int(args[0]) - 1].detailedInfo())
            else:
                self.usage()
        else:
            self.usage()


class make(Command):
    def __init__(self, bestiary):
        super().__init__()
        self.names = ["make"]
        self.bestiary = bestiary
        self.description = "Creates an NPC for the bestiary"
        self.usageStr = "make <name> <max hp> <armor class>"

    def execute(self, args=[]) -> None:
        if len(args) == 3:
            if args[0].isnumeric() or not isInt(args[1]) or not isInt(args[2]):
                self.usage()
                return
            self.bestiary.data.append(NPC(args[0], int(args[1]), int(args[2])))
            print(self.bestiary.toMenu())
        else:
            self.usage()


def main():
    bestiary = NPCList(['bestiary', 'book', 'b'])
    encounter = NPCList(['encounter', 'e', "combat", "c"])
    referenceLists = [bestiary, encounter]

    # Instantiate commands
    commands = [
        load(bestiary),
        displayMenu(referenceLists),
        addNPC(referenceLists),
        removeNPC(encounter),
        clearNPCList(referenceLists),
        smite(encounter),
        damage(encounter),
        attack(encounter),
        heal(encounter),
        status(encounter),
        info(bestiary),
        make(bestiary)
    ]

    commands.append(displayHelp(commands))

    # Load default bestiary
    commands[0].execute(["bestiary.txt"])

    print("Type help or ? to get a list of availible commands.")

    # command loop
    while True:
        usrRequest = input("Type a command: ").lower().split(" ")

        action = None

        if usrRequest != ['']:
            action = usrRequest[0]

        if action == "quit" or action == "q" or action == "exit":
            break

        args = []

        if (len(usrRequest) > 1):
            for index in range(1, len(usrRequest)):
                args.append(usrRequest[index])

        found = False
        for command in commands:
            if action in command.names:
                command.execute(args)
                found = True
                break

        if not found:
            print("Unrecognized command.")
            print("Type help or ? to learn how to use availible commands.")


if __name__ == "__main__":
    main()
