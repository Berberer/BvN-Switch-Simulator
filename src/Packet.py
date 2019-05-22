class Packet(object):

    def __init__(self, source, destination, arrival_timestep):
        super(Packet, self).__init__()
        self._source = source
        self._destination = destination
        self._arrival_timestep = arrival_timestep

    def get_source(self):
        return self._source

    def get_destionation(self):
        return self._destination

    def get_arrival_timestep(self):
        return self._arrival_timestep

    def __str__(self):
        return "[{} -> {}, arrived at step {}]".format(
            self._source, self._destination, self._arrival_timestep
        )
