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
# info [num] [list]
# status [num] [list]
* prints an NPC's [num]'s name and the amount of hp they have left from the any valid list.
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