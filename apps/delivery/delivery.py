import googlemaps
import easypost

GKEY = 'AIzaSyAF5a1ktypMvsvnMMnoaFGHkmt_9vnWfok'
PRICE_VECTOR = [1.50, 2.34, 7.54]

# Need To Add Exceptions for Invalid Addresses
# And Connection Issues


class Mapper(object):
    _client = googlemaps.Client(key=GKEY)

    def __init__(self, orig, dest, md='transit'):
        self.dist_mat = self._client.distance_matrix(orig, dest, mode=md)
        # Distance In Km and Point Value
        self.__distance = self.dist_mat['rows'][0]['elements'][0]['duration']['text']
        self.__points = self.dist_mat['rows'][0]['elements'][0]['duration']['value']
        self.origin = orig
        self.destin = dest

    @property
    def one(self):
        addr = self.origin.split(',')
        return [x.strip() for x in addr]

    @property
    def two(self):
        addr = self.destin.split(',')
        return [x.strip() for x in addr]

    @property
    def dist(self):
        return self.__distance

    @property
    def pnts(self):
        return self.__points

    def prices(self, array):
        return [float(self.__points)*x for x in array]


tdot = '17 Raglan Ave, Toronto, ON M6C 2K7, Canada'
home = '48 Parkview Court, Chatham, ON N7M 6H9, Canada'
buxx = 'Nonsense'

if __name__ == '__main__':


    x = 29
    y = {'here': x}
    x += 23
    print x
    # y = {'here': x}
    print y['here']

