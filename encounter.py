class Monster:
    def __init__(self, name, maxHP, ac):
        self.name = name
        self.maxHP = self.currentHP = int(maxHP)
        self.ac = int(ac)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def status(self):
        print(str(self) + ": " + str(self.currentHP) + " " + str(self.ac))
        
    def damage(self, amt):
        self.currentHP -= int(amt)

#Define important variables here
encounter = []
graveyard = []

def helpEncounter():
    print("help or ?")
    print("--prints this premade list of commands that you can use to interact with your list of monsters. \n")
    print("quit or exit")
    print("--exits the program. \n")
    print("list [str]")
    print("--if [str] is bestiary the function will print a list of availible monsters to add to your encounter.")
    print("--if [str] is encounter the function will print the monsters in your current encounter.")
    print("--if [str] is graveyard the function will list the currently defeated monsters in your encounter.")
    print("--if [str] is left blank the bestiary will be shown. \n")
    print("add [num1,num2,num3,...] [list]")
    print("--populates the encounter list with your selected monsters in the list [str].")
    print("--[list] can either be encounter or graveyard.")
    print("remove [num1,num2,etc...] [list]")
    print("--removes monsters at positions [num1,num2,etc...] from [list].")
    print("--list can either be encounter or graveyard.")
    print("--duplicate numbers in list [nums] will only remove one monster. \n")
    print("clear [str]")
    print("--clears the encounter and graveyard lists of enemies.")
    print("--if [str] is all the function will clear all lists.")
    print("--if [str] is encounter the function will clear the encounter list.")
    print("--if [str] is graveyard the function will clear the graveyard.")
    print("--If [str] is left blank it will default to all. \n")
    print("The following commands require a non empty encounter")
    print("status [num]")
    print("--prints a monster [num]'s name and the amount of hp they have left from the encounter list. \n")
    print("attack [num]")
    print("--attacks a monster from the encounter list at the position [num]. \n")
    print("smite or kill")
    print("--instantly sends a monster to the graveyard.\n")
    print("heal [num1] [num2]")
    print("--heals a monster at position [num1] in the encounter list by [num2] amount of health points, but won't raise currentHP above maxHP. \n")
    print("revive or resurrect [num]")
    print("--revives the monster in position [num] in the graveyard list. \n")
    print("change-ac [num1] [num2]")
    print("--adds [num2] to monster's armor class at position [num1] in  the encounter list. A monster's armor class cannot fall below 0.")
    print("END")

def menu(list):
    c = 0
    if list == bestiary:
        print("BESTIARY:")
    elif list == encounter:
        print("ENCOUNTER:")
    elif list == graveyard:
        print("GRAVEYARD:")
    else:
        pass

    if len(list) > 0:
        for m in list:
            c += 1
            print(str(c) + " " + str(m))
    else:
        print("EMPTY")

def bestiary():
    print("AVAILIBLE MONSTERS")
    with open("bestiary") as book:
        count = 1
        for line in book:
            if not line.startswith("#"):
                line = line.split(",")
                print(str(count) + " " + line[0])
                count += 1

def list(book = "bestiary"):
    if arg1 == None:
        bestiary()
    else:
        book == book.strip(" ").lower()
        if book == "bestiary":
            bestiary()
        elif book == "encounter":
            menu(encounter)
        elif book == "graveyard":
            menu(graveyard)
        elif book == "all":
            bestiary()
            print("")
            menu(encounter)
            print("")
            menu(graveyard)
        else:
            print("Unknown list selected.")

def add(args = None, list = None):
    if args == None:
        print("Command requires at least one monster.")
    else:
        args = args.split(",")
        c = 0
        for m in args:
            with open("bestiary") as bestiary:
                lineCount = 0
                for line in bestiary:
                    if not line.startswith("#"):
                        lineCount += 1
                        if lineCount == int(m):
                            line = line.rstrip("\n").split(",")
                            monster = Monster(line[0], line[1], line[2])
                            if list == "encounter":
                                encounter.append(monster)
                            elif list == "graveyard":
                                graveyard.append(monster)
                            else:
                                pass
                            c += 1
    if list == None:
        print("Command requires two arguments. Check help for more info.")
    elif list == "encounter":
        menu(encounter)
    elif list == "graveyard":
        menu(graveyard)
    else:
        print("Referenced unknown list.")

def remove(selector = None, args = None):
    if selector == None:
        print("remove requires two arguments. Check help for more info.")
    else:
        selector = selector.split(",")
        count = 0
        skip = False
        if args == None:
            print("remove requires two arguments. Check help for more info.")
        elif args == "encounter" and len(encounter) > 0:
            length = len(encounter)
            for s in selector:
                if int(s) > length or int(s) < 0:
                    skip = True
            if skip == False:
                try:
                    for s in selector:
                        encounter[int(selector[count]) - 1] = None
                        count += 1
                    count = 0
                    while count < length:
                        try:
                            index = encounter.index(None)
                            encounter.pop(index)
                        except ValueError:
                            pass
                        count += 1
                    menu(encounter)
                except IndexError:
                    print("Selected an invalid monster.")
            else:
                print("One or more numbers out of range of availible monsters.")
        elif args == "graveyard" and len(graveyard) > 0:
            length = len(graveyard)
            for s in selector:
                if int(s) > length or int(s) < 0:
                    skip = True
            if skip == False:
                try:
                    for s in selector:
                        graveyard[int(selector[count]) - 1] = None
                        count += 1
                    count = 0
                    while count < length:
                        try:
                            index = graveyard.index(None)
                            graveyard.pop(index)
                        except ValueError:
                            pass
                        count += 1
                    menu(graveyard)
                except IndexError:
                    print("Selected an invalid monster.")
            else:
                print("One or more numbers out of range of availible monsters.")
        else:
            print("Unknown list selected or selected list is empty.")

def listClear(selector = "all"):
    if arg1 == None:
        encounter.clear()
        graveyard.clear()
    else:
        if selector == "all":
            encounter.clear()
            graveyard.clear()
            print("All lists cleared.")
        elif selector == "encounter":
            encounter.clear()
            print("Cleared encounter list.")
        elif selector == "graveyard":
            graveyard.clear()
            print("Cleared graveyard.")
        else:
            print("Unknown list selected.")

def attack(monster):
    if monster.currentHP > 0:
        print("Party member attacks " + str(monster) + ".")
        accuracy = input("Roll for hit: ")
        if int(accuracy) >= monster.ac:
            amt = input("Roll for damage: ")
            monster.damage(amt)
        else:
            print("Attack misses " + monster.name + ".")
        
    if monster.currentHP <= 0:
        print(str(monster) + " has been defeated.")
        graveyard.append(monster)
        encounter.pop(int(arg1) - 1)
    
    if len(encounter) == 0:
        print("Party has defeated all enemies.")

def smite(monster):
    print(str(monster) + " has been defeated.")
    graveyard.append(monster)
    encounter.pop(int(arg1) - 1)
    
    if len(encounter) == 0:
        print("Party has defeated all enemies.")

def heal(monster, amount):
    monster.currentHP += amount
    if monster.currentHP > monster.maxHP: monster.currentHP = monster.maxHP
    print(str(monster) + " was healed by " + str(amount) + " points.")

def revive(monster):
    encounter.append(monster)
    graveyard.pop(int(arg1) - 1)
    print(str(encounter[-1]) + " has been revived.")

def changeAC (monster, amount):
    monster.ac += amount
    if monster.ac < 0: monster.ac = 0
    print(str(monster) + "'s armor class was changed by " + str(amount) + ".")

print("Type help or ? to get a list of availible commands.")
wait = True
while wait:
    action = input("Type an action to perform: ").lower().split(" ")
    command = action[0]
    try:
        arg1 = action[1]
    except IndexError:
        arg1 = None
    try:
        arg2 = action[2]
    except IndexError:
        arg2 = None
    try:
        arg3 = action[3]
    except IndexError:
        arg3 = None

    if command == "help" or command == "?":
        helpEncounter()
    elif command == "quit" or command == "exit":
        wait = False
        exit()
    elif command == "list":
        list(arg1)
    elif command == "add":
        add(arg1, arg2)
    elif command == "clear":
        listClear(arg1)
    elif command == "revive" or command == "resurrect":
        if len(graveyard) > 0:
            revive(graveyard[int(arg1) - 1])
        else:
            print("Your graveyard is empty. There is no one to revive.")
    elif command == "remove":
        if len(encounter) > 0 or len(graveyard) > 0:
            remove(arg1, arg2)
        else:
            print("Both your encounter and graveyard lists are empty. There is no one to remove.")
    else:
        if encounter != []:
            if command == "status":
                if int(arg1) > 0 and int(arg1) <= len(encounter):
                    encounter[int(arg1) - 1].status()
                else:
                    print("Selected number is out of range of availible monsters.")
            elif command == "attack":
                attack(encounter[int(arg1) - 1])
            elif command == "kill" or command == "smite":
                smite(encounter[int(arg1) - 1])
            elif command == "heal":
                heal(encounter[int(arg1) - 1], int(arg2))
            elif command == "change-ac":
                changeAC(encounter[int(arg1) - 1], int(arg2))
            else:
                print("Unrecognized command")
        else:
            print("An error occured running your selected command. Check your arguments. You may need to build an encounter before using that command.")
            print("Type help or ? to get a list of commands and explanations of how to use them.")