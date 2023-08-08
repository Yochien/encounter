import unittest
from src.commands import isInt
from src.npc import CombatNPC


class TestSubMethods(unittest.TestCase):
    def test_Encounter(self):
        self.assertFalse(isInt("e"))
        self.assertTrue(isInt("1"))
        self.assertTrue(isInt("11"))


class TestNPCs(unittest.TestCase):
    def test_valid_combat_npc(self):
        npc = CombatNPC("Mulligan", 1, 0)
        self.assertEqual("Mulligan", npc.name)
        self.assertEqual(1, npc.maxHP)
        self.assertEqual(1, npc.currentHP)
        self.assertEqual(0, npc.ac)

    def test_invalid_npc(self):
        self.assertRaises(TypeError, CombatNPC, 1, 1, 1)
        self.assertRaises(TypeError, CombatNPC, "Norm", 'err', 1)
        self.assertRaises(TypeError, CombatNPC, "Norm", 1, 'err')

        self.assertRaises(ValueError, CombatNPC, "", 1, 1)
        self.assertRaises(ValueError, CombatNPC, "Whoops", 0, 1)
        self.assertRaises(ValueError, CombatNPC, "Whoops", 1, -1)

    def test_str(self):
        npc = CombatNPC("Mulligan", 1, 0)
        self.assertEqual("Mulligan", str(npc))

        npc.currentHP = 0
        self.assertEqual("Mulligan [X]", str(npc))

    def test_detailedInfo(self):
        npc = CombatNPC("Mulligan", 10, 0)
        self.assertEquals("Mulligan [10/10]", npc.detailedInfo())

        npc.currentHP = 7
        self.assertEquals("Mulligan [7/10]", npc.detailedInfo())

        npc.currentHP = 0
        self.assertEquals("Mulligan [Dead]", npc.detailedInfo())


# Allows for running the file directly to test
if __name__ == '__main__':
    unittest.main()
