import src.commands as cmd
from src.npc import NPCList


def initialize_commands() -> list[cmd.Command]:
    bestiary = NPCList(["bestiary", "book", "b"])
    encounter = NPCList(["encounter", "e", "combat", "c"])
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
    commands.append(cmd.rank(encounter))
    commands.append(cmd.displayHelp(commands))
    return commands


def main():
    commands = initialize_commands()

    for command in commands:
        if "load" in command.names:
            command.execute(["bestiary.txt"])
            break

    prompt = "\nType a command: "
    print("Type help or ? to get a list of availible commands.")

    while True:
        userInput = input(prompt).split(" ")
        userInput = [token for token in userInput if not token.isspace() and not token == ""]

        if not len(userInput) > 0:
            prompt = "\nType a command: "
            continue
        else:
            prompt = "\ncmd: "

        userCommand = userInput.pop(0).lower()
        if userCommand in ["quit", "q", "exit"]:
            break

        found = False
        for command in commands:
            if userCommand in command.names:
                command.execute(userInput)
                found = True
                break

        if not found:
            print("Unrecognized command.")
            print("Type help or ? to learn how to use availible commands.")


if __name__ == "__main__":
    main()
