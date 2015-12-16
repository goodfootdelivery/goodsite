import googlemaps

GKEY = 'AIzaSyAF5a1ktypMvsvnMMnoaFGHkmt_9vnWfok'

# Need To Add Exceptions for Invalid Addresses
# And Connection Issues


class Mapper(object):
    client = googlemaps.Client(key=GKEY)

    def __init__(self, orig, dest, md='transit'):
        self.dist_mat = self.client.distance_matrix(orig, dest, mode=md)
        # Distance In Km and Point Value
        self.__distance = self.dist_mat['rows'][0]['elements'][0]['duration']['text']
        self.__points = self.dist_mat['rows'][0]['elements'][0]['duration']['value']

    @property
    def dist(self):
        return self.__distance

    @property
    def pnts(self):
        return self.__points

    def prices(self, array):
        return [float(self.__points)*x for x in array]
