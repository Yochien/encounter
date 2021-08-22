class NPC:
    def __init__(self, name, maxHP, ac):
        self.name = name
        self.maxHP = self.currentHP = int(maxHP)
        self.ac = int(ac)
    
        if self.ac < 0 or self.maxHP < 1:
            raise Exception("Attribute out of valid range.")
    
    def toString(self):
        info = ""
        info += "NAME: "
        info += str(self.name)
        info += "\n"
        info += "HP: "
        info += str(self.currentHP)
        info += "\n"
        info += "AC: "
        info += str(self.ac)
        return info
    
    def damage(self, amt):
        self.currentHP -= int(amt)

#NPC lists
bestiary = []
encounter = []
graveyard = []

def load(args):
    if len(args) > 0:
        bestiary.clear()
        try:
            bestiaryFile = open(args[0])
        except FileNotFoundError:
            print("Selected bestiary file could not be found. \n Loading placeholder bestiary.")
            human = NPC("Human", 5, 12)
            animal = NPC("Animal", 3, 10)
            enemy = NPC("Enemy", 10, 13)
            bestiary.append(human)
            bestiary.append(animal)
            bestiary.append(enemy)
        else:
            for line in bestiaryFile:
                if not line.startswith("#"):
                    line = line.rstrip("\n").split(",")
                    npc = NPC(line[0], line[1], line[2])
                    bestiary.append(npc)
            bestiaryFile.close()
    else:
        print("load requires at least one argument.")

def displayHelp():
    try:
        helpFile = open("usage.md")
    except FileNotFoundError:
        print("\"usage.md\" could not be found.")
    else:
        print(helpFile.read())
        helpFile.close()

###############################################################################################
###         All functions should allow you to use the name of an NPC as a selector.         ###
###If more than one of a particular NPC type exists encounter should ask for clarification. ###
###############################################################################################

def menu(npcList, title = "MENU:"): #Should be rewritten to be more robust displaying menus for more types of functions
    title = title.upper() + ":"
    print(title)

    c = 0
    if len(npcList) > 0:
        for m in npcList:
            c += 1
            print(str(c) + " " + m.name)
    else:
        print("EMPTY")

def displayList(args):
    if len(args) == 0:
        menu(bestiary, "bestiary")
        print("")
        menu(encounter, "encounter")
        print("")
        menu(graveyard, "graveyard")
    else:
        if args[0] == "bestiary":
            menu(bestiary, "bestiary")
        elif args[0] == "encounter":
            menu(encounter, "encounter")
        elif args[0] == "graveyard":
            menu(graveyard, "graveyard")
        elif args[0] == "combat":
            menu(encounter, "encounter")
            print("")
            menu(graveyard, "graveyard")
        elif args[0] == "all":
            menu(bestiary, "bestiary")
            print("")
            menu(encounter, "encounter")
            print("")
            menu(graveyard, "graveyard")
        else:
            print("Unknown list selected.")

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

#Default should add to encounter list
def add(args):
    if len(args) < 2:
        print("Command requires two arguments")
    else:
        selected = args[0].split(",")
        skip = False
        for n in selected:
            if int(n) > len(bestiary) or int(n) <= 0:
                skip = True
        if skip == True:
            print("One or more selected NPCs is outside the range of the bestiary.")
        else:
            for m in selected:
                name = bestiary[int(m) - 1].name
                hp = bestiary[int(m) - 1].maxHP
                ac = bestiary[int(m) - 1].ac
                npc = NPC(name, hp, ac)
                if args[1] == "encounter":
                    encounter.append(npc)
                elif args[1] == "graveyard":
                    graveyard.append(npc)
            if args[1] == "encounter":
                menu(encounter, "encounter")
            elif args[1] == "graveyard":
                menu(graveyard, "graveyard")
            else:
                print("Referenced an unknown list.")

def info(args):
    if len(args) >= 2:
        if isInt(args[0]):
            if args[1] == "bestiary":
                if isValidInt(args[0], bestiary) == True:     #Could be broken into a sub command that could take a list as an argument and be reused here
                    print("INFO:")
                    print(bestiary[int(args[0])-1].toString())
            elif args[1] == "encounter":
                if isValidInt(args[0], encounter) == True:
                    print("INFO:")
                    print(encounter[int(args[0])-1].toString())
            elif args[1] == "graveyard":
                if isValidInt(args[0], graveyard) == True:
                    print("INFO:")
                    print(graveyard[int(args[0])-1].toString())
            else:
                print("Unrecognized list")
        else:
            print("First argument must be a valid integer")
    else:
        print("info requires 2 arguments")

def delete(selector, npcList):
    count = 0
    skip = False
    length = len(npcList)

    for s in selector:
        if int(s) > length or int(s) < 0:
            skip = True
            break
    if skip == False:
        for s in selector:
            npcList[int(s) - 1] = None
            count += 1
        
        count = 0
        while count < length:
            if npcList[count] == None:
                npcList.pop(count)
                length -= 1
            count += 1
    else:
        print("One or more numbers out of range of availible NPCs.")

def remove(args):
    if len(args) < 2:
        print("remove requires at least two arguments.")
    else:
        if args[0] == "all":
            if args[1] == "all":
                encounter.clear()
                graveyard.clear()
                menu(encounter, "encounter")
                menu(graveyard, "graveyard")
            elif args[1] == "encounter":
                encounter.clear()
                menu(encounter, "encounter")
            elif args[1] == "graveyard":
                graveyard.clear()
                menu(graveyard, "graveyard")
        else:
            selected = args[0].split(",")
            
            if args[1] == "encounter":
                if len(encounter) > 0:
                    delete(selected, encounter)
                menu(encounter, "encounter")
            elif args[1] == "graveyard":
                if len(graveyard) > 0:
                    delete(selected, graveyard)
                menu(graveyard, "graveyard")
            else:
                print("Unknown list selected.")

def attack(args): #for n in selector attack(n)
    npc = None

    if len(args) >= 1:
        if isValidInt(args[0], encounter) == True:
            npc = encounter[int(args[0]) - 1]
            if npc.currentHP > 0:
                if len(args) >= 2:
                    if args[0].isnumeric() == True:
                        accuracy = int(args[1])
                        if accuracy >= npc.ac:
                            if len(args) >= 3:
                                if args[2].isnumeric() == True:
                                    npc.damage(args[2])
                                    print(npc.name + " took " + args[2] + " damage.")
                                else:
                                    print("Damage must be a number.")
                            else:
                                damage = input("Roll for damage: ")
                                if damage.isnumeric() == True:
                                    amt = int(damage)
                                    npc.damage(amt)
                                    print(npc.name + " took " + damage + " damage.")
                                else:
                                    print("Damage must be a number.")
                        else:
                            print("Attack misses " + npc.name + ".")
                    else:
                        print("Accuracy must be a number.")
                else:
                    accuracy = input("Roll for hit: ")
                    if accuracy.isnumeric() == True:
                        accuracy = int(accuracy)
                        if accuracy >= npc.ac:
                            damage = input("Roll for damage: ")
                            if damage.isnumeric() == True:
                                amt = int(damage)
                                npc.damage(amt)
                                print(npc.name + " took " + damage + " damage.")
                            else:
                                print("Damage must be a number.")
                        else:
                            print("Attack misses " + npc.name + ".")
                    else:
                        print("Accuracy must be a number.")
            else:
                print("That NPC is already dead!")
        else:
            print("Selected an invalid NPC.")
    else:
        print("attack requires at least one argument.")
    
    if npc != None:
        if npc.currentHP <= 0:
            print(npc.name + " has been defeated.")
            graveyard.append(npc)
            encounter.pop(int(args[0]) - 1)
            if len(encounter) == 0:
                print("Party has defeated all enemies.")

def damage(args):
    if len(args) >= 2:
        if isValidInt(args[0], encounter) == True:
            npc = encounter[int(args[0]) - 1]
            npc.damage(args[1])
            if npc.currentHP <= 0:
                print(npc.name + " has been defeated.")
                graveyard.append(npc)
                encounter.pop(int(args[0]) - 1)
                if len(encounter) == 0:
                    print("Party has defeated all enemies.")
        else:
            print("Selected an invalid NPC.")
    else:
        print("damage requires 2 or more arguments")

def smite(args):
    if len(args) > 0:
        global graveyard #Is this necessary?
        if args[0] == "all":
            graveyard = graveyard + encounter
            encounter.clear()
            print("All NPCs were smitten.")
        else:
            if args[0].isnumeric():
                selector = int(args[0])
                if selector <= len(encounter) and selector > 0:
                    print(encounter[int(selector) - 1].name + " has been defeated.")
                    graveyard.append(encounter[int(selector) - 1])
                    encounter.pop(int(selector) - 1)
                    
                    if len(encounter) == 0:                                         #Should create a check if encounter defeated function
                        print("Party has defeated all enemies.")
                else:
                    print("Selected an invalid NPC.")
            else:
                print("Expected \"all\" or a positive number.")
    else:
        print("smite requires 1 argument.")
        
def heal(args): #Should allow for negative healing I.E. harm undead
    if len(args) >= 1:
        if args[0].isnumeric() == True:
            if isValidInt(args[0], encounter) == True:
                npc = encounter[int(args[0]) - 1]
                if len(args) >= 2:
                    if args[1].isnumeric() == True:
                        amt = int(args[1])
                        npc.currentHP += amt
                        if npc.currentHP > npc.maxHP: npc.currentHP = npc.maxHP
                        print(npc.name + " was healed by " + str(amt) + " points.") #Should display amount restored rather than amount input
                    else:
                        print("Amount must be a number.")
                else:
                    amt = input("Amount to heal: ")
                    if amt.isnumeric() == True:
                        amt = int(amt)
                        npc.currentHP += amt
                        if npc.currentHP > npc.maxHP: npc.currentHP = npc.maxHP
                        print(npc.name + " was healed by " + str(amt) + " points.")
                    else:
                        print("Amount must be a number.")
            else:
                print("Selected an invalid monster.")
        else:
            print("Expected a number.")
    else:
        print("heal requires one argument.")

def revive(args):
    if len(graveyard) > 0:
        if len(args) > 0:
            if len(graveyard) >= int(args[0]) and int(args[0]) > 0:
                encounter.append(graveyard[int(args[0]) - 1])
                graveyard.pop(int(args[0]) - 1)
                print(encounter[-1].name + " has been revived.")
            else:
                print("Selected an invalid NPC. Check you graveyard.")
        else:
            print("revive requires one argument.")
    else:
        print("Graveyard is empty. There is no one to revive.")
                    #Should be changed to a generic change command that takes an argument for a particular stat
                    #Should be valid for dead or alive NPCs or even the bestiary
def changeAC(args): #Should allow one to set stat to a specific value, or change by positive or negative values
    if len(args) > 0:
        if isValidInt(args[0], encounter) == True:
            npc = encounter[int(args[0]) - 1]
            if len(args) >= 2:
                if args[1].isnumeric() == True:
                    amt = int(args[1])
                    npc.ac += amt
                    if npc.ac < 0: npc.ac = 0
                    print(npc.name + "'s armor class was changed by " + str(amt) + ".")
            else:
                amt = input("Amount to change by: ")
                if amt.isnumeric() == True:
                    amt = int(amt)
                    npc.ac += amt
                    if npc.ac < 0: npc.ac = 0
                    print(npc.name + "'s armor class was changed by " + str(amt) + ".")
                else:
                    print("Amount must be a number.")
        else:
            print("Selected an invalid monster.")
    else:
        print("change-ac requires at least 1 argument.")

    '''
def changeAC(npc, amount): 
    npc.ac += amount
    if npc.ac < 0: npc.ac = 0
    print(npc.name + "'s armor class was changed by " + str(amount) + ".")
    '''

load(['bestiary.txt'])
    
print("Type help or ? to get a list of availible commands.")
wait = True
while wait:
    action = input("Type an action to perform: ").lower().split(" ")
    
    if action != ['']:
        command = action[0]
    else:
        command = None
    
    args = []
    
    if (len(action) > 1):
        count = 1
        while count < len(action):
            args.append(action[count])
            count += 1
    
    if command == "help" or command == "?":
        displayHelp()
    elif command == "list":
        displayList(args)
    elif command == "add":
        add(args)
    elif command == "revive" or command == "resurrect" or command == "save":
        revive(args)
    elif command == "remove" or command == "clear":
        remove(args)
    elif command == "info" or command == "status":
        info(args)
    elif command == "attack":
        attack(args)
    elif command == "damage":
        damage(args)
    elif command == "kill" or command == "smite":
        smite(args)
    elif command == "heal":
        heal(args)
    elif command == "changeac":
        changeAC(args)
    elif command == "load":
        load(args)
    elif command == "quit" or command == "q" or command == "exit":
        wait = False
    else:
        print("Unrecognized command.")
        print("Type help or ? to learn how to use availible commands.")