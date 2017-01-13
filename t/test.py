#!/usr/bin/python

import sys
sys.path.append('..')
import unittest
from token_data import TokenData

class TestRosary(unittest.TestCase):
   def testJoyful(self):
       self._testMysteries('Joyful')

   def _testMysteries(self,mysteries):
       currentData = TokenData('Rosary',mysteries,'SignOfTheCross',0,0)
       token = currentData.get_token();
       newData = currentData.from_token(token)
       self.assertEqual(currentData,newData)


if __name__ == '__main__':
    unittest.main()
