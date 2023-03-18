import commands as cmd
from npc import NPCList


def initialize_commands() -> list[cmd.Command]:
    bestiary = NPCList(['bestiary', 'book', 'b'])
    encounter = NPCList(['encounter', 'e', 'combat', 'c'])
    referenceLists = [bestiary, encounter]

    commands = []
    commands.append(cmd.load(bestiary))
    commands.append(cmd.displayMenu(referenceLists))
    commands.append(cmd.addNPC(referenceLists))
    commands.append(cmd.removeNPC(encounter))
    commands.append(cmd.clearNPCList(referenceLists))
    commands.append(cmd.smite(encounter))
    commands.append(cmd.damage(encounter))
    commands.append(cmd.attack(encounter))
    commands.append(cmd.heal(encounter))
    commands.append(cmd.status(encounter))
    commands.append(cmd.info(bestiary))
    commands.append(cmd.make(bestiary))
    commands.append(cmd.name(encounter))
    commands.append(cmd.mark(encounter))
    commands.append(cmd.unmark(encounter))
    commands.append(cmd.displayHelp(commands))
    return commands


    print("Type help or ? to get a list of availible commands.")
def main():
    commands = initialize_commands()

    for command in commands:
        if "load" in command.names:
            command.execute("bestiary.txt")
            break
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
