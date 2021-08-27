import unittest
import encounter

human = encounter.NPC("Human", 5, 12)
bruh = encounter.NPC("Bruh", 1, 1)
bread = flatbread = encounter.NPC("Human", 5, 12)
test = encounter.NPC("test", 6, 9)

print(human.equals(human))
print(bruh.equals(encounter.NPC("test", 6, 9)))
print(encounter.NPC("oh", 1, 0).equals(encounter.NPC("test", 6, 9)))
print(encounter.NPC("test", 6, 9).name, encounter.NPC("test", 6, 9).currentHP, encounter.NPC("test", 6, 9).maxHP, encounter.NPC("test", 6, 9).ac)
print(encounter.NPC("test", 6, 9).equals(encounter.NPC("test", 6, 9)))
print(encounter.NPC("test", 6, 9).equals(test))
print(bread.equals(flatbread))