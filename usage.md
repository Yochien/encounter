# help / ?
* prints this premade list of commands that you can use to interact with your list of NPCs.

# quit / q / exit
* exits the program.

# load [file]
* loads a file in place of the default bestiary
* [file] should be exact and include the file extension if any
  * ex: myBestiary.txt

# list [str]
* if [str] is bestiary the function will print a list of availible NPCs to add to your encounter.
* if [str] is encounter the function will print the NPCs in your current encounter.
* if [str] is graveyard the function will list the currently defeated NPCs in your encounter.
* if [str] is left blank the bestiary will be shown with a message explaining how to select a particular list.

# add [int1,int2,int3,...] [list]
* populates the encounter list with your selected NPCs in the list [str].
* [list] can either be encounter or graveyard.

# remove [int1,int2,... or str] [list]
* removes NPCs at positions [int1,int2,...] from [list].
* list can either be encounter or graveyard.
* duplicate integers in list will be ignored.
* setting [str] to all will clear the selected list in [list].
* setting [str] to all and [list] to all will clear all lists of all NPCs.
* providing no list after [str] = all will do the same as remove all all.

# revive or resurrect [int]
* revives the NPCs in position [int] in the graveyard list.

**The following commands require a non empty encounter**

# info / status [int] [list]
* prints an NPC's [int]'s name and the amount of HP they have left from the any valid list.

# attack [int]
* attacks an NPC's from the encounter list at the position [int].

# damage [int1] [int2]

* directly subtracts a total amount of HP [int2] from NPC in spot [int1] in your encounter

# smite / kill

* instantly sends an NPC to the graveyard.

# heal [int1] [int2]
* heals an NPC at position [int1] in the encounter list by [int2] amount of HP.
* won't raise currentHP above their maxHP.

# changeAC [int1] [int2]
* adds [int2] to an NPC's armor class at position [int1] in  the encounter list. An NPC's armor class cannot fall below 0.

**END**