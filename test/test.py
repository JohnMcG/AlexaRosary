#!/usr/bin/python

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

   def _testMysteries(self,mysteries):
       currentData = TokenData('Rosary',mysteries,'SignOfTheCross',0,0)
       token = currentData.get_token();
       newData = currentData.from_token(token)
       self.assertEqual(currentData,newData)
       currentData = self._testBeginning(currentData, mysteries)
       for i in range(1,6):
          currentData = self._testDecade(currentData, mysteries, i)
       currentData = self._testEnding(currentData, mysteries)

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
