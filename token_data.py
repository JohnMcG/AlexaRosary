"""
Declaration of a class corresponding to the data stored in the token for a prayer
"""

from __future__ import print_function
import struct


PRAYER_TYPE_MAPPING={
    'Rosary': 'r'
    }

MYSTERY_MAPPING={
    'Joyful':'j',
    'Sorrowful':'s',
    'Glorious':'g',
    'Luminous':'l'
}

PRAYER_MAPPING={
    'Creed':'c',
    'Our Father':'o',
    'Hail Mary':'h',
    'Glory Be':'g',
    'Fatima Prayer':'f',
    'Hail Holy Queen':'q'
}

AUDIO_MAPPING={
    'Creed':'https://s3.amazonaws.com/rosary-files/audio/prayers/Creed',
    'Our Father':'https://s3.amazonaws.com/rosary-files/audio/prayers/Our+Father',
    'Hail Mary':'https://s3.amazonaws.com/rosary-files/audio/prayers/Hail+Mary',
    'Glory Be':'https://s3.amazonaws.com/rosary-files/audio/prayers/Glory+Be',
    'Fatima Prayer':'https://s3.amazonaws.com/rosary-files/audio/prayers/Fatima+Prayer',
    'Hail Holy Queen':'https://s3.amazonaws.com/rosary-files/audio/prayers/Hail+Holy+Queen'
    }

FORMAT='15p15p15pll'

class TokenData:
    prayer_type='Rosary'
    mysteries='Joyful'
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
        print(parts)
        return self(parts[0],parts[1],parts[2],parts[3],parts[4])

    def get_audio(self):
        return AUDIO_MAPPING[self.prayer]

    def get_token(self):
        return struct.pack(FORMAT, self.prayer_type,
                           self.mysteries,
                           self.prayer,
                           self.decade,
                           self.counter)

    def get_next(self):
        if self.prayer_type == "Rosary":
            return self._get_next_rosary()

    def _get_next_rosary(self):
        if self.prayer=='Hail Holy Queen':
            return {}

        prayer_type=self.prayer_type
        mysteries=self.mysteries
        prayer=self.prayer
        counter=self.counter+1
        decade=self.decade
        
        if self.prayer=='Creed':
            prayer='Our Father';            

        elif self.prayer=='Our Father':
            prayer='Hail Mary'

        elif self.prayer=='Hail Mary':
            if (self.decade == 0 and counter >= 3) or counter >= 10:
                prayer='Glory Be'
                
        elif self.prayer=='Glory Be':
            prayer='Fatima Prayer'

        elif self.prayer=='Fatima Prayer':
            if self.decade == 5:
                prayer='Hail Holy Queen'
            else:
                prayer='Our Father'
                decade += 1
                print('Incremented decade to' + str(decade))

        if prayer != self.prayer:
            counter=0
                
        return TokenData(prayer_type, mysteries, prayer, decade, counter)
        
        
     
