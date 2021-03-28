class NPC:
    def __init__(self, name, maxHP, ac):
        self.name = name
        self.maxHP = self.currentHP = int(maxHP)
        self.ac = int(ac)
    
    def status(self):
        print("STATUS:")
        print("Name: " + self.name)
        print("HP: " + str(self.currentHP))
        print("AC: " + str(self.ac))
        
    def damage(self, amt):
        self.currentHP -= int(amt)

#NPC lists
bestiary = []
encounter = []
graveyard = []

#Attempt to open the bestiary file. If not found fallback on a default set of NPCs
try:
    with open("bestiary.txt") as book:
        for line in book:
            if not line.startswith("#"):
                line = line.rstrip("\n").split(",")
                npc = NPC(line[0], line[1], line[2])
                bestiary.append(npc)
except FileNotFoundError:
    human = NPC("Human", 5, 12)
    animal = NPC("Animal", 3, 10)
    enemy = NPC("Enemy", 10, 13)
    bestiary.append(human)
    bestiary.append(animal)
    bestiary.append(enemy)

def displayHelp():
    print(
'''
# help or ?
* prints this premade list of commands that you can use to interact with your list of NPCs.
# quit or or q or exit
* exits the program.
# list [str]
* if [str] is bestiary the function will print a list of availible NPCs to add to your encounter.
* if [str] is encounter the function will print the NPCs in your current encounter.
* if [str] is graveyard the function will list the currently defeated NPCs in your encounter.
* if [str] is left blank the bestiary will be shown with a message explaining how to select a particular list.
# add [num1,num2,num3,...] [list]
* populates the encounter list with your selected NPCs in the list [str].
* [list] can either be encounter or graveyard.
# remove [num1,num2,etc... or str] [list]
* removes NPCs at positions [num1,num2,etc...] from [list].
* list can either be encounter or graveyard.
* duplicate numbers in list [nums] will be ignored.
* setting [str] to all will clear the selected list in [list].
* setting [str] to all and [list] to all will clear all lists of all NPCs.
* providing no list after [str] =  all will do the same as remove all all.
# revive or resurrect [num]
* revives the NPCs in position [num] in the graveyard list.
**The following commands require a non empty encounter**
# status [num]
* prints an NPC's [num]'s name and the amount of hp they have left from the encounter list.
# attack [num]
* attacks an NPC's from the encounter list at the position [num].
# smite or kill
* instantly sends an NPC to the graveyard.
# heal [num1] [num2]
* heals an NPC at position [num1] in the encounter list by [num2] amount of health points.
* won't raise currentHP above their maxHP.
# change-ac [num1] [num2]
* adds [num2] to an NPC's armor class at position [num1] in  the encounter list. An NPC's armor class cannot fall below 0.
**END**
'''
    )

###############################################################################################
###All functions should allow you to use the name of an NPC as a selector.                  ###
###If more than one of a particular NPC type exists encounter should ask which one you mean.###
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

def isValidInt(selector, npcList):
    valid = True
    for s in selector:
        if s.isnumeric() == False:
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
                    delete(selector, graveyard)
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
        
def heal(args): #Should allow for negative healing
    if len(args) >= 1:
        if args[0].isnumeric() == True:
            if isValidInt(args[0], encounter) == True:
                npc = encounter[int(args[0]) - 1]
                if len(args) >= 2:
                    if args[1].isnumeric() == True:
                        amt = int(args[1])
                        npc.currentHP += amt
                        if npc.currentHP > npc.maxHP: npc.currentHP = npc.maxHP
                        print(npc.name + " was healed by " + str(amt) + " points.") #Should display the actual amount restored asopposed to the amount input
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
        print("Your graveyard is empty. There is no one to revive.")
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
    
    ###Debug input
    #print(action)
    #print(command)
    #print(args)
    
    if command == "help" or command == "?":
        displayHelp()
    elif command == "quit" or command == "q" or command == "exit":
        wait = False
    elif command == "list":
        displayList(args)
    elif command == "add":
        add(args)
    elif command == "revive" or command == "resurrect" or command == "save":
        revive(args)
    elif command == "remove" or command == "clear":
        remove(args)
    elif command == "status":                    #Status could be rewritten to not be a property of NPCs
        if len(encounter) > 0:                   #Status should be able to display status of dead enemies
            if len(args) > 0:
                if isValidInt(args[0], encounter) == True:
                    encounter[int(args[0]) - 1].status()
                else:
                    print("Selected an invalid NPC.")
            else:
                print("status requires 1 argument")
        else:
            print("status requires an encounter first.")
    elif command == "attack":
        attack(args)
    elif command == "kill" or command == "smite":
        smite(args)
    elif command == "heal":
        heal(args)
    elif command == "change-ac":
        changeAC(args)
    else:
        print("Unrecognized command.")
        print("Type help or ? to learn how to use availible commands.")