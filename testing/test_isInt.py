import unittest
import isInt

noText = ""
letter = "f"
word = "frog"
boundaryNegative = "-1"
boundaryZero = "0"
boundaryPositive = "1"
positive = "99"
negative = "-10"
minusAfter = "1-"
minusBeforeAndAfter= "-1-"
minusAndLetter = "-a"
minusLetterAndNumber = "-9a"
doubleNegative = "--1"

class test_isNumeric(unittest.TestCase):
    def test_isnumeric_noText(self):
        self.assertFalse(noText.isnumeric())
    
    def test_isnumeric_letter(self):
        self.assertFalse(letter.isnumeric())
    
    def test_isnumeric_word(self):
        self.assertFalse(word.isnumeric())
    
    def test_isnumeric_boundaryNegative(self):
        self.assertFalse(boundaryNegative.isnumeric(), "Is False since it contains a non-digit")
    
    def test_isnumeric_boundaryZero(self):
        self.assertTrue(boundaryZero.isnumeric())
    
    def test_isnumeric_boundaryPositive(self):
        self.assertTrue(boundaryPositive.isnumeric())
    
    def test_isnumeric_positive(self):
        self.assertTrue(positive.isnumeric())
    
    def test_isnumeric_negative(self):
        self.assertFalse(negative.isnumeric(), "Is False since it contains a non-digit")
    
    def test_isnumeric_minusAfter(self):
        self.assertFalse(minusAfter.isnumeric())
    
    def test_isnumeric_minusBeforeAndAfter(self):
        self.assertFalse(minusBeforeAndAfter.isnumeric())
    
    def test_isnumeric_minusAndLetter(self):
        self.assertFalse(minusAndLetter.isnumeric())
    
    def test_isnumeric_minusLetterAndNumber(self):
        self.assertFalse(minusLetterAndNumber.isnumeric())
    
    def test_isnumeric_doubleNegative(self):
        self.assertFalse(doubleNegative.isnumeric())

class test_int(unittest.TestCase):
    def test_int_doubleNegative(self):
        self.assertEqual(int(--1), 1)
    
    def test_int_doubleNegativeZero(self):
        self.assertEqual(int(--0), 0)
    
    def test_int_negativeZero(self):
        self.assertEqual(int(-0), 0)
    
    def test_int_negativeInt(self):
        self.assertEqual(int(-1), -1)
    
    def test_int_positiveInt(self):
        self.assertEqual(int(45), 45)
    
    def test_int_decimal(self):
        self.assertEqual(int(1.0), 1)
    
    def test_int_boundaryRoundDown(self):
        self.assertEqual(int(1.4), 1)
    
    def test_int_boundaryRoundUp(self):
        self.assertEqual(int(1.5), 1)
    
    def test_int_letter(self):
        with self.assertRaises(ValueError):
            int(letter)
    
    def test_int_positiveNumberString(self):
        self.assertEqual(int(positive), 99)
    
    def test_int_boundaryNegaitveString(self):
        self.assertEqual(int(boundaryNegative), -1)
            
    def test_int_doubleNegaitveString(self):
        with self.assertRaises(ValueError):
            int(doubleNegative)

class test_isInt(unittest.TestCase):
    def test_isInt_noText(self):
        self.assertFalse(isInt.isInt(noText))
    
    def test_isInt_letter(self):
        self.assertFalse(isInt.isInt(letter))
    
    def test_isInt_word(self):
        self.assertFalse(isInt.isInt(word))
    
    def test_isInt_boundaryNegative(self):
        self.assertTrue(isInt.isInt(boundaryNegative), "Should be recognized as an integer")
    
    def test_isInt_boundaryZero(self):
        self.assertTrue(isInt.isInt(boundaryZero))
    
    def test_isInt_boundaryPositive(self):
        self.assertTrue(isInt.isInt(boundaryPositive))
    
    def test_isInt_positive(self):
        self.assertTrue(isInt.isInt(positive))
    
    def test_isInt_negative(self):
        self.assertTrue(isInt.isInt(negative))
    
    def test_isInt_minusAfter(self):
        self.assertFalse(isInt.isInt(minusAfter), "Contains a minus sign, but is not a proper number format")
    
    def test_isInt_minusBeforeAndAfter(self):
        self.assertFalse(isInt.isInt(minusBeforeAndAfter), "Contains a valid number, but isn't as a whole valid")
    
    def test_isInt_minusAndLetter(self):
        self.assertFalse(isInt.isInt(minusAndLetter), "Contains a valid number, but isn't as a whole valid")
    
    def test_isInt_minusLetterAndNumber(self):
        self.assertFalse(isInt.isInt(minusLetterAndNumber), "Contains a valid number, but isn't as a whole valid")
    
    def test_isInt_doubleNegative(self):
        self.assertFalse(isInt.isInt(doubleNegative), "Ideally should be recognized as a positive number, but is out of scope of reasonable programming to catch this case")

if __name__ == '__main__':
    unittest.main()