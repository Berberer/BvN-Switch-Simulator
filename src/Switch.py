class Switch(object):

    def __init__(self, inputs_number, outputs_number, schedule):
        super(Switch, self).__init__()
        self._schedule = schedule
        self._input_queues = []
        for input in range(inputs_number):
            self._input_queues.append([])
            for output in range(outputs_number):
                self._input_queues[input].append([]);

    def packets_arrive(self, packets):
        for packet in packets:
            self._input_queues[packet.get_source()][packet.get_destination()].append(packet)

    def forward_packets(self):
        permutation_matrix = self._schedule.get_random_permutation_matrix()
        for input, forward_plan in enumerate(permutation_matrix):
            output_list = forward_plan.tolist()
            if 1 in output_list:
                output = output_list.index(1)
                if (len(self._input_queues[input][output]) > 0):
                    print("Forwarded packet {}".format(self._input_queues[input][output][0]))
                    self._input_queues[input][output].pop(0)
