import unittest
from encounter import NPC

class TestEncounter(unittest.TestCase):
    def test_NPC_creation(self):
        self.assertEquals(NPC("test", 6, 9).name, "test")
        self.assertEquals(NPC("test", 6, 9).currentHP, 6)
        self.assertEquals(NPC("test", 6, 9).maxHP, 6)
        self.assertEquals(NPC("test", 6, 9).ac, 9)
        
        
    def test_NPC_equals(self):
        human = NPC("Human", 5, 12)
        bruh = NPC("Bruh", 1, 1)
        bread = flatbread = NPC("Human", 5, 12)
        test = NPC("test", 6, 9)
        
        self.assertTrue(human.equals(human))
        self.assertFalse(bruh.equals(NPC("test", 6, 9)))
        self.assertFalse(NPC("oh", 1, 0).equals(NPC("test", 6, 9)))
        self.assertTrue(NPC("test", 6, 9).equals(NPC("test", 6, 9)))
        self.assertTrue(NPC("test", 6, 9).equals(test))
        self.assertTrue(bread.equals(flatbread))

if __name__ == "__main__":
    unittest.main()