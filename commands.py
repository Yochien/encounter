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
        #Type assertions
        if type(name) != str:
            raise TypeError("Argument name must be a string.")
        if type(maxHP) != int:
            raise TypeError("Argument HP must be an integer.")
        if type(ac) != int:
            raise TypeError("Argument AC must be an integer.")
        
        #Value assestions
        if ac < 0:
            raise ValueError("Argument out of valid range. AC must be at least 0.")
        if maxHP < 1:
            raise ValueError("Argument out of valid range. HP must be at least 1.")
        
        #Value assignment
        self.name = name
        self.maxHP = self.currentHP = maxHP
        self.ac = int(ac)
    
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

class NPCList:
    def __init__(self, nameList, tags, data):
        #Error Checking
        if type(nameList) != list:
            raise TypeError("Argument nameList must be a list of strings.")
        if type(tags) != list:
            raise TypeError("Argument tags must be a list of strings.")
        if type(data) != list:
            raise TypeError("Argument data must be a list of NPCs.")

        if len(nameList) == 0:
            raise ValueError("Argument nameList must contain at least one entry.")
        
        #Value assignment
        self.nameList = nameList
        self.name = nameList[0]
        self.tags = tags
        self.data = data

    def toMenu(self):
        info = self.name.upper() + ":\n"
        
        if len(self.data) == 0:
            info += "EMPTY"
        else:
            for i in self.data[:-1]:
                info += str(self.data.index(i) + 1) + " " + str(i) + "\n"
            info += str(self.data.index(self.data[-1]) + 1) + " " + str(self.data[-1])
        return info

#TODO append option & import folder functionality
class load(Command):
    def __init__(self, nameList, bestiary):
        super().__init__(nameList)
        self.bestiary = bestiary
        self.description = "Replaces the default bestiary."
        self.usageStr = "load <file_name>"
    
    #Override execute
    def execute(self, args = []):
        numArgs = len(args)
        
        if numArgs == 1:
            try:
                bestiaryFile = open(args[0])
            except FileNotFoundError:
                print("Selected bestiary file could not be found.")
                if len(self.bestiary.data) == 0:
                    print("Loading placeholder bestiary.")
                    human = NPC("Human", 5, 12)
                    animal = NPC("Animal", 3, 10)
                    enemy = NPC("Enemy", 10, 13)
                    self.bestiary.data.append(human)
                    self.bestiary.data.append(animal)
                    self.bestiary.data.append(enemy)
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
    def __init__(self, nameList, commandList):
        super().__init__(nameList)
        self.commandList = commandList
        self.description = "Prints a list of availible commands."
        self.usageStr = "help [command_name]"
    
    #Override execute
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
    def __init__(self, nameList, referenceLists):
        super().__init__(nameList)
        self.referenceLists = referenceLists
        self.description = "Prints all NPCs in a list."
        self.usageStr = "list [bestiary | encounter | combat | graveyard | all]"
    
    #Override execute
    def execute(self, args = []):
        numArgs = len(args)
        
        if numArgs == 1 and args[0] != "all":
            found = False
            
            for l in self.referenceLists:
                if args[0] in l.nameList or args[0] in l.tags:
                    found = True
                    print(l.toMenu())
                    print("")
            
            if not found:
                print("Unknown list selected.")
        else:
            if numArgs == 0 or args[0] == "all":
                for l in self.referenceLists:
                    print(l.toMenu())
                    print("")
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

class addNPC(Command):
    def __init__(self, nameList, referenceLists):
        super().__init__(nameList)
        self.referenceLists = referenceLists
        self.description = "Adds an NPC to a list. Defaults to the encounter list."
        self.usageStr = "add <bestiary_index,...> {encounter | graveyard}"
    
    #Override execute
    def execute(self, args = []):
        numArgs = len(args)
        bestiary = self.referenceLists[0].data
        
        if numArgs == 2 or numArgs == 1:
            selected = args[0].split(",")
            valid = True
            #Check if the selector is made of all integers
            for i in selected:
                if not isInt(i):
                    valid = False
            
            #Check if selectors are within range of the bestiary
            if valid:
                for i in selected:
                    if int(i) > len(bestiary) or int(i) <= 0:
                        valid = False
                        break
            
            #If all above checks are passed, then execute logic
            if valid:
                if numArgs == 2 and args[1].lower() not in self.referenceLists[0].nameList:
                    for l in self.referenceLists:
                        if args[1] in l.nameList:
                            for n in selected:
                                npcCopy(bestiary, n, l.data)
                            print(l.toMenu())
                            print("")
                elif numArgs == 1:
                    for n in selected:
                        npcCopy(bestiary, n, self.referenceLists[1].data)
                    print(self.referenceLists[1].toMenu())
                    print("")
            else:
                self.usage()
        else:
            self.usage()

#TODO setting to make no argument clear all
class clearNPCList(Command):
    def __init__(self, nameList, referenceLists):
        super().__init__(nameList)
        self.referenceLists = referenceLists
        self.description = "Clears a list of NPCs."
        self.usageStr = "clear {all | encounter | graveyard}"
    
    #Override execute
    def execute(self, args = []):
        lenArgs = len(args)
        
        if lenArgs == 1:
            if args[0] not in self.referenceLists[0].nameList:
                if args[0].lower() == "all":
                    for l in self.referenceLists:
                        if l != self.referenceLists[0]:
                            l.data.clear()
                            print(l.toMenu())
                            print("")
                else:
                    found = False
                    for l in self.referenceLists:
                        if args[0] in l.nameList or args[0] in l.tags:
                            found = True
                            l.data.clear()
                            print(l.toMenu())
                            print("")
                    if not found:
                        print("Unknown list selected.")
            else:
                self.usage()
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

class damage(Command):
    def __init__(self, nameList, referenceLists):
        super().__init__(nameList)
        self.referenceLists = referenceLists
        self.description = "Directly subtracts from an NPC's health."
        self.usageStr = "damage <encounter_index> <amount>"
    
    #Override execute
    def execute(self, args = []):
        encounter = self.referenceLists[1].data
        lenArgs = len(args)
        
        if lenArgs == 2:
            if isValidInt(args[0], encounter) == True:
                npc = encounter[int(args[0]) - 1]
                npc.currentHP = npc.currentHP - int(args[1])
                if npc.currentHP <= 0:
                    print(npc.name + " has been defeated.")
                    referenceLists[2].data.append(npc)
                    encounter.pop(int(args[0]) - 1)
                    if len(encounter) == 0:
                        print("Party has defeated all enemies.")
        else:
            self.usage()

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
    def __init__(self, nameList, referenceLists):
        super().__init__(nameList)
        self.referenceLists = referenceLists
        self.description = "Directly adds to an NPC's health."
        self.usageStr = "heal <encounter_index> <amount>"
    
    #Override execute
    def execute(self, args = []):
        encounter = self.referenceLists[1].data
        lenArgs = len(args)
        
        if lenArgs == 2:
            if isValidInt(args[0], encounter) == True:
                npc = encounter[int(args[0]) - 1]
                
                origHP = npc.currentHP
                
                npc.currentHP = npc.currentHP + int(args[1])
                if npc.currentHP > npc.maxHP:
                    npc.currentHP = npc.maxHP
                
                healedAmt = npc.currentHP - origHP
                
                print(npc.name + " was healed by " + str(healedAmt) + " points.")
        else:
            self.usage()

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
    def __init__(self, nameList, referenceLists):
        super().__init__(nameList)
        self.referenceLists = referenceLists
    
    #Override execute
    def execute(self, args = []):
        print("Debuff")
        super().execute()

class status(Command):
    def __init__(self, nameList, referenceLists):
        super().__init__(nameList)
        self.referenceLists = referenceLists
        self.description = "Displays an NPC's current stats."
        self.usageStr = "status <index> {encounter | graveyard}"
    
    #Override execute
    def execute(self, args = []):
        lenArgs = len(args)
        if lenArgs == 2:
            if isInt(args[0]):
                found = False
                for l in self.referenceLists:
                    #TODO better error reporting here. currently ambiguous
                    if args[1].lower() not in self.referenceLists[0].nameList and args[1] in l.nameList:
                        found = True
                        if isValidInt([args[0]], l.data):
                            print("Status:")
                            print(l.data[int(args[0]) - 1].name + " " + "[" + str(l.data[int(args[0]) - 1].currentHP) + " / " + str(l.data[int(args[0]) - 1].maxHP) + "]")
                            break
                        else:
                            self.usage
                if not found:
                    print("Unknown list selected.")
            else:
                self.usage()
        else:
            self.usage()

class info(Command):
    def __init__(self, nameList, referenceLists):
        super().__init__(nameList)
        self.referenceLists = referenceLists
        self.description = "Displays an NPC's detailed stats."
        self.usageStr = "info <index> {bestiary | encounter | graveyard}"

    #Override execute
    def execute(self, args = []):
        lenArgs = len(args)
        if lenArgs == 2:
            if isInt(args[0]):
                found = False
                for l in self.referenceLists:
                    if args[1] in l.nameList:
                        found = True
                        if isValidInt([args[0]], l.data):
                            print("INFO:")
                            print("NAME: " + l.data[int(args[0]) - 1].name)
                            print("HP: " + str(l.data[int(args[0]) - 1].currentHP))
                            print("MAX HP: " + str(l.data[int(args[0]) - 1].maxHP))
                            print("AC: " + str(l.data[int(args[0]) - 1].ac))
                            break
                        else:
                            self.usage
                if not found:
                    print("Unknown list selected.")
            else:
                self.usage()
        else:
            self.usage()

def main():
    referenceLists = [
        NPCList(['bestiary', 'book', 'b'], [], []),
        NPCList(['encounter', 'e'], ['combat'], []),
        NPCList(['graveyard', 'g'], ['combat'], [])
        ]
    
    bestiary = referenceLists[0]
    
    #Instantiate commands
    commands = [
        load(['load'], bestiary),
        displayMenu(['list', 'display'], referenceLists),
        addNPC(['add'], referenceLists),
        clearNPCList(['clear'], referenceLists),
        damage(['damage'], referenceLists),
        debuff(['debuff', 'change'], referenceLists),
        heal(['heal'], referenceLists),
        status(['status'], referenceLists),
        info(['info'], referenceLists)
        ]
    '''
    removeNPC(['remove', 'clear'], referenceLists),
    attack(['attack'], referenceLists),
    smite(['smite', 'kill'], referenceLists),
    revive(['revive', 'resurrect', 'save'], referenceLists),
    '''
    
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
        
        #TODO Check for deaths in encounter list. Display message and move to graveyard
        
if __name__ == "__main__":
    main()