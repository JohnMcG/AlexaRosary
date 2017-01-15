#!/usr/bin/python
"""
Test class for token data class

by John McGuinness, 2017
"""


import sys
import os
sys.path.insert(0,os.path.abspath('..'))
import unittest
from token_data import TokenData

class TestRosary(unittest.TestCase):
   def testJoyful(self):
       self._testMysteries('Joyful')
   def testSorrowful(self):
       self._testMysteries('Sorrowful')
   def testGlorious(self):
       self._testMysteries('Glorious')
   def testLuminous(self):
       self._testMysteries('Luminous')

   def testTokenization(self):
       currentData = TokenData('Rosary','Joyful','SignOfTheCross',0,0)
       token = currentData.get_token();
       newData = currentData.from_token(token)
       self.assertEqual(currentData,newData)
      

   """
   Test the rosary -- beginning, 5 decades, and the ending
   """
   def _testMysteries(self,mysteries):
       currentData = TokenData('Rosary',mysteries,'SignOfTheCross',0,0)
       
       currentData = self._testBeginning(currentData, mysteries)
       for i in range(1,6):
          currentData = self._testDecade(currentData, mysteries, i)
       currentData = self._testEnding(currentData, mysteries)

   """
   The beginning is the Sign of the Cross, the Creed, the Our Father,
   3 Hail Marys, the Glory Be, and the Fatima Prayer
   """
   def _testBeginning(self, currentData, mysteries):
      expected = TokenData('Rosary',mysteries,'SignOfTheCross',0,0)
      self.assertEqual(expected, currentData)

      currentData = currentData.get_next()
      expected.prayer='Creed'
      self.assertEqual(expected, currentData)
            
      currentData = currentData.get_next()
      expected.prayer='Our Father'
      self.assertEqual(expected, currentData)
      for i in range(0,3):
         expected.prayer='Hail Mary'
         expected.counter = i
         currentData = currentData.get_next()
         self.assertEqual(expected, currentData)

      expected.prayer = 'Glory Be'
      expected.counter = 0
      currentData = currentData.get_next()
      self.assertEqual(expected, currentData)

      expected.prayer = 'Fatima Prayer'
      currentData = currentData.get_next()
      self.assertEqual(expected, currentData)

      currentData = currentData.get_next()
      return currentData

   """
   A decade consists of the announcement of the mystery, the Our Father,
   10 Hail Marys, the Glory Be, and the Fatima Prayer
   """
   def _testDecade(self, currentData, mysteries, decade):
      expected = TokenData('Rosary',mysteries,'Mystery',decade,0)
      self.assertEqual(expected, currentData)

      currentData = currentData.get_next()
      expected.prayer='Our Father'
      self.assertEqual(expected, currentData)

      for i in range(0,10):
         expected.prayer='Hail Mary'
         expected.counter = i
         currentData = currentData.get_next()
         self.assertEqual(expected, currentData)

      expected.prayer = 'Glory Be'
      expected.counter = 0
      currentData = currentData.get_next()
      self.assertEqual(expected, currentData)

      expected.prayer = 'Fatima Prayer'
      currentData = currentData.get_next()
      self.assertEqual(expected, currentData)

      currentData = currentData.get_next()
      return currentData

   """
   The Ending is the Hail Holy Queen, the Closing Prayer, and
   the Sign Of the Cross
   """
   def _testEnding(self, currentData, mysteries):
      expected = TokenData('Rosary',mysteries,'Hail Holy Queen',5,0)
      self.assertEqual(expected, currentData)

      expected.prayer = 'ClosingPrayer'
      currentData = currentData.get_next()
      self.assertEqual(expected, currentData)

      expected.prayer = 'SignOfTheCross'
      currentData = currentData.get_next()
      self.assertEqual(expected, currentData)

      currentData = currentData.get_next()
      self.assertEqual({},currentData)

if __name__ == '__main__':
    unittest.main()
