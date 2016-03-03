#
#       API Parcel
#
#               Tue  1 Mar 21:10:18 2016
#

from django.db import models
from api.delivery import TEST_EP_KEY

#
#       Parcel Model
#
class Parcel(models.Model):
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()

    def __str__(self):
        return '%f" x %f" x %f", %foz' % \
            (self.length, self.width, self.height, self.weight)

    def easypost(self):
        return {
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'weight': self.weight
        }
