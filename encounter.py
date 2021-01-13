class Monster:
    def __init__(self, name, hp, ac):
        self.name = name
        self.hp = int(hp)
        self.ac = int(ac)
        
    def status(self):
        print(self.name + ": " + str(self.hp))
    
    def attack(self):
        if self.hp > 0:
            print("Party member attacks " + self.name + ".")
            accuracy = input("Roll for hit: ")
            if int(accuracy) >= self.ac:
                damage = input("Roll for damage: ")
                self.hp = self.hp - int(damage)
            else:
                print("Attack misses " + self.name + ".")
        else:
            print("That enemy is already dead.")

print("AVAILIBLE MONSTERS")
with open("bestiary") as bestiary:
    count = 1
    for line in bestiary:
        if not line.startswith("#"):
            line = line.split(",")
            print(str(count) + " " + line[0])
            count += 1

print("BUILD ENCOUNTER")
print("Type the number of each monster to include separated by a comma. Duplicates are allowed.")
encounter = []
c = 0

validate = True
while validate:
    try:
        monsters = input("Enemies to include: ").split(",")
        for m in monsters:
            with open("bestiary") as bestiary:
                lineCount = 0
                for line in bestiary:
                    if not line.startswith("#"):
                        lineCount += 1
                        if lineCount == int(m):
                            line = line.rstrip("\n").split(",")
                            monster = Monster(line[0], line[1], line[2])
                            encounter.append(monster)
                            c += 1
            validate = False
    except ValueError:
        print("Encountered invalid number. Try input again.")

print("Enemies in encounter:")
battle = True
validate = True
while validate:
    try:
        while battle:
            c = 0
            for m in encounter:
                if m.hp <= 0:
                    print("Party has defeated " + encounter[c].name)
                    encounter.pop(c)
                c += 1
            
            c = 0 
            for m in encounter:
                c += 1
                print(str(c) + " " + m.name)

            if len(encounter) > 1:
                a = input("Enter number of enemy to attack: ")
                if int(a) > 0 and int(a) <= len(encounter):
                    encounter[int(a) - 1].attack()
                else:
                    raise IndexError
            elif len(encounter) == 1:
                encounter[0].attack()
            else:
                battle = False
                validate = False
    except IndexError:
        print("Encountered invalid number.")
print("BATTLE ENDED")