import commands as cmd
from npc import NPCList


def main():
    bestiary = NPCList(['bestiary', 'book', 'b'])
    encounter = NPCList(['encounter', 'e', 'combat', 'c'])
    referenceLists = [bestiary, encounter]

    # Instantiate commands
    commands = [
        cmd.load(bestiary),
        cmd.displayMenu(referenceLists),
        cmd.addNPC(referenceLists),
        cmd.removeNPC(encounter),
        cmd.clearNPCList(referenceLists),
        cmd.smite(encounter),
        cmd.damage(encounter),
        cmd.attack(encounter),
        cmd.heal(encounter),
        cmd.status(encounter),
        cmd.info(bestiary),
        cmd.make(bestiary),
        cmd.name(encounter),
        cmd.mark(encounter),
        cmd.unmark(encounter)
    ]

    commands.append(cmd.displayHelp(commands))

    # Load default bestiary
    commands[0].execute(["bestiary.txt"])

    print("Type help or ? to get a list of availible commands.")

    # command loop
    while True:
        print()
        usrRequest = input("Type a command: ").split(" ")

        action = None

        if usrRequest != ['']:
            action = usrRequest[0].lower()

        if action in ['quit', 'q', 'exit']:
            break

        args = []

        if (len(usrRequest) > 1):
            for index in range(1, len(usrRequest)):
                args.append(usrRequest[index])

        found = False
        for command in commands:
            if action in command.names:
                command.execute(args)
                found = True
                break

        if not found:
            print("Unrecognized command.")
            print("Type help or ? to learn how to use availible commands.")


if __name__ == "__main__":
    main()
