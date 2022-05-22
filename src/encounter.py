from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self):
        self.nameList = ["Command", "Test"]
        self.description = "This Command has no defined description yet."
        self.usageStr = "This Command has no defined usage yet."

    def usage(self):
        print("Usage: " + self.usageStr)

    @abstractmethod
    def execute(self, args = []):
        print("This Command has not been implemented yet.")


class NPC:
    def __init__(self, name, maxHP, ac):
        # Type assertions
        if type(name) != str:
            raise TypeError("Argument name must be a string.")
        if type(maxHP) != int:
            raise TypeError("Argument HP must be an integer.")
        if type(ac) != int:
            raise TypeError("Argument AC must be an integer.")

        # Value assestions
        if len(name) < 1:
            raise ValueError("Name must be at least one character in length.")
        if ac < 0:
            raise ValueError("Argument out of valid range. AC must be at least 0.")
        if maxHP < 1:
            raise ValueError("Argument out of valid range. HP must be at least 1.")

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

    def toString(self):
        info = ""
        info += "NAME: " + str(self.name) + "\n"
        info += "HP: " + str(self.currentHP) + "\n"
        info += "AC: " + str(self.ac)
        return info


class NPCList:
    def __init__(self, nameList):
        # Error Checking
        if type(nameList) != list:
            raise TypeError("Argument nameList must be a list of strings.")

        if len(nameList) == 0:
            raise ValueError("Argument nameList must contain at least one entry.")

        # Value assignment
        self.nameList = nameList
        self.name = nameList[0]
        self.data = []

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


def findList(name, referenceLists):
    for list in referenceLists:
        if name in list.nameList:
            return list
    return None


class load(Command):
    def __init__(self, bestiary):
        super().__init__()
        self.nameList = ['load']
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
    def __init__(self, commandList):
        super().__init__()
        self.nameList = ['help', '?']
        self.commandList = commandList
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
                for command in self.commandList:
                    if args[0].lower() in command.nameList:
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
                for command in self.commandList:
                    if len(command.nameList[0]) > spacing:
                        spacing = len(command.nameList[0])
                print("quit".ljust(spacing) + ": " + "Exits the program.")
                for command in self.commandList:
                    print(command.nameList[0].ljust(spacing) + ": " + command.description)
                print("")
                print("For more detailed information > Usage: " + self.usageStr)
            else:
                self.usage()


class displayMenu(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.nameList = ['list', 'display', 'show']
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


def isInt(string):
    if string.isnumeric():
        return True
    else:
        try:
            int(string)
        except ValueError:
            return False
        else:
            return True


def isValidInt(selector, list):
    selector = selector.split(",")
    for s in selector:
        if not isInt(s) or int(s) <= 0 or int(s) > len(list):
            print("One or more inputs are invalid in this context.")
            return False
    return True


def npcCopy(bestiaryList, index, npcList):
    name = bestiaryList[int(index) - 1].name
    hp = bestiaryList[int(index) - 1].maxHP
    ac = bestiaryList[int(index) - 1].ac
    npc = NPC(name, hp, ac)
    npcList.append(npc)


class addNPC(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.nameList = ['add']
        self.referenceLists = referenceLists
        self.description = "Adds an NPC to a the encounter."
        self.usageStr = "add <bestiary_index,...>"

    def execute(self, args = []):
        bestiary = findList("bestiary", self.referenceLists)

        if len(args) == 1:
            selected = args[0].split(",")

            for i in selected:
                if not isInt(i) or int(i) > len(bestiary.data) or int(i) <= 0:
                    self.usage()
                    return

            for n in selected:
                npcCopy(bestiary.data, n, self.referenceLists[1].data)
            print(self.referenceLists[1].toMenu())
        else:
            self.usage()


class clearNPCList(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.nameList = ['clear']
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
    def __init__(self, referenceLists):
        super().__init__()
        self.nameList = ['remove']
        self.referenceLists = referenceLists
        self.description = "Removes an NPC from the encounter."
        self.usageStr = "remove <index,...>"

    def execute(self, args = []):
        if len(args) == 1:
            encounter = findList("encounter", self.referenceLists)

            if args[0] == "all":
                encounter.data.clear()
                print(encounter.toMenu())
            else:
                selected = args[0].split(",")

                for i in selected:
                    if not isValidInt(i, encounter):
                        return

                # Remove duplicates and reverse sort the input
                selected = sorted(list(set(selected)), reverse = True)

                for i in selected:
                    encounter.data.pop(int(i) - 1)
                print(encounter.toMenu())
        else:
            self.usage()


def areAllDefeated(encounter):
    for npc in encounter:
        if npc.currentHP > 0:
            return False
    return True


class attack(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.nameList = ['attack']
        self.referenceLists = referenceLists
        self.description = "Initiantiates D&D like combat with an NPC."
        self.usageStr = "attack <index> [hit] [damage]"

    def execute(self, args = []):
        encounter = findList("encounter", self.referenceLists)
        lenArgs = len(args)
        npc = None

        if lenArgs > 3 or lenArgs < 1:
            self.usage()
            return

        if not isValidInt(args[0], encounter.data):
            self.usage()
            return

        npc = encounter.data[int(args[0]) - 1]
        if npc.currentHP <= 0:
            print("Enemy already defeated.")
            return

        if lenArgs == 3:
            if not isInt(args[1]) or not isInt(args[2]):
                self.usage()
                return

            if int(args[1]) >= npc.ac:
                npc.currentHP = npc.currentHP - int(args[2])
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
                    npc.currentHP = npc.currentHP - amt
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
                        npc.currentHP = npc.currentHP - amt
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
                if areAllDefeated(encounter.data):
                    print("Party has defeated all enemies.")


class damage(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.nameList = ['damage']
        self.referenceLists = referenceLists
        self.description = "Directly subtracts from an NPC's health."
        self.usageStr = "damage <index> <amount>"

    def execute(self, args = []):
        encounter = findList("encounter", self.referenceLists)

        if len(args) == 2:
            if not isInt(args[1]):
                self.usage()
                return
            if isValidInt(args[0], encounter.data) is True:
                npc = encounter.data[int(args[0]) - 1]

                if npc.currentHP <= 0:
                    print("Enemy already defeated.")
                    return

                npc.currentHP = npc.currentHP - int(args[1])
                if npc.currentHP <= 0:
                    print(npc.name + " has been defeated.")
                    if areAllDefeated(encounter.data):
                        print("Party has defeated all enemies.")
        else:
            self.usage()


class smite(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.nameList = ['smite', 'kill']
        self.referenceLists = referenceLists
        self.description = "Immediately kills an NPC."
        self.usageStr = "smite <bestiary_index>"

    def execute(self, args = []):
        encounter = findList("encounter", self.referenceLists)

        if len(encounter.data) > 0:
            if len(args) == 1:
                if isValidInt(args[0], encounter.data) is True:
                    npc = encounter.data[int(args[0]) - 1]
                    if npc.currentHP <= 0:
                        print("Enemy already defeated.")
                        return
                    else:
                        npc.currentHP = 0
                        print(npc.name + " was defeated.")

                        if areAllDefeated(encounter.data):
                            print("Party has defeated all enemies.")
            else:
                self.usage()
        else:
            print("Encounter list is empty. There is no one to smite.")


class heal(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.nameList = ['heal']
        self.referenceLists = referenceLists
        self.description = "Directly adds to an NPC's health."
        self.usageStr = "heal <index> <amount>"

    def execute(self, args = []):
        encounter = findList("encounter", self.referenceLists)

        if len(args) == 2:
            if not isInt(args[1]):
                self.usage()
                return
            if isValidInt(args[0], encounter.data):
                npc = encounter.data[int(args[0]) - 1]
                origHP = npc.currentHP

                npc.currentHP = npc.currentHP + int(args[1])

                if npc.currentHP > npc.maxHP:
                    npc.currentHP = npc.maxHP

                healedAmt = npc.currentHP - origHP

                print(npc.name + " was healed " + str(healedAmt) + " points.")
        else:
            self.usage()


class status(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.nameList = ['status']
        self.referenceLists = referenceLists
        self.description = "Displays an NPC's current stats."
        self.usageStr = "status <index>"

    def execute(self, args = []):
        encounter = findList("encounter", self.referenceLists)

        if len(args) == 1:
            if isValidInt(args[0], encounter.data):
                npc = encounter.data[int(args[0]) - 1]
                print("Status:")
                print(npc.name + " [" + str(npc.currentHP) + " / " + str(npc.maxHP) + "]")
            else:
                self.usage()
        else:
            self.usage()


class info(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.nameList = ['info']
        self.referenceLists = referenceLists
        self.description = "Displays an NPC's detailed stats."
        self.usageStr = "info <index> {bestiary | encounter}"

    def execute(self, args = []):
        if len(args) == 2:
            if isInt(args[0]):
                list = findList(args[1], self.referenceLists)
                if list is not None:
                    if isValidInt(args[0], list.data):
                        print("INFO:")
                        print("NAME: " + list.data[int(args[0]) - 1].name)
                        print("HP: " + str(list.data[int(args[0]) - 1].currentHP))
                        print("MAX HP: " + str(list.data[int(args[0]) - 1].maxHP))
                        print("AC: " + str(list.data[int(args[0]) - 1].ac))
                else:
                    print("Unknown list selected.")
            else:
                self.usage()
        else:
            self.usage()


def main():
    referenceLists = [
        NPCList(['bestiary', 'book', 'b']),
        NPCList(['encounter', 'e', "combat", "c"])
    ]

    bestiary = findList("bestiary", referenceLists)

    # Instantiate commands
    commands = [
        load(bestiary),
        displayMenu(referenceLists),
        addNPC(referenceLists),
        removeNPC(referenceLists),
        clearNPCList(referenceLists),
        smite(referenceLists),
        damage(referenceLists),
        attack(referenceLists),
        heal(referenceLists),
        status(referenceLists),
        info(referenceLists)
    ]

    commands.append(displayHelp(commands))

    # Load default bestiary
    commands[0].execute(["bestiary.txt"])

    # print help message
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
            count = 1
            while count < len(usrRequest):
                args.append(usrRequest[count])
                count += 1

        found = False
        for command in commands:
            if action in command.nameList:
                command.execute(args)
                found = True
                break

        if not found:
            print("Unrecognized command.")
            print("Type help or ? to learn how to use availible commands.")


if __name__ == "__main__":
    main()
