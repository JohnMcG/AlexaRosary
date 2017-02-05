#!/usr/bin/python
"""
Test class for token data class

by John McGuinness, 2017
"""


import sys
import os
import unittest
sys.path.insert(0,os.path.abspath('..'))
os.environ['AUDIO_HOST'] = 'AUDIO_HOST'
from token_data import RosaryTokenData
from token_data import TokenData
from token_data import DivineMercyTokenData

class TestBaseClass(unittest.TestCase):
   
   def testTokenizeBadPrayerTypeShouldThrow(self):
       currentData = RosaryTokenData('Joyful','SignOfTheCross',0,0)
       currentData.prayer_type='XYX'
       token = currentData.get_token()
       with self.assertRaisesRegexp(NotImplementedError, 'Bad prayer type') as context:
          newData = currentData.from_token(token)

   def testCannotDirectlyIntantiateBaseClass(self):
      with self.assertRaisesRegexp(TypeError, 'instantiate abstract class') as context:
         currentData = TokenData('Rosary','Joyful','SignOfTheCross',0,0)
   

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
       currentData = RosaryTokenData('Joyful','SignOfTheCross',0,0)
       token = currentData.get_token();
       newData = currentData.from_token(token)
       self.assertEqual(currentData,newData)
      


       
   """
   Test the rosary -- beginning, 5 decades, and the ending
   """
   def _testMysteries(self,mysteries):
       currentData = RosaryTokenData(mysteries,'SignOfTheCross',0,0)
       
       currentData = self._testBeginning(currentData, mysteries)
       for i in range(1,6):
          currentData = self._testDecade(currentData, mysteries, i)
       currentData = self._testEnding(currentData, mysteries)

   """
   The beginning is the Sign of the Cross, the Creed, the Our Father,
   3 Hail Marys, the Glory Be, and the Fatima Prayer
   """
   def _testBeginning(self, currentData, mysteries):
      expected = RosaryTokenData(mysteries,'SignOfTheCross',0,0)
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
      expected = RosaryTokenData(mysteries,'Mystery',decade,0)
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
      expected = RosaryTokenData(mysteries,'Hail Holy Queen',5,0)
      self.assertEqual(expected, currentData)

      expected.prayer = 'ClosingPrayer'
      currentData = currentData.get_next()
      self.assertEqual(expected, currentData)

      expected.prayer = 'SignOfTheCross'
      currentData = currentData.get_next()
      self.assertEqual(expected, currentData)

      currentData = currentData.get_next()
      self.assertEqual({},currentData)

class TestDivineMercy(unittest.TestCase):
   def testDivineMercy(self):
      self._testDivineMercy()

   def testTokenization(self):
      currentData = DivineMercyTokenData('SignOfTheCross',0,0)
      token = currentData.get_token();
      newData = currentData.from_token(token)
      self.assertEqual(currentData,newData)
      
       
   """
   Test the Divine Mercy Chaplet -- beginning, 5 decades, and the ending
   """
   def _testDivineMercy(self):
       currentData = DivineMercyTokenData('SignOfTheCross',0,0)
       
       currentData = self._testBeginning(currentData)
       for i in range(1,6):
          currentData = self._testDecade(currentData, i)
          
       currentData = self._testEnding(currentData)

   """
   The beginning is the Sign of the Cross,  the Our Father,
   the Hail Mary, and the Creed
   """
   def _testBeginning(self, currentData):
      expected = DivineMercyTokenData('SignOfTheCross',0,0)
      self.assertEqual(expected, currentData)

      currentData = currentData.get_next()
      expected.prayer='Our Father'
      self.assertEqual(expected, currentData)

      currentData = currentData.get_next()
      expected.prayer='Hail Mary'
      self.assertEqual(expected, currentData)

      expected.prayer = 'Creed'
      expected.counter = 0
      currentData = currentData.get_next()
      self.assertEqual(expected, currentData)

      currentData = currentData.get_next()
      return currentData

   """
   A decade consists of the Eternal Father and
   10 'For the sake..' prayers
   """
   def _testDecade(self, currentData, decade):
      expected = DivineMercyTokenData('Eternal Father',decade,0)
      self.assertEqual(expected, currentData)

      for i in range(0,10):
         expected.prayer='For the sake'
         expected.counter = i
         currentData = currentData.get_next()
         self.assertEqual(expected, currentData)

      currentData = currentData.get_next()
      return currentData

   """
   The Ending is the Holy God and the Sign of the Cross
   the Sign Of the Cross
   """
   def _testEnding(self, currentData):
      expected = DivineMercyTokenData('Holy God',5,0)
      self.assertEqual(expected, currentData)

      expected.prayer = 'SignOfTheCross'
      currentData = currentData.get_next()
      self.assertEqual(expected, currentData)

      currentData = currentData.get_next()
      self.assertEqual({},currentData)

      
if __name__ == '__main__':
    unittest.main()


