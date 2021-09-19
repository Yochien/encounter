from abc import ABC, abstractmethod
#TODO implement settings
#Make lists generic with new type of list (name and other stored info)

class Command(ABC):
    def __init__(self, nameList):
        self.nameList = nameList
        self.description = "This Command has no defined description yet."
        self.usageStr = "This Command has no defined usage yet."
    
    def usage(self):
        print("Usage: " + self.usageStr)
    
    @abstractmethod
    def execute(self, args = []):
        print("This Command has not been implemented yet.")

class NPC:
    def __init__(self, name, maxHP, ac):
        self.name = name
        self.maxHP = self.currentHP = maxHP
        self.ac = int(ac)
        
        #Type assertions
        if type(name) != str:
            raise TypeError("Argument name must be a string.")
        if type(maxHP) != int:
            raise TypeError("Argument HP must be an integer.")
        if type(ac) != int:
            raise TypeError("Argument AC must be an integer.")
        
        #Value assestions
        if self.ac < 0:
            raise ValueError("Argument out of valid range. AC must be at least 0.")
        if self.maxHP < 1:
            raise ValueError("Argument out of valid range. HP must be at least 1.")
    
    def __str__(self):
        return self.name
    
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

#Implement menuPrint method
class Menu:
    def __init__(self, data, title = "menu"):
        self.title = title
        self.data = data
    
    def __str__(self):
        info = self.title.upper() + ":\n"
        if len(self.data) == 0:
            info += "EMPTY"
        else:
            for i in self.data[:-1]:
                info += str(self.data.index(i) + 1) + " " + str(i) + "\n"
            info += str(self.data.index(self.data[-1]) + 1) + " " + str(self.data[-1])
        return info

#TODO append option & import folder functionality
class load(Command):
    def __init__(self, nameList, bList):
        super().__init__(nameList)
        self.bList = bList
        self.description = "Replaces the default bestiary."
        self.usageStr = "load <file_name>"
    
    #Override execute
    def execute(self, args = []):
        if len(args) == 1:
            try:
                bestiaryFile = open(args[0])
            except FileNotFoundError:
                print("Selected bestiary file could not be found.")
                if len(self.bList) == 0:
                    print("Loading placeholder bestiary.")
                    human = NPC("Human", 5, 12)
                    animal = NPC("Animal", 3, 10)
                    enemy = NPC("Enemy", 10, 13)
                    self.bList.append(human)
                    self.bList.append(animal)
                    self.bList.append(enemy)
            else:
                self.bList.clear()
                for line in bestiaryFile:
                    if not line.startswith("#"):
                        line = line.rstrip("\n").split(",")
                        npc = NPC(line[0], int(line[1]), int(line[2]))
                        self.bList.append(npc)
                bestiaryFile.close()
                print("Bestiary loaded.")
        else:
            self.usage()

class displayHelp(Command):
    def __init__(self, nameList, commandList):
        super().__init__(nameList)
        self.commandList = commandList
        self.description = "Prints a list of availible commands."
        self.usageStr = "help [command_name]"
    
    #Override execute
    def execute(self, args = []):
        if len(args) == 1:
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
            if len(args) == 0:
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

#TODO clean up redundancy here
class displayMenu(Command):
    def __init__(self, nameList, bMenu, eMenu, gMenu):
        super().__init__(nameList)
        self.bMenu = bMenu
        self.eMenu = eMenu
        self.gMenu = gMenu
        self.description = "Prints all NPCs in a list."
        self.usageStr = "list [bestiary | encounter | combat | all]"
    
    #Override execute
    def execute(self, args = []):
        if len(args) == 1:
            if args[0] == "bestiary":
                print(self.bMenu)
            elif args[0] == "encounter":
                print(self.eMenu)
            elif args[0] == "graveyard":
                print(self.gMenu)
            elif args[0] == "combat":
                print(self.eMenu)
                print("")
                print(self.gMenu)
            elif args[0] == "all":
                print(self.bMenu)
                print("")
                print(self.eMenu)
                print("")
                print(self.gMenu)
            else:
                print(args[0] + " isn't a recognized list.")
        else:
            if len(args) == 0:
                print(self.bMenu)
                print("")
                print(self.eMenu)
                print("")
                print(self.gMenu)
            else:
                self.usage()

def isInt(string):
    if string.isnumeric():
        return True
    else:
        try:
            int(string)
        except:
            return False
        else:
            return True

def isValidInt(selector, npcList):
    valid = True
    for s in selector:
        if isInt(s) == False:
            valid = False
            break
    if valid == True:
        for s in selector:
            if int(s) > len(npcList) or int(s) <= 0:
                valid = False
                break
    if valid == False:
        print("One or more inputs are invalid in this context.")

    return valid

def npcCopy(bestiaryList, index, npcList):
    name = bestiaryList[int(index) - 1].name
    hp = bestiaryList[int(index) - 1].maxHP
    ac = bestiaryList[int(index) - 1].ac
    npc = NPC(name, hp, ac)
    npcList.append(npc)

#TODO make more generic
#TODO print who was added to what list
class addNPC(Command):
    def __init__(self, nameList, bList, eList, gList):
        super().__init__(nameList)
        self.bList = bList
        self.eList = eList
        self.gList = gList
        self.description = "Adds an NPC to a list. Defaults to the encounter list."
        self.usageStr = "add <bestiary_index,...> {encounter | graveyard}"
    
    #Override execute
    def execute(self, args = []):
        if len(args) == 2 or len(args) == 1:
            selected = args[0].split(",")
            valid = True
            for i in selected:
                if int(i) > len(self.bList) or int(i) <= 0:
                    valid = False
                    break
            if valid:
                if len(args) == 2:
                    if args[1] == "encounter":
                        for n in selected:
                            npcCopy(self.bList, n, self.eList)
                    elif args[1] == "graveyard":
                        for n in selected:
                            npcCopy(self.bList, n, self.gList)
                    else:
                        self.usage()
                elif len(args) == 1:
                    for n in selected:
                        npcCopy(self.bList, n, self.eList)
            else:
                print("One or more selected NPCs is outside of the range of your bestiary.")
        else:
            self.usage()

#TODO make more generic
#TODO setting to make no argument clear all
class clearNPCList(Command):
    def __init__(self, nameList, eList, gList):
        super().__init__(nameList)
        self.eList = eList
        self.gList = gList
        self.description = "Clears a list of NPCs."
        self.usageStr = "clear {all | encounter | graveyard}"
    
    #Override execute
    def execute(self, args = []):
        if len(args) == 1:
            npcList = args[0]
            if npcList == "all":
                self.eList.clear()
                self.gList.clear()
                print("Encounter and graveyard lists cleared.")
            elif npcList == "encounter":
                self.eList.clear()
                print("Encounter list cleared.")
            elif npcList == "graveyard":
                self.gList.clear()
                print("Graveyard list cleared.")
            else:
                print("Unknown list selected.")
        else:
            self.usage()

#TODO Could be made more generic with list and menu
#     (perhaps use a helper command?) for final implementation
class removeNPC(Command):
    def __init__(self, nameList, eList, gList, eMenu, gMenu):
        super().__init__(nameList)
        self.eList = eList
        self.gList = gList
        self.eMenu = eMenu
        self.gMenu = gMenu
        self.description = "Removes an NPC from a list."
        self.usageStr = "remove <bestiary_index,...> {encounter | graveyard}"
    
    #Override execute
    def execute(self, args = []):
        print("Remove")
        super().execute()

#TODO implement psuedocode
class reorder(Command):
    def __init__(self, nameList, eList, gList):
        super().__init__(nameList)
        self.eList = eList
        self.gList = gList
        self.description = "Switches the position of two NPCs."
    
    #Override execute
    def execute(self, args = []):
        print("Reorder")
        super().execute()

class attack(Command):
    def __init__(self, nameList, eList):
        super().__init__(nameList)
        self.eList = eList
        self.description = "Initiantiates D&D like combat with and NPC."
        self.usageStr = "attack <bestiary_index> [hit] [damage]"
    
    #Override execute
    def execute(self, args = []):
        print("Attack")
        super().execute()

#TODO Check dead helper command?
class damage(Command):
    def __init__(self, nameList, eList):
        super().__init__(nameList)
        self.eList = eList
        self.description = "Directly subtracts from an NPC's health."
        self.usageStr = "damage <bestiary_index>"
    
    #Override execute
    def execute(self, args = []):
        print("Damage")
        super().execute()

class smite(Command):
    def __init__(self, nameList, eList):
        super().__init__(nameList)
        self.eList = eList
        self.description = "Immediately kills an NPC."
        self.usageStr = "smite <bestiary_index>"
    
    #Override execute
    def execute(self, args = []):
        print("Smite")
        super().execute()

class heal(Command):
    def __init__(self, nameList, eList):
        super().__init__(nameList)
        self.eList = eList
        self.description = "Directly adds to an NPC's health."
        self.usageStr = "heal <bestiary_index> <amount>"
    
    #Override execute
    def execute(self, args = []):
        print("Heal")
        super().execute()

#TODO revive multiple NPCs at once
class revive(Command):
    def __init__(self, nameList, gList):
        super().__init__(nameList)
        self.gList = gList
        self.description = "Brings an NPC back from the graveyard."
        self.usageStr = "revive <graveyard_index>"
    
    #Override execute
    def execute(self, args = []):
        print("Revive")
        super().execute()

class debuff(Command):
    def __init__(self, nameList, eList):
        super().__init__(nameList)
        self.eList = eList
    
    #Override execute
    def execute(self, args = []):
        print("Debuff")
        super().execute()

class status(Command):
    def __init__(self, nameList, bList, eList, gList):
        super().__init__(nameList)
        self.bList = bList
        self.eList = eList
        self.gList = gList
        self.description = "Displays an NPC's current stats."
        self.usageStr = "status <index> {bestiary | encounter | graveyard}"
    
    #Override execute
    def execute(self, args = []):
        print("Status")
        super().execute()

def main():
    #Initiantiate reference lists
    bestiary = []
    encounter = []
    graveyard = []
    
    #Instantiate menus
    bestiaryMenu = Menu(bestiary, "bestiary")
    encounterMenu = Menu(encounter, "encounter")
    graveyardMenu = Menu(graveyard, "graveyard")
    
    #Instantiate commands
    commands = [
        load(['load'], bestiary),
        displayMenu(['list', 'display'], bestiaryMenu, encounterMenu, graveyardMenu),
        addNPC(['add'], bestiary, encounter, graveyard),
        clearNPCList(['clear'], encounter, graveyard),
        removeNPC(['remove', 'clear'], encounter, graveyard, encounterMenu, graveyardMenu),
        reorder(['reorder', 'arrange'], encounter, graveyard),
        attack(['attack'], encounter),
        damage(['damage'], encounter),
        smite(['smite', 'kill'], encounter),
        heal(['heal'], encounter),
        revive(['revive', 'resurrect', 'save'], graveyard),
        debuff(['debuff', 'change'], encounter),
        status(['status', 'info'], bestiary, encounter, graveyard)
        ]
    
    helpCommand =  displayHelp(['help', '?'], commands)
    commands.append(helpCommand)
    
    #Load default bestiary
    commands[0].execute(["bestiary.txt"])
    
    #print help message
    print("Type help or ? to get a list of availible commands.")
    
    #command loop
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