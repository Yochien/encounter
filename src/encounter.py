from abc import ABC, abstractmethod


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
        if nick is None:
            self.nick = name
        else:
            self.nick = nick
        self.maxHP = self.currentHP = maxHP
        self.ac = int(ac)

    def __str__(self):
        output = ""
        if self.nick is not self.name:
            output += self.nick + " (" + self.name + ")"
        else:
            output += self.name

        if self.marked:
            output += "*"

        if self.currentHP <= 0:
            output += " [X]"

        return output

    def equals(self, other):
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
        return True

    def combatStatus(self) -> str:
        status = ""
        if self.currentHP > 0:
            if self.name is not self.nick:
                status += self.nick + " (" + self.name + ")"
            else:
                status += self.name
            status += " [" + str(self.currentHP) + "/" + str(self.maxHP) + "]"
        else:
            if self.name is not self.nick:
                status += self.nick + " (" + self.name + ")"
            else:
                status += self.name
            status += " [Dead]"

        if self.marked:
            status += "\nNote:\n"
            if not self.note.isspace() and len(self.note) > 0:
                status += self.note
            else:
                status += "EMPTY"

        return status

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
                bestiaryFile = open(args[0].strip())
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
                    if not (line.startswith("#") or line.isspace()):
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
    def __init__(self, referenceLists: list[NPCList]):
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
                    if list is not self.referenceLists[-1]:
                        print()
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
            return False
    return True


def copyNPC(bestiaryList, index: int, list: list[NPC]) -> None:
    npc = bestiaryList[index - 1]
    copy = NPC(npc.name, npc.maxHP, npc.ac)
    list.append(copy)


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
                    if list is not self.referenceLists[-1]:
                        print()
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
                print(npc.nick + " took " + args[2] + " damage.")
            else:
                print("Attack misses " + npc.nick + ".")
        elif lenArgs == 2:
            if not isInt(args[1]):
                self.usage()
                return

            if int(args[1]) >= npc.ac:
                damage = input("Roll for damage: ")
                if damage.isnumeric() is True:
                    amt = int(damage)
                    npc.currentHP = max(0, npc.currentHP - amt)
                    print(npc.nick + " took " + damage + " damage.")
                else:
                    print("Damage must be a number.")
            else:
                print("Attack misses " + npc.nick + ".")
        elif lenArgs == 1:
            accuracy = input("Roll for hit: ")
            if accuracy.isnumeric() is True:
                accuracy = int(accuracy)
                if accuracy >= npc.ac:
                    damage = input("Roll for damage: ")
                    if damage.isnumeric() is True:
                        amt = int(damage)
                        npc.currentHP = max(0, npc.currentHP - amt)
                        print(npc.nick + " took " + damage + " damage.")
                    else:
                        print("Damage must be a number.")
                else:
                    print("Attack misses " + npc.nick + ".")
            else:
                print("Accuracy must be a number.")

        if npc is not None:
            if npc.currentHP <= 0:
                print(npc.nick + " has been defeated.")
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
                    print(npc.nick + " has been defeated.")
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
                        print(npc.nick + " was defeated.")

                        if areAllDefeated(self.encounter.data):
                            print("Party has defeated all enemies.")
                else:
                    self.usage()
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

                print(npc.nick + " was healed " + str(healedAmt) + " points.")
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
        self.names = ['make']
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


class name(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ['name', 'nick']
        self.encounter = encounter
        self.description = "Gives a specific name to an NPC in the encounter"
        self.usageStr = "name <index> <nickname>"

    def execute(self, args=[]) -> None:
        if len(args) == 2:
            if not args[0].isnumeric():
                self.usage()
                return
            if isValidInt(args[0], self.encounter.data) is True:
                self.encounter.data[int(args[0]) - 1].nick = args[1]
            else:
                self.usage()
        else:
            self.usage()


class mark(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ['mark', 'note']
        self.encounter = encounter
        self.description = "Mark an NPC with a symbol and note"
        self.usageStr = "mark <index> [note]"

    def execute(self, args=[]) -> None:
        if len(args) >= 1:
            if not args[0].isnumeric():
                if args[0].lower() == "all":
                    for npc in self.encounter.data:
                        npc.marked = True
                        if len(args) > 1:
                            npc.note = " ".join(args[1:])
                        else:
                            npc.note = ""
                else:
                    self.usage()
                return
            if isValidInt(args[0], self.encounter.data) is True:
                self.encounter.data[int(args[0]) - 1].marked = True
                if len(args) > 1:
                    self.encounter.data[int(args[0]) - 1].note = " ".join(args[1:])
                else:
                    self.encounter.data[int(args[0]) - 1].note = ""
            else:
                self.usage()
        else:
            self.usage()


class unmark(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ['unmark']
        self.encounter = encounter
        self.description = "Remove mark and symbol from an NPC"
        self.usageStr = "unmark <index>"

    def execute(self, args=[]) -> None:
        if len(args) == 1:
            if not args[0].isnumeric():
                if args[0].lower() == "all":
                    for npc in self.encounter.data:
                        npc.marked = False
                        npc.note = ""
                else:
                    self.usage()
                return
            if isValidInt(args[0], self.encounter.data) is True:
                self.encounter.data[int(args[0]) - 1].marked = False
                self.encounter.data[int(args[0]) - 1].note = ""
            else:
                self.usage()
        else:
            self.usage()


def main():
    bestiary = NPCList(['bestiary', 'book', 'b'])
    encounter = NPCList(['encounter', 'e', 'combat', 'c'])
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
        make(bestiary),
        name(encounter),
        mark(encounter),
        unmark(encounter)
    ]

    commands.append(displayHelp(commands))

    # Load default bestiary
    commands[0].execute(["bestiary.txt"])

    print("Type help or ? to get a list of availible commands.")

    # command loop
    while True:
        print()
        usrRequest = input("Type a command: ").split(" ")

        action = None

        if usrRequest != ['']:
            action = usrRequest[0].lower()

        if action in ['quit', 'q', 'exit']:
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
