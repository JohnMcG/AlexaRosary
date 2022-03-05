"""
Declaration of a class corresponding to the data stored in the token for a prayer

by John McGuinness, 2017
"""

from __future__ import print_function
import struct
import os
from abc import ABC, abstractmethod

AUDIO_HOST=os.environ['AUDIO_HOST']


AUDIO_MAPPING={
    'SignOfTheCross': AUDIO_HOST + 'prayers/SignOfTheCross.m4a',
    'Creed': AUDIO_HOST + 'prayers/Creed.m4a',
    'Our Father': AUDIO_HOST + 'prayers/Our+Father.m4a',
    'Hail Mary': AUDIO_HOST + 'prayers/Hail+Mary.m4a',
    'Glory Be': AUDIO_HOST + 'prayers/Glory+Be.m4a',
    'Fatima Prayer': AUDIO_HOST + 'prayers/Fatima+Prayer.m4a',
    'Hail Holy Queen': AUDIO_HOST + 'prayers/Hail+Holy+Queen.m4a',
    'ClosingPrayer': AUDIO_HOST + 'prayers/ClosingPrayer.m4a',
    'Holy God': AUDIO_HOST + 'prayers/Holy+God.m4a',
    'For the sake': AUDIO_HOST + 'prayers/For+the+sake.m4a',
    'Eternal Father': AUDIO_HOST + 'prayers/Eternal+Father.m4a'
    }

FORMAT='15p15p20pll'

class TokenData(ABC):
    prayer_type='Rosary'
    mysteries='joyful'
    prayer='Creed'
    decade=0
    counter=0

    
    def do_print(self):
        return (self.prayer_type + ":" + self.mysteries + ":" + str(self.decade) + ":" + self.prayer + ":" + str(self.counter))

    def __init__(self,prayer_type,mysteries,prayer,decade,counter):
        self.prayer_type = prayer_type
        self.mysteries = mysteries
        self.prayer = prayer
        self.decade = decade
        self.counter = counter

    @classmethod
    def from_token(self, token):
        parts = struct.unpack(FORMAT,token)
        type  = parts[0].decode('utf-8');
        decoded_mysteries = parts[1].decode('utf-8')
        decoded_prayer = parts[2].decode('utf-8')
        if (type == 'Rosary'):
            return RosaryTokenData(decoded_mysteries,decoded_prayer,parts[3],parts[4])
        elif (type == 'Divine Mercy'):
            return DivineMercyTokenData(decoded_prayer,parts[3],parts[4])
        else:
            raise NotImplementedError('Bad prayer type:' + type)
        
    def get_audio(self):
        if self.prayer=='Mystery':
            return AUDIO_HOST + 'mysteries/' + self.mysteries + '/' + str(self.decade) + '.m4a'
        else:
            return AUDIO_MAPPING[self.prayer]

    def get_token(self):
        return struct.pack(FORMAT, bytes(self.prayer_type, 'utf-8'),
                           bytes(self.mysteries, 'utf-8'),
                           bytes(self.prayer, 'utf-8'),
                           self.decade,
                           self.counter)


    @abstractmethod
    def get_next(self):
        pass
    
    def __eq__(self, other):
        if isinstance(other, TokenData):
            return (self.prayer_type == other.prayer_type
                    and self.mysteries == other.mysteries
                    and self.prayer == other.prayer
                    and self.decade == other.decade
                    and self.counter == other.counter
            )
        else:
            return NotImplemented


class RosaryTokenData(TokenData):
    def __init__(self,mysteries,prayer,decade,counter):
        super(RosaryTokenData, self).__init__('Rosary',mysteries,prayer,decade,counter)
    
    def get_next(self):
        mysteries=self.mysteries
        prayer=self.prayer
        counter=self.counter+1
        decade=self.decade

        if self.prayer=='SignOfTheCross':
            if (self.decade == 0):
                prayer='Creed'
            else:
                return {}
        
        if self.prayer=='Hail Holy Queen':
            prayer='ClosingPrayer'

        if self.prayer=='ClosingPrayer':
            prayer='SignOfTheCross'
            
        if self.prayer=='Creed':
            prayer='Our Father';            

        elif self.prayer=='Mystery':
            prayer='Our Father'
            
        elif self.prayer=='Our Father':
            prayer='Hail Mary'

        elif self.prayer=='Hail Mary':
            if (self.decade == 0 and counter >= 3) or counter >= 10:
                prayer='Glory Be'
                
        elif self.prayer=='Glory Be':
            prayer='Fatima Prayer'

        elif self.prayer=='Fatima Prayer':
            if self.decade >= 5:
                prayer='Hail Holy Queen'
            else:
                prayer='Mystery'
                decade += 1

        if prayer != self.prayer:
            counter=0
                
        return RosaryTokenData(mysteries, prayer, decade, counter)

class DivineMercyTokenData(TokenData):
    def __init__(self,prayer,decade,counter):
        super(DivineMercyTokenData, self).__init__('Divine Mercy','',prayer,decade,counter)
    
    def get_next(self):
        prayer=self.prayer
        counter=self.counter+1
        decade=self.decade

        if self.prayer == 'SignOfTheCross':
            if (self.decade == 0):
                prayer='Our Father'
            else:
                return {}

        elif self.prayer == 'Our Father':
            prayer='Hail Mary'

        elif self.prayer == 'Hail Mary':
            prayer='Creed'

        elif self.prayer == 'Creed':
            decade += 1
            prayer ='Eternal Father'

        elif self.prayer == 'Eternal Father':
            prayer = 'For the sake'


        elif self.prayer == 'For the sake':
            if (counter >= 10):
                if (decade >= 5):
                    prayer='Holy God'
                    counter = 0
                else:
                    decade += 1
                    prayer='Eternal Father'
            
        elif self.prayer == 'Holy God':
            if (counter < 3):
                prayer = 'Holy God'
            else:
                prayer='SignOfTheCross'

        if prayer != self.prayer:
            counter=0
                
        return DivineMercyTokenData(prayer, decade, counter)

            
            

    
        
     
