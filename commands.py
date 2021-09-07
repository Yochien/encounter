from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, nameList, numArgs, args = []):
        self.nameList = nameList
        self.numArgs = numArgs
        self.args = args
    
    def nameIs(self, name):
        for n in self.nameList:
            if name == n:
                return True
        return False
    
    @abstractmethod
    def execute(self):
        pass
        
class load(Command):
    def __init__(self, nameList, numArgs, bList, args = []):
        super().__init__(nameList, numArgs, args = [])
        self.bList = bList
    
    #Override execute
    def execute(self):
        print("load")

class displayHelp(Command):
    #Override execute
    def execute(self):
        print("Help")

class displayMenu(Command):
    def __init__(self, nameList, numArgs, bMenu, eMenu, gMenu, args = []):
        super().__init__(nameList, numArgs, args = [])
        self.bMenu = bMenu
        self.eMenu = eMenu
        self.gMenu = gMenu
    
    #Override execute
    def execute(self):
        print("displayMenu")

class addNPC(Command):
    def __init__(self, nameList, numArgs, bList, eList, gList, args = []):
        super().__init__(nameList, numArgs, args = [])
        self.bList = bList
        self.eList = eList
        self.gList = gList

    #Override execute
    def execute(self):
        print("add")

#TODO Could be made more generic with list and menu (perhaps use a helper command?)
class removeNPC(Command):
    def __init__(self, nameList, numArgs, eList, gList, eMenu, gMenu, args = []):
        super().__init__(nameList, numArgs, args = [])
        self.eList = eList
        self.gList = gList
        self.eMenu = eMenu
        self.gMenu = gMenu

    #Override execute
    def execute(self):
        print("remove")

class reorder(Command):
    def __init__(self, nameList, numArgs, eList, gList, args = []):
        super().__init__(nameList, numArgs, args = [])
        self.eList = eList
        self.gList = gList
    
    #Override execute
    def execute(self):
        print("reorder")

class attack(Command):
    def __init__(self, nameList, numArgs, eList, args = []):
        super().__init__(nameList, numArgs, args = [])
        self.eList = eList
    
    #Override execute
    def execute(self):
        print("attack")

#TODO Check dead helper command?
class damage(Command):
    def __init__(self, nameList, numArgs, eList, args = []):
        super().__init__(nameList, numArgs, args = [])
        self.eList = eList
    
    #Override execute
    def execute(self):
        print("damage")

class smite(Command):
    def __init__(self, nameList, numArgs, eList, args = []):
        super().__init__(nameList, numArgs, args = [])
        self.eList = eList
    
    #Override execute
    def execute(self):
        print("smite")

class heal(Command):
    def __init__(self, nameList, numArgs, eList, args = []):
        super().__init__(nameList, numArgs, args = [])
        self.eList = eList
    
    #Override execute
    def execute(self):
        print("heal")

class revive(Command):
    def __init__(self, nameList, numArgs, gList, args = []):
        super().__init__(nameList, numArgs, args = [])
        self.gList = gList
    
    #Override execute
    def execute(self):
        print("revive")

class debuff(Command):
    def __init__(self, nameList, numArgs, eList, args = []):
        super().__init__(nameList, numArgs, args = [])
        self.eList = eList
    
    #Override execute
    def execute(self):
        print("debuff")

class status(Command):
    def __init__(self, nameList, numArgs, bList, eList, gList, args = []):
        super().__init__(nameList, numArgs, args = [])
        self.bList = bList
        self.eList = eList
        self.gList = gList
    
    #Override execute
    def execute(self):
        print("status")

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
    
    def setData(self, data):
        self.data = data
    
    def getData(self):
        return self.data
    
    def setTitle(self, title):
        self.title = title
    
    def getTitle(self):
        return self.title
    
    def toString(self):
        info = self.title.upper() + ":\n"
        if len(self.data) == 0:
            info += "EMPTY"
        else:
            for i in self.data[:-1]:
                info += str(self.data.index(i) + 1) + " " + str(i) + "\n"
            info += str(self.data.index(self.data[-1]) + 1) + " " + str(self.data[-1])
        return info

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
        displayHelp(['help', '?'], 0),
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
    
    #print help message
    print("Type help or ? to get a list of availible commands.")
    
    #command loop
    loop = True
    while loop:
        action = input("Type a command: ").lower().split(" ")
        
        command = None
        
        if action != ['']:
            command = action[0]
        
        if command == "quit" or command == "q" or command == "exit":
            break
        
        found = False
        for c in commands:
            if c.nameIs(command):
                c.execute()
                found = True
                break
        
        if not found:
            print("Unrecognized command.")
            print("Type help or ? to learn how to use availible commands.")

if __name__ == "__main__":
    main()