from abc import ABC, abstractmethod
from textwrap import dedent

import yaml

from src.npc import NPC, BookNPC, CombatNPC, NPCList, findList


class Command(ABC):
    def __init__(self):
        self.names: list[str] = ["command", "test"]
        self.description: str = "This command has no defined description yet."
        self.details: str | None = None
        self.usageStr: str = "This command has no defined usage yet."

    def usage(self) -> None:
        print("Usage: " + self.usageStr)

    @staticmethod
    def encounterEmpty() -> None:
        print("The encounter is empty. Add some NPCs to it and try again.")

    @staticmethod
    def OOBSelection(referenceList: NPCList) -> None:
        print("Your selection contains values out of range for the " + referenceList.name)
        print("Adjust your selection and try again.")

    @abstractmethod
    def execute(self, args = []) -> None:
        raise NotImplementedError("This command has not been implemented yet.")


class load(Command):
    def __init__(self, bestiary):
        super().__init__()
        self.names = ["load"]
        self.bestiary = bestiary
        self.description = "Replaces the loaded bestiary."
        self.details = dedent("""\
                              Searches the absolute address provided for a valid bestiary file.
                              The correct format for a file is provided in an example file "bestiary.yaml".
                              If the provided file cannot be loaded the current list will be kept.
                              If the current list is empty and a new list cannot be found
                              then some primitive entries will be generated.\
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "load <file_name>"

    def execute(self, args = []):
        numArgs = len(args)

        if numArgs == 1:
            try:
                bestiary_text = open(args[0].strip())
            except FileNotFoundError:
                print("Selected bestiary file could not be found.")
                if len(self.bestiary) == 0:
                    print("Loading placeholder bestiary.")
                    self.bestiary.data.append(BookNPC("Human", 5, 12, "Common townsfolk."))
                    self.bestiary.data.append(BookNPC("Animal", 3, 10))
                    self.bestiary.data.append(BookNPC("Enemy", 10, 13))
            else:
                self.bestiary.data.clear()
                num_npc_loaded = 0
                with bestiary_text:
                    try:
                        file = yaml.load(bestiary_text, Loader=yaml.BaseLoader)
                    except yaml.YAMLError:
                        print("Something is wrong the syntax of your bestiary file.")
                        print("Try validating the YAML file?")
                        exit()
                    else:
                        for npc, attributes in file.items():
                            name = npc
                            try:
                                hp = int(attributes["hp"])
                                ac = int(attributes["ac"])
                                try:
                                    description = attributes["description"]
                                except KeyError:
                                    description = None
                                npc = BookNPC(name, hp, ac, description)
                            except KeyError as key:
                                print(f"NPC \"{name}\" is missing the {key} attribute!")
                            except TypeError:
                                print(f"Formatting of NPC \"{name}\" is incorrect somehow!")
                            except ValueError as attr_err:
                                print(f"The NPC \"{name}\" has an invalid attribute!")
                                print(attr_err)
                            else:
                                self.bestiary.data.append(npc)
                                num_npc_loaded += 1
                print(f"Successfully loaded {num_npc_loaded}/{len(file.items())} NPCs")
        else:
            self.usage()


class displayHelp(Command):
    def __init__(self, commands: list[Command]):
        super().__init__()
        self.names = ["help", "?"]
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
                        if command.details is not None:
                            print("\nNote:")
                            print(command.details)
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
                print()
                print("For more detailed information > Usage: " + self.usageStr)
            else:
                self.usage()


class displayMenu(Command):
    def __init__(self, referenceLists: list[NPCList]):
        super().__init__()
        self.names = ["list", "display", "show"]
        self.referenceLists = referenceLists
        self.description = "Displays the selected list of NPCs."
        self.details = dedent("""\
                              The list command can be called using the aliases "display" and "show".
                              The selected list can be any valid alias for their respective list.
                              Allowed aliases for "bestiary" are "book" and "b".
                              Allowed aliases for "encounter" are "e", "combat", and "c".\
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "list [all | bestiary | encounter]"

    def execute(self, args = []):
        numArgs = len(args)

        if numArgs <= 1:
            if numArgs == 0 or args[0].lower() == "all":
                for list in self.referenceLists:
                    print(list.toMenu())
                    if list is not self.referenceLists[-1]:
                        print()  # Print newline between all lists
            else:
                list = findList(args[0], self.referenceLists)

                if list is not None:
                    print(list.toMenu())
                else:
                    print("Unknown list selected.")
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


def isValidInt(selector: str, referencList: NPCList) -> bool:
    selected = selector.split(",")
    for index in selected:
        if not isInt(index) or int(index) <= 0 or int(index) > len(referencList):
            return False
    return True


def copyNPC(bestiary: NPCList, index: int, encounter: NPCList) -> None:
    npc = bestiary.data[index]
    npc_instance = CombatNPC(npc.name, npc.maxHP, npc.ac)
    encounter.data.append(npc_instance)


class addNPC(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.names = ["add"]
        self.referenceLists = referenceLists
        self.description = "Adds an NPC to the encounter."
        self.details = dedent("""\
                              Reference entries in the bestiary by number.
                              Multiple NPCs (even multiple of the same type) can be added at the same time
                              in a comma separated list without spaces.
                              Can be used with the all selector.\
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "add <bestiary_index,...>"

    def execute(self, args = []):
        bestiary = findList("bestiary", self.referenceLists)
        if bestiary is None:
            raise TypeError("Bestiary list must be an NPCList.")
        encounter = findList("encounter", self.referenceLists)
        if encounter is None:
            raise TypeError("Encounter list must be an NPCList.")

        if len(args) == 1:
            if args[0].lower() == "all":
                for index, _ in enumerate(bestiary.data):
                    copyNPC(bestiary, index, encounter)
            elif not isInt(args[0]):
                self.usage()
                return
            elif not isValidInt(args[0], bestiary):
                Command.OOBSelection(bestiary)
                return
            else:
                selected = args[0].split(",")

                for index in selected:
                    copyNPC(bestiary, int(index) - 1, encounter)
        else:
            self.usage()


class clearNPCList(Command):
    def __init__(self, referenceLists):
        super().__init__()
        self.names = ["clear"]
        self.referenceLists = referenceLists
        self.description = "Removes all NPCs from a list."
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
        self.names = ["remove"]
        self.encounter = encounter
        self.description = "Removes selected NPC(s) from the encounter."
        self.details = dedent("""\
                              Can be used with the all selector.\
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "remove <index,...>"

    def execute(self, args = []):
        if (len(self.encounter) < 1):
            Command.encounterEmpty()
            return

        if len(args) == 1:
            if args[0].lower() == "all":
                self.encounter.data.clear()
            else:
                if not isValidInt(args[0], self.encounter):
                    Command.OOBSelection(self.encounter)
                    return

                selected = args[0].split(",")
                selected = sorted(list(set(selected)), reverse = True)  # Remove duplicates and reverse sort the input

                for index in selected:
                    self.encounter.data.pop(int(index) - 1)
        else:
            self.usage()


def areAllDefeated(encounter: NPCList):
    return all(npc.currentHP > 0 for npc in encounter.data)


class attack(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ["attack"]
        self.encounter = encounter
        self.description = "Initiantiates D&D like combat with an NPC."
        self.details = dedent("""\
                              The attack command is interactive meaning if you leave out
                              a required field you will be asked for the data instead of
                              the command throwing an error state.\
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "attack <index> [hit] [damage]"

    def execute(self, args = []):
        if (len(self.encounter) < 1):
            Command.encounterEmpty()
            return

        lenArgs = len(args)

        if lenArgs > 3 or lenArgs < 1:
            self.usage()
            return

        for i in range(lenArgs):
            if not isInt(args[i]):
                self.usage()
                return

        if not isValidInt(args[0], self.encounter):
            Command.OOBSelection(self.encounter)
            return

        npc = self.encounter.data[int(args[0]) - 1]
        if npc.currentHP <= 0:
            print("Enemy already defeated.")
            return

        if lenArgs == 3:
            if int(args[1]) >= npc.ac:
                npc.currentHP = max(0, npc.currentHP - int(args[2]))
                print(npc.nick + " took " + args[2] + " damage.")
            else:
                print("Attack misses " + npc.nick + ".")
        elif lenArgs == 2:
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

        if npc is not None and npc.currentHP <= 0:
            npc.currentRank = 0
            print(npc.nick + " has been defeated.")
            if areAllDefeated(self.encounter):
                print("Party has defeated all enemies.")


class damage(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ["damage"]
        self.encounter = encounter
        self.description = "Directly subtracts from selected NPCs' health."
        self.details = dedent("""\
                              Can be used with the all selector.\
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "damage <encounter_index,...> <amount>"

    def execute(self, args = []):
        if (len(self.encounter) < 1):
            Command.encounterEmpty()
            return

        if len(args) == 2 and isInt(args[1]):
            if int(args[1]) < 1:
                print("Amount must be more than zero.")
                return
            if args[0].lower() == "all":
                for npc in self.encounter.data:
                    if npc.currentHP > 0:
                        npc.currentHP = max(0, npc.currentHP - int(args[1]))
                        if npc.currentHP <= 0:
                            npc.currentRank = 0
                            print(npc.nick + " has been defeated.")
                            if areAllDefeated(self.encounter):
                                print("Party has defeated all enemies.")
            else:
                if not isValidInt(args[0], self.encounter):
                    Command.OOBSelection(self.encounter)
                    return

                selected = args[0].split(",")
                selected = list(set(selected))

                for index in selected:
                    npc = self.encounter.data[int(index) - 1]

                    if npc.currentHP <= 0:
                        print(npc.nick + " already defeated.")
                        continue

                    npc.currentHP = max(0, npc.currentHP - int(args[1]))

                    if npc.currentHP <= 0:
                        npc.currentRank = 0
                        print(npc.nick + " has been defeated.")
                        if areAllDefeated(self.encounter):
                            print("Party has defeated all enemies.")
                            return
        else:
            self.usage()


class smite(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ["smite", "kill"]
        self.encounter = encounter
        self.description = "Immediately kills an NPC."
        self.details = dedent("""\
                              The smite command can be called using the alias "kill".
                              Supports the all selector, i.e. "kill all" will smite all NPCs in the encounter.\
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "smite <encounter_index,...>"

    def execute(self, args = []):
        if (len(self.encounter) < 1):
            Command.encounterEmpty()
            return

        if len(args) == 1:
            if args[0].lower() == "all":
                for npc in self.encounter.data:
                    npc.currentHP = 0
                    npc.currentRank = 0
            else:
                if not isValidInt(args[0], self.encounter):
                    Command.OOBSelection(self.encounter)
                    return

                selected = args[0].split(",")
                selected = list(set(selected))  # Remove duplicates from the selection

                for index in selected:
                    npc = self.encounter.data[int(index) - 1]
                    if npc.currentHP <= 0:
                        print(npc.nick + " already defeated.")
                        return
                    else:
                        npc.currentHP = 0
                        npc.currentRank = 0

                        if areAllDefeated(self.encounter):
                            print("Party has defeated all enemies.")
        else:
            self.usage()


class heal(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ["heal"]
        self.encounter = encounter
        self.description = "Directly adds to selected NPCs' health."
        self.details = dedent("""\
                              Can be used with the all selector.\
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "heal <encounter_index,...> <amount>"

    def __healNPC(self, npc: NPC, amount: int) -> int:
        if not isinstance(npc, CombatNPC):
            raise TypeError()

        originalHP = npc.currentHP
        npc.currentHP = originalHP + amount
        npc.currentHP = min(npc.maxHP, npc.currentHP)
        return npc.currentHP - originalHP

    def execute(self, args = []):
        if (len(self.encounter) < 1):
            Command.encounterEmpty()
            return

        if len(args) == 2 and isInt(args[1]):
            if int(args[1]) < 1:
                print("Amount must be more than zero.")
                return
            if args[0].lower() == "all":
                for npc in self.encounter.data:
                    npc.currentRank = npc.maxRank
                    healedAmt = self.__healNPC(npc, int(args[1]))
                    if healedAmt > 0:
                        print(f"{npc.nick} was healed {healedAmt} points.")
            else:
                if not isValidInt(args[0], self.encounter):
                    Command.OOBSelection(self.encounter)
                    return

                selected = args[0].split(",")
                selected = list(set(selected))

                for index in selected:
                    npc = self.encounter.data[int(index) - 1]
                    npc.currentRank = npc.maxRank
                    healedAmt = self.__healNPC(npc, int(args[1]))
                    print(npc.nick + " was healed " + str(healedAmt) + " points.")
        else:
            self.usage()


class status(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ["status"]
        self.encounter = encounter
        self.description = "Displays selected NPCs' current stats."
        self.details = dedent("""\
                              Displays the current health of the selected NPC in the encounter.
                              Additionally displays the contents of notes if any.
                              Supports the all selector.\
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "status <encounter_index,...>"

    def execute(self, args = []):
        if (len(self.encounter) < 1):
            Command.encounterEmpty()
            return

        if len(args) == 1:
            if args[0].lower() == "all":
                print("Status:")
                for npc in self.encounter.data:
                    print(npc.detailedInfo())
            elif isValidInt(args[0], self.encounter):
                selected = args[0].split(",")
                selected = list(set(selected))

                print("Status:")
                for index in selected:
                    npc = self.encounter.data[int(index) - 1]

                    print(npc.detailedInfo())
            else:
                Command.OOBSelection(self.encounter)
        else:
            self.usage()


class info(Command):
    def __init__(self, bestiary):
        super().__init__()
        self.names = ["info", "details"]
        self.bestiary = bestiary
        self.description = "Displays detailed stats for a bestiary entry."
        self.usageStr = "info <index>"

    def execute(self, args = []):
        if len(args) == 1:
            if isInt(args[0]):
                if isValidInt(args[0], self.bestiary):
                    print("INFO:")
                    print(self.bestiary.data[int(args[0]) - 1].detailedInfo())
                else:
                    Command.OOBSelection(self.bestiary)
            elif args[0].lower() == "all":
                print("INFO:")
                for entry in self.bestiary.data[:-1]:
                    print(entry.detailedInfo() + "\n")
                print(self.bestiary.data[-1].detailedInfo())
            else:
                if not isValidInt(args[0], self.bestiary):
                    Command.OOBSelection(self.bestiary)
                    return

                selected = args[0].split(",")
                selected = sorted(list(set(selected)))

                print("INFO:")
                for index in selected[:-1]:
                    entry = self.bestiary.data[int(index) - 1]
                    print(entry.detailedInfo() + "\n")
                print(self.bestiary.data[int(selected[-1]) - 1].detailedInfo())
        else:
            self.usage()


class make(Command):
    def __init__(self, bestiary):
        super().__init__()
        self.names = ["make"]
        self.bestiary = bestiary
        self.description = "Creates an NPC and adds it to the bestiary."
        self.details = dedent("""\
                              Entries added in this manner are temporary and will
                              not persist across reloads of the program.\
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "make <name> <max hp> <armor class>"

    def execute(self, args=[]) -> None:
        if len(args) >= 3 and not args[0].isnumeric() and isInt(args[1]) and isInt(args[2]):
            description = " ".join(args[3:]) if (len(args) > 3) else None
            self.bestiary.data.append(BookNPC(args[0], int(args[1]), int(args[2]), description))
        else:
            self.usage()


class name(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ["nickname", "name", "nn"]
        self.encounter = encounter
        self.description = "Gives a specific name to an NPC in the encounter."
        self.details = dedent("""\
                              Nicknames work on a per NPC basis. Multiple NPCs may have the
                              same nickname. The nickname does not replace the NPCs original
                              name and will still be displayed alongside it.
                              Can be called with the alias "name" or "nn".\
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "name <index> <nickname>"

    def execute(self, args=[]) -> None:
        if (len(self.encounter) < 1):
            Command.encounterEmpty()
            return

        if len(args) == 2 and args[0].isnumeric():
            if isValidInt(args[0], self.encounter):
                self.encounter.data[int(args[0]) - 1].nick = args[1]
            else:
                Command.OOBSelection(self.encounter)
        else:
            self.usage()


class mark(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ["mark", "note"]
        self.encounter = encounter
        self.description = "Mark an NPC with a symbol and note."
        self.details = dedent("""\
                              Can be used with the all selector. Will place an "*" next to the
                              NPC's name in any list display of NPCs. If this command is run on the same
                              NPC again the new note will overwrite their old note. This can be used
                              to delete a note entirely by replacing it with an empty note.
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "mark <encounter_index,...> [note]"

    def execute(self, args=[]) -> None:
        if (len(self.encounter) < 1):
            Command.encounterEmpty()
            return

        if len(args) >= 1:
            if args[0].lower() == "all":
                for npc in self.encounter.data:
                    npc.marked = True
                    if len(args) > 1:
                        npc.note = " ".join(args[1:])
                    else:
                        npc.note = ""
            else:
                if not isValidInt(args[0], self.encounter):
                    Command.OOBSelection(self.encounter)
                    return

                selected = args[0].split(",")
                selected = list(set(selected))

                for index in selected:
                    npc = self.encounter.data[int(index) - 1]
                    npc.marked = True
                    if len(args) > 1:
                        npc.note = " ".join(args[1:])
                    else:
                        npc.note = ""
        else:
            self.usage()


class unmark(Command):
    def __init__(self, encounter):
        super().__init__()
        self.names = ["unmark"]
        self.encounter = encounter
        self.description = "Remove mark and symbol from an NPC."
        self.details = dedent("""\
                              Can be used with the all selector.\
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "unmark <encounter_index,...>"

    def execute(self, args=[]) -> None:
        if (len(self.encounter) < 1):
            Command.encounterEmpty()
            return

        if len(args) == 1:
            if args[0].lower() == "all":
                for npc in self.encounter.data:
                    npc.marked = False
                    npc.note = ""
            else:
                if not isValidInt(args[0], self.encounter):
                    Command.OOBSelection(self.encounter)
                    return

                selected = args[0].split(",")
                selected = list(set(selected))

                for index in selected:
                    npc = self.encounter.data[int(index) - 1]
                    npc.marked = False
                    npc.note = ""
        else:
            self.usage()


class rank(Command):
    def __init__(self, encounter: NPCList):
        super().__init__()
        self.names = ["rank", "initiative"]
        self.encounter = encounter
        self.description = "Assigns NPCs a rank order."
        self.details = dedent("""\
                              NPCs order within the encounter will be determined by their rank.
                              NPCs with a higher value will appear higher in the list.
                              Assigning an NPC a rank of 0 or below removes their ranking.
                              This command can also be called with the alias "initiative".\
                              """).strip().replace("\n", " ").replace("\r", "")
        self.usageStr = "rank <encounter_index,...> <rank>"

    def execute(self, args=[]) -> None:
        if (len(self.encounter) < 1):
            Command.encounterEmpty()
            return

        if len(args) == 2 and isValidInt(args[0], self.encounter) and isInt(args[1]):
            rank = max(int(args[1]), 0)
            npc = self.encounter.data[int(args[0]) - 1]
            if not isinstance(npc, CombatNPC):
                raise TypeError()

            if npc.currentHP > 0:
                npc.currentRank = rank
                npc.maxRank = rank
            else:
                npc.maxRank = rank
        else:
            self.usage()


if __name__ == "__main__":
    print("Something seems wrong, this file is not meant to be executed.")
    print("Did you mean to run encounter instead?")
