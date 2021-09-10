from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, nameList, numArgs):
        self.nameList = nameList
        self.numArgs = numArgs
        self.description = "This Command has no defined description yet."
        self.usageStr = "This Command has no defined usage yet."
    
    def usage(self):
        print("Usage: " + self.usageStr)
    
    @abstractmethod
    def execute(self):
        print("This Command has not been implemented yet.")

class Menu:
    def __init__(self, data, title = "menu"):
        self.title = title
        self.data = data
    
    def equals(self, other):
        if self == other:
            return True
        if other is None:
            return False
        if self.data != other.data:
            return False
        if self.title != other.title:
            return False
        return True
    
    def toString(self):
        info = self.title.upper() + ":\n"
        if len(self.data) == 0:
            info += "EMPTY"
        else:
            for i in self.data[:-1]:
                info += str(self.data.index(i) + 1) + " " + str(i) + "\n"
            info += str(self.data.index(self.data[-1]) + 1) + " " + str(self.data[-1])
        return info

class load(Command):
    def __init__(self, nameList, numArgs, bList):
        super().__init__(nameList, numArgs)
        self.bList = bList
        self.description = "Replaces the default bestiary."
        self.usageStr = "load <file_name>"
    
    #Override execute
    def execute(self, args = []):
        print("Load")
        super().execute()

class displayHelp(Command):
    def __init__(self, nameList, numArgs, commandList):
        super().__init__(nameList, numArgs)
        self.commandList = commandList
        self.description = "Prints a list of availible commands."
        self.usageStr = "help [command_name]"
    
    #Override execute
    def execute(self, args = []):
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
        elif args[0].lower() in ["quit", "q", "exit"]:
            print("Exits the program.")
            print("Usage: {quit | q | exit}")
        elif len(args) == self.numArgs:
            found = False
            for command in self.commandList:
                if command.nameIs(args[0].lower()):
                    print(command.description)
                    command.usage()
                    found = True
                    break
            
            if not found:
                print("Unrecognized command.")
                print("Type help or ? to learn how to use availible commands.")
        else:
            self.usage()

#TODO clean up redundancy here
class displayMenu(Command):
    def __init__(self, nameList, numArgs, bMenu, eMenu, gMenu):
        super().__init__(nameList, numArgs)
        self.bMenu = bMenu
        self.eMenu = eMenu
        self.gMenu = gMenu
        self.description = "Prints all NPCs in a list."
        self.usageStr = "list [bestiary | encounter | combat | all]"
    
    #Override execute
    def execute(self, args = []):
        if len(args) == 0:
            print(self.bMenu.toString() + "\n")
            print(self.eMenu.toString() + "\n")
            print(self.gMenu.toString())
        elif len(args) == self.numArgs:
            if args[0] == "bestiary":
                print(self.bMenu.toString())
            elif args[0] == "encounter":
                print(self.eMenu.toString())
            elif args[0] == "graveyard":
                print(self.gMenu.toString())
            elif args[0] == "combat":
                print(self.eMenu.toString() + "\n")
                print(self.gMenu.toString())
            elif args[0] == "all":
                print(self.bMenu.toString() + "\n")
                print(self.eMenu.toString() + "\n")
                print(self.gMenu.toString())
            else:
                print(args[0] + " isn't a recognized list.")
        else:
            self.usage()

class addNPC(Command):
    def __init__(self, nameList, numArgs, bList, eList, gList):
        super().__init__(nameList, numArgs)
        self.bList = bList
        self.eList = eList
        self.gList = gList
        self.description = "Adds an NPC to a list."
        self.usageStr = "add <bestiary_index,...> {encounter | graveyard}"
    
    #Override execute
    def execute(self, args = []):
        print("Add")
        super().execute()

#TODO Could be made more generic with list and menu
#     (perhaps use a helper command?) for final implementation
class removeNPC(Command):
    def __init__(self, nameList, numArgs, eList, gList, eMenu, gMenu):
        super().__init__(nameList, numArgs)
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
    def __init__(self, nameList, numArgs, eList, gList):
        super().__init__(nameList, numArgs)
        self.eList = eList
        self.gList = gList
        self.description = "Switches the position of two NPCs."
    
    #Override execute
    def execute(self, args = []):
        print("Reorder")
        super().execute()

class attack(Command):
    def __init__(self, nameList, numArgs, eList):
        super().__init__(nameList, numArgs)
        self.eList = eList
        self.description = "Initiantiates D&D like combat with and NPC."
        self.usageStr = "attack <bestiary_index> [hit] [damage]"
    
    #Override execute
    def execute(self, args = []):
        print("Attack")
        super().execute()

#TODO Check dead helper command?
class damage(Command):
    def __init__(self, nameList, numArgs, eList):
        super().__init__(nameList, numArgs)
        self.eList = eList
        self.description = "Directly subtracts from an NPC's health."
        self.usageStr = "damage <bestiary_index>"
    
    #Override execute
    def execute(self, args = []):
        print("Damage")
        super().execute()

class smite(Command):
    def __init__(self, nameList, numArgs, eList):
        super().__init__(nameList, numArgs)
        self.eList = eList
        self.description = "Immediately kills an NPC."
        self.usageStr = "smite <bestiary_index>"
    
    #Override execute
    def execute(self, args = []):
        print("Smite")
        super().execute()

class heal(Command):
    def __init__(self, nameList, numArgs, eList):
        super().__init__(nameList, numArgs)
        self.eList = eList
        self.description = "Directly adds to an NPC's health."
        self.usageStr = "heal <bestiary_index> <amount>"
    
    #Override execute
    def execute(self, args = []):
        print("Heal")
        super().execute()

#TODO revive multiple NPCs at once
class revive(Command):
    def __init__(self, nameList, numArgs, gList):
        super().__init__(nameList, numArgs)
        self.gList = gList
        self.description = "Brings an NPC back from the graveyard."
        self.usageStr = "revive <graveyard_index>"
    
    #Override execute
    def execute(self, args = []):
        print("Revive")
        super().execute()

class debuff(Command):
    def __init__(self, nameList, numArgs, eList):
        super().__init__(nameList, numArgs)
        self.eList = eList
    
    #Override execute
    def execute(self, args = []):
        print("Debuff")
        super().execute()

class status(Command):
    def __init__(self, nameList, numArgs, bList, eList, gList):
        super().__init__(nameList, numArgs)
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
        load(['load'], 1, bestiary),
        displayMenu(['list', 'display'], 1, bestiaryMenu, encounterMenu, graveyardMenu),
        addNPC(['add'], 2, bestiary, encounter, graveyard),
        removeNPC(['remove', 'clear'], 2, encounter, graveyard, encounterMenu, graveyardMenu),
        reorder(['reorder', 'arrange'], 3, encounter, graveyard),
        attack(['attack'], 1, encounter),
        damage(['damage'], 1, encounter),
        smite(['smite', 'kill'], 1, encounter),
        heal(['heal'], 1, encounter),
        revive(['revive', 'resurrect', 'save'], 1, graveyard),
        debuff(['debuff', 'change'], 3, encounter),
        status(['status', 'info'], 2, bestiary, encounter, graveyard)
        ]
    
    helpCommand =  displayHelp(['help', '?'], 1, commands)
    commands.append(helpCommand)
    
    #print help message
    print("Type help or ? to get a list of availible commands.")
    
    #command loop
    loop = True
    while loop:
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
                #command.usage()
                command.execute(args)
                found = True
                break
        
        if not found:
            print("Unrecognized command.")
            print("Type help or ? to learn how to use availible commands.")

if __name__ == "__main__":
    main()