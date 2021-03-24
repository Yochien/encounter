class Monster:
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

#Monster lists
bestiary = []
encounter = []
graveyard = []

#Attempt to open the bestiary file. If not found fallback on a default set of monsters
try:
    with open("bestiary") as book:
        for line in book:
            if not line.startswith("#"):
                line = line.rstrip("\n").split(",")
                monster = Monster(line[0], line[1], line[2])
                bestiary.append(monster)
except FileNotFoundError:
    npc = Monster("NPC", 5, 12)
    animal = Monster("Animal", 3, 10)
    enemy = Monster("Enemy", 10, 13)
    bestiary.append(npc)
    bestiary.append(animal)
    bestiary.append(enemy)

def helpEncounter():
    print(
'''
help or ?
--prints this premade list of commands that you can use to interact with your list of monsters.
quit or exit
--exits the program.
list [str]
--if [str] is bestiary the function will print a list of availible monsters to add to your encounter.
--if [str] is encounter the function will print the monsters in your current encounter.
--if [str] is graveyard the function will list the currently defeated monsters in your encounter.
--if [str] is left blank the bestiary will be shown with a message explaining how to select a particular list.
add [num1,num2,num3,...] [list]
--populates the encounter list with your selected monsters in the list [str].
--[list] can either be encounter or graveyard.
remove [num1,num2,etc... or str] [list]
--removes monsters at positions [num1,num2,etc...] from [list].
--list can either be encounter or graveyard.
--duplicate numbers in list [nums] will be ignored.
--setting [str] to all will clear the selected list in [list].
--setting [str] to all and [list] to all will clear all lists of all monsters.
--providing no list after [str] =  all will do the same as remove all all.
revive or resurrect [num]
--revives the monster in position [num] in the graveyard list.
The following commands require a non empty encounter
status [num]
--prints a monster [num]'s name and the amount of hp they have left from the encounter list.
attack [num]
--attacks a monster from the encounter list at the position [num].
smite or kill
--instantly sends a monster to the graveyard.
heal [num1] [num2]
--heals a monster at position [num1] in the encounter list by [num2] amount of health points, but won't raise currentHP above maxHP.
change-ac [num1] [num2]
--adds [num2] to monster's armor class at position [num1] in  the encounter list. A monster's armor class cannot fall below 0.
END
'''
    ),

def menu(monsterList, title = "MENU:"):
    title = title.upper() + ":"
    print(title)

    c = 0
    if len(monsterList) > 0:
        for m in monsterList:
            c += 1
            print(str(c) + " " + m.name)
    else:
        print("EMPTY")

    print("")

def listMenu(book = None):
    if arg1 == None:
        menu(bestiary, "bestiary")
        menu(encounter, "encounter")
        menu(graveyard, "graveyard")
    else:
        book == book.strip(" ").lower()
        if book == "bestiary":
            menu(bestiary, "bestiary")
        elif book == "encounter":
            menu(encounter, "encounter")
        elif book == "graveyard":
            menu(graveyard, "graveyard")
        elif book == "all":
            menu(bestiary, "bestiary")
            print("")
            menu(encounter, "encounter")
            print("")
            menu(graveyard, "graveyard")
        else:
            print("Unknown list selected.")

def isValidInt(selector, monsterList):
    valid = True
    for s in selector:
        if s.isnumeric() == False:
            valid = False
    if valid == True:
        for s in selector:
            if int(s) > len(monsterList) or int(s) <= 0:
                valid = False
    else:
        print("One or more inputs are invalid in this context.")
    
    return valid

def add(args = None, monsterList = None):
    if args == None:
        print("Command requires at least one monster.")
    else:
        skip = False
        args = args.split(",")
        for n in args:
            if int(n) > len(bestiary) or int(n) <= 0:
                skip = True
        if skip == True:
            print("One or more selected monsters is outside the range of the bestiary.")
        else:
            for m in args:
                name = bestiary[int(m) - 1].name
                hp = bestiary[int(m) - 1].maxHP
                ac = bestiary[int(m) - 1].ac
                monster = Monster(name, hp, ac)
                if monsterList == "encounter":
                    encounter.append(monster)
                elif monsterList == "graveyard":
                    graveyard.append(monster)
                else:
                    pass
            if monsterList == None:
                print("No list selected.")
            elif monsterList == "encounter":
                menu(encounter, "encounter")
            elif monsterList == "graveyard":
                menu(graveyard, "graveyard")
            else:
                print("Referenced an unknown list.")

def delete(selector, monsterList):
    count = 0
    skip = False
    length = len(monsterList)

    for s in selector:
        if int(s) > length or int(s) < 0:
            skip = True
    if skip == False:
        for s in selector:
            monsterList[int(s) - 1] = None
            count += 1
        count = 0
        while count < length:                  #####################################
            try:                               ###Remove dependency on try except###
                index = monsterList.index(None)#####################################
                monsterList.pop(index)
            except ValueError:
                pass
            count += 1
    else:
        print("One or more numbers out of range of availible monsters.")

def remove(selector = None, monsterList = None):
    if selector == None:
        print("remove requires at least two arguments.")
    elif selector == "all":
        if monsterList == "all":
            encounter.clear()
            graveyard.clear()
            menu(encounter, "encounter")
            menu(graveyard, "graveyard")
        elif monsterList == "encounter":
            encounter.clear()
            menu(encounter, "encounter")
        elif monsterList == "graveyard":
            graveyard.clear()
            menu(graveyard, "graveyard")
        else:
            print("Selected an unknown list.")
    else:
        selector = selector.split(",")
        count = 0
        skip = False
        
        if monsterList == None:
            print("remove requires at least two arguments.")
        else:
            monsterList = monsterList.lower()
            if monsterList == "encounter" and encounter != []:
                delete(selector, encounter)
                menu(encounter, "encounter")
            elif monsterList == "graveyard" and len(graveyard) > 0:
                delete(selector, graveyard)
                menu(graveyard, "graveyard")
            else:
                print("Unknown list selected or selected list is empty.")

def attack(monster, accuracy = None, amt = None):
    if monster.currentHP > 0:
        print("Party member attacks " + monster.name + ".")
        if accuracy != None and amt != None:
            if int(accuracy) >= monster.ac:
                monster.damage(amt)
            else:
                print("Attack misses " + monster.name + ".")
        elif accuracy != None and amt == None:
            if int(accuracy) >= monster.ac:
                amt = input("Roll for damage: ")
                monster.damage(amt)
            else:
                print("Attack misses " + monster.name + ".")
        else:
            accuracy = input("Roll for hit: ")
            if int(accuracy) >= monster.ac:
                amt = input("Roll for damage: ")
                monster.damage(amt)
            else:
                print("Attack misses " + monster.name + ".")

    if monster.currentHP <= 0:
        print(monster.name + " has been defeated.")
        graveyard.append(monster)
        encounter.pop(int(arg1) - 1)
        if len(encounter) == 0:
            print("Party has defeated all enemies.")

def smite(selector):
    global graveyard
    if selector == "all":
        graveyard = graveyard + encounter
        encounter.clear()
        print("All monsters defeated.")
    else:
        print(encounter[int(selector) - 1].name + " has been defeated.")
        graveyard.append(encounter[int(selector) - 1])
        encounter.pop(int(selector) - 1)
    
    if len(encounter) == 0:
        print("Party has defeated all enemies.")

def heal(monster, amount):
    monster.currentHP += amount
    if monster.currentHP > monster.maxHP: monster.currentHP = monster.maxHP
    print(monster.name + " was healed by " + str(amount) + " points.")

def revive(monster):
    encounter.append(monster)
    graveyard.pop(int(arg1) - 1)
    print(encounter[-1].name + " has been revived.")

def changeAC (monster, amount):
    monster.ac += amount
    if monster.ac < 0: monster.ac = 0
    print(monster.name + "'s armor class was changed by " + str(amount) + ".")

print("Type help or ? to get a list of availible commands.")
wait = True
while wait:
    action = input("Type an action to perform: ").lower().split(" ")
    
    #default all arguments to None
    command = arg1 = arg2 = arg3 = None
    
    if (len(action) > 3):
        command = action[0]
        arg1 = action[1]
        arg2 = action[2]
        arg3 = action[3]
    elif (len(action) == 3):
        command = action[0]
        arg1 = action[1]
        arg2 = action[2]
    elif (len(action) == 2):
        command = action[0]
        arg1 = action[1]
    elif (len(action) == 1):
        command = action[0]
    else:
        command = None

    if command == "help" or command == "?":
        helpEncounter()
    elif command == "quit" or command == "q" or command == "exit":
        wait = False
    elif command == "list":
        listMenu(arg1)
    elif command == "add":
        add(arg1, arg2)
    elif command == "revive" or command == "resurrect":
        if len(graveyard) > 0:
            revive(graveyard[int(arg1) - 1])
        else:
            print("Your graveyard is empty. There is no one to revive.")
    elif command == "remove":
        if len(encounter) > 0 or len(graveyard) > 0:
            remove(arg1, arg2)
        else:
            print("encounter and graveyard lists are empty. There is no one to remove.")
    elif command == "status" or command == "attack" or command == "kill" or command == "smite" or command == "heal" or command == "change-ac":
        if encounter != []:
            if command == "status":
                if isValidInt(arg1, encounter) == True:
                    encounter[int(arg1) - 1].status()
            elif command == "attack":
                valid = True
                if arg2 == None and arg3 == None:
                    valid = True
                elif arg2.isnumeric() == True and arg3.isnumeric() == True:
                    valid = True
                elif arg2.isnumeric() == True:
                    valid = True
                else:
                    valid = False
                
                if valid == True:
                    if isValidInt(arg1, encounter) == True:
                        attack(encounter[int(arg1) - 1], arg2, arg3)
                    else:
                        print("One or more inputs are invalid in this context.")
            elif command == "kill" or command == "smite":
                smite(arg1)
            elif command == "heal":
                if isValidInt(arg1, encounter) == True:
                    heal(encounter[int(arg1) - 1], int(arg2))
            elif command == "change-ac":
                if isValidInt(arg1, encounter) == True:
                    changeAC(encounter[int(arg1) - 1], int(arg2))
        else:
            print("You must build an encounter before using that command.")
    else:
        print("Unrecognized command.")
        print("Type help or ? to learn how to use availible commands.")