import unittest
from src.commands import isInt
from src.npc import NPC


class TestSubMethods(unittest.TestCase):
    def test_Encounter(self):
        self.assertFalse(isInt("e"))


class TestNPCs(unittest.TestCase):
    def test_valid_npc(self):
        npc = NPC("Mulligan", 1, 0)
        self.assertEqual("Mulligan", npc.name)
        self.assertEqual(1, npc.maxHP)
        self.assertEqual(1, npc.currentHP)
        self.assertEqual(0, npc.ac)

    def test_invalid_npc(self):
        self.assertRaises(TypeError, NPC, 1, 1, 1)
        self.assertRaises(TypeError, NPC, "Norm", 'err', 1)
        self.assertRaises(TypeError, NPC, "Norm", 1, 'err')

        self.assertRaises(ValueError, NPC, "", 1, 1)
        self.assertRaises(ValueError, NPC, "Whoops", 0, 1)
        self.assertRaises(ValueError, NPC, "Whoops", 1, -1)

    def test_str(self):
        npc = NPC("Mulligan", 1, 0)
        self.assertEqual("Mulligan", str(npc))

        npc.currentHP = 0
        self.assertEqual("Mulligan [X]", str(npc))

    def test_equals(self):
        npc1 = NPC("Mulligan", 10, 0)
        npc2 = NPC("Mathias", 130, 16)
        npc3 = NPC("Mulligan", 130, 16)
        npc4 = NPC("Mathias", 10, 16)
        npc5 = NPC("Mathias", 130, 0)
        npc6 = NPC("Mulligan", 10, 0)
        npc6.currentHP = 5
        npc7 = NPC("Mulligan", 10, 0)

        self.assertFalse(npc1.equals(None))
        self.assertTrue(npc1.equals(npc1))
        self.assertFalse(npc1.equals(npc2))
        self.assertFalse(npc1.equals(npc3))
        self.assertFalse(npc1.equals(npc4))
        self.assertFalse(npc1.equals(npc5))
        self.assertFalse(npc1.equals(npc6))
        self.assertTrue(npc1.equals(npc7))

    def test_combatStatus(self):
        npc = NPC("Mulligan", 10, 0)
        self.assertEquals("Mulligan [10/10]", npc.combatStatus())

        npc.currentHP = 7
        self.assertEquals("Mulligan [7/10]", npc.combatStatus())

        npc.currentHP = 0
        self.assertEquals("Mulligan [Dead]", npc.combatStatus())

    def test_detailedInfo(self):
        npc = NPC("Mulligan", 1, 0)
        self.assertEquals("NAME: Mulligan\nMAX HP: 1\nAC: 0", npc.detailedInfo())


# Allows for running the file directly to test
if __name__ == '__main__':
    unittest.main()
