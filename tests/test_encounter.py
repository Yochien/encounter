import unittest

from src.commands import isInt, areAllDefeated
from src.npc import BookNPC, CombatNPC, NPCList


class TestSubMethods(unittest.TestCase):
    def test_IsInt(self):
        self.assertFalse(isInt("e"))
        self.assertTrue(isInt("1"))
        self.assertTrue(isInt("11"))

    def test_AreAllDefeated(self):
        # Setup
        npcs = NPCList(["combat"], CombatNPC)
        npc1 = CombatNPC("NPC1", 1, 1)
        npc2 = CombatNPC("NPC2", 1, 1)
        npc3 = CombatNPC("NPC3", 1, 1)
        npcs.data.append(npc1)
        npcs.data.append(npc2)
        npcs.data.append(npc3)
        self.assertFalse(areAllDefeated(npcs))

        npc1.currentHP = 0
        self.assertFalse(areAllDefeated(npcs))

        npc1.currentHP = 0
        npc2.currentHP = 0
        npc3.currentHP = 0
        self.assertTrue(areAllDefeated(npcs))


class TestNPCs(unittest.TestCase):
    def test_valid_combat_npc(self):
        npc = CombatNPC("Mulligan", 1, 0)
        self.assertEqual("Mulligan", npc.name)
        self.assertEqual("Mulligan", npc.nick)
        self.assertEqual(1, npc.maxHP)
        self.assertEqual(1, npc.currentHP)
        self.assertEqual(0, npc.ac)

    def test_invalid_combat_npc(self):
        self.assertRaises(TypeError, CombatNPC, 1, 1, 1)
        self.assertRaises(TypeError, CombatNPC, "Norm", "err", 1)
        self.assertRaises(TypeError, CombatNPC, "Norm", 1, "err")

        self.assertRaises(ValueError, CombatNPC, "", 1, 1)
        self.assertRaises(ValueError, CombatNPC, "Whoops", 0, 1)
        self.assertRaises(ValueError, CombatNPC, "Whoops", 1, -1)

    def test_combat_npc_str(self):
        npc = CombatNPC("Mulligan", 1, 0)
        self.assertEqual("Mulligan", str(npc))

        npc.currentHP = 0
        self.assertEqual("Mulligan [X]", str(npc))

    def test_combat_npc_detailedInfo(self):
        npc = CombatNPC("Mulligan", 10, 0)
        self.assertEquals("Mulligan [10/10]", npc.detailedInfo())

        npc.currentHP = 7
        self.assertEquals("Mulligan [7/10]", npc.detailedInfo())

        npc.currentHP = 0
        self.assertEquals("Mulligan [Dead]", npc.detailedInfo())

    def test_valid_book_npc(self):
        npc = BookNPC("Mulligan", 1, 0, "description")
        self.assertEqual("Mulligan", npc.name)
        self.assertEqual(1, npc.maxHP)
        self.assertEqual(0, npc.ac)
        self.assertEqual("description", npc.description)

    def test_invalid_book_npc(self):
        self.assertRaises(TypeError, BookNPC, 1, 1, 1)
        self.assertRaises(TypeError, BookNPC, "Norm", "err", 1)
        self.assertRaises(TypeError, BookNPC, "Norm", 1, "err")
        self.assertRaises(TypeError, BookNPC, "Norm", 1, 0, 1)

        self.assertRaises(ValueError, BookNPC, "", 1, 1)
        self.assertRaises(ValueError, BookNPC, "Whoops", 0, 1)
        self.assertRaises(ValueError, BookNPC, "Whoops", 1, -1)

    def test_book_npc_detailedInfo(self):
        npc = BookNPC("Mulligan", 10, 0)
        self.assertEquals("NAME: Mulligan\nMAX HP: 10\nAC: 0", npc.detailedInfo())

        npc = BookNPC("Mulligan", 10, 0, "description")
        self.assertEquals("NAME: Mulligan\nMAX HP: 10\nAC: 0\nDESCRIPTION: description", npc.detailedInfo())


class TestNPCList(unittest.TestCase):
    def test_npc_list(self):
        self.assertRaises(TypeError, NPCList, "Norm", BookNPC)
        self.assertRaises(TypeError, NPCList, ["Norm"], str)
        self.assertRaises(ValueError, NPCList, [""], BookNPC)

        try:
            NPCList(["Book"], BookNPC)
        except TypeError:
            self.fail("NPCList can have type BookNPC")
        try:
            NPCList(["Book"], CombatNPC)
        except TypeError:
            self.fail("NPCList can have type BookNPC")


# Allows for running the file directly to test
if __name__ == "__main__":
    unittest.main()
