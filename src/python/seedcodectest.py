import unittest
import codecTranslated

class TestStringMethods(unittest.TestCase):

    def test_simpleStiem2Frame(self):
        frame = bytearray(64)
        out = seedcodec.decodeSteim2(frame, 0, False, 0)
        self.assertEqual(len(out), 0)


if __name__ == '__main__':
    unittest.main()
