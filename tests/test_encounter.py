import unittest
from src.encounter import isInt
from src.encounter import NPC


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
        self.assertRaises(ValueError, NPC, "Whoops", 0, -1)


# Allows for running the file directly to test
if __name__ == '__main__':
    unittest.main()
