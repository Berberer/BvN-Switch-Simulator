import numpy as np

def gljd(traffic_matrix):
    permutation_matrices = []
    probabilities = []
    matrix_elements = []
    for x, line in enumerate(traffic_matrix):
        for y, element in enumerate(line):
            matrix_elements.append([element, x, y])
    matrix_elements = sorted(matrix_elements, reverse=True, key=lambda x: x[0])
    while len(matrix_elements) > 0:
        p = 0
        blocked_columns = []
        blocked_rows = []
        permutation_matrix = np.zeros(traffic_matrix.shape, dtype="int")
        for element in matrix_elements[:]:
            if (element[1] not in blocked_rows) and (element[2] not in blocked_columns):
                if p == 0:
                    p = element[0]
                matrix_elements.remove(element)
                blocked_rows.append(element[1])
                blocked_columns.append(element[2])
                permutation_matrix[element[1]][element[2]] = 1
        permutation_matrices.append(permutation_matrix)
        probabilities.append(p)
    return permutation_matrices, probabilities


def exact(traffic_matrix):
    # 1. Initialization
    i = 1
    bpGraph = {}
    permutation_matrices = []

    # 2. blow up traffic_matrix
    blow_up_factor = 10
    traffic_matrix = traffic_matrix * blow_up_factor
    traffic_matrix = np.round(traffic_matrix)

    while np.any(traffic_matrix):
        # 2. Bipartite matching
        # 2.1 create bipartite graph from traffic matrix
        for lineNum, line in enumerate(traffic_matrix):
            currDestinations = set()
            for elementNum, element in enumerate(line):
                if element > 0:
                    currDestinations.add(elementNum)

            bpGraph[lineNum] = currDestinations

        # 2.2 find maximum matching in the bipartite graph
        maxMatching = {}
        (maxMatching, a, u) = bipartiteMatch(bpGraph)

        # 3. Schedule
        # 3.1 Construct permutation matrix
        # 3.2 Set weight according to minimum value of A according to M
        permutation_matrix = np.zeros((len(traffic_matrix),len(traffic_matrix)), dtype="int")
        weight = 99999999999
        for dst,src in maxMatching.items():
            permutation_matrix[src][dst] = 1
            if weight > traffic_matrix[src][dst]:
                weight = traffic_matrix[src][dst]
        permutation_matrices.append(permutation_matrix)

        # 4. Update and loop
        # 4.1 Set A to A - weight*P(i) and i = i+1
        traffic_matrix = np.subtract(traffic_matrix,np.multiply(weight,permutation_matrix))

    probabilities = [1/len(permutation_matrices) for i in permutation_matrices]

    print("Probabilities are",probabilities)
    print("Permutation Matrices are",permutation_matrices)

    return permutation_matrices,probabilities

def qbvn(traffic_matrix):
    #TODO: Make this configurable?
    blow_up_factor = 10

    #Blow up matix and round to integers
    matrix = traffic_matrix * blow_up_factor
    matrix = np.round(matrix)

    size = len(traffic_matrix)
    permutation_matrices = []
    in_start = 0
    for i in range(blow_up_factor):
        permutation_matrix = np.zeros(matrix.shape, dtype="int")
        for in_counter in range(size):
            in_port = (in_start + in_counter) % size
            for out_port in range(size):
                #Is there still traffic for this out port and is out port not yet served?
                if matrix[in_port][out_port] > 0 and np.max(permutation_matrix[:,out_port]) == 0:
                    permutation_matrix[in_port][out_port] = 1
                    matrix[in_port][out_port] -=1
                    break
        permutation_matrices.append(permutation_matrix)
        in_start = (in_start + 1) % size
    permutation_matrices = np.array(permutation_matrices)
    unique, counts = np.unique(permutation_matrices,axis=0, return_counts=True)
    probabilities = counts / np.sum(counts)
    return unique, probabilities

# Algorithm 3
def double(traffic_matrix):
    # In this paper C is a cumulative request matrix measured over a period of time
    C = traffic_matrix
    # 1. Define A s.t. a_ij = floor(c_ij / T/N)
    N = len(C)
    # T = #of batches -> we only send 1 packet
    T = 1
    A = C * (N/T)
    A = np.floor(A)
    # We now color the graph iteratively, since mirko is too lazy to look for an appropirate algorithm, we use the matching one:
    # Each matching represents one color, after such a matching has been found, we remove the matching from the (multi-) graph and
    # look for a new matching


    # Create biparite multi graph from A
    bpGraph = {}
    for lineNum, line in enumerate(A):
        currDestinations = list()
        for elementNum, element in enumerate(line):
            for i in range(0, int(element)):
                currDestinations.append(elementNum)
        bpGraph[lineNum] = currDestinations

    permutation_matrices = []
    # As long as we did not split up A entirely
    while any (len(x) > 0 for x in bpGraph.values()):
        matching = {}
        (matching, a, u) = bipartiteMatch(bpGraph)
        # Each matching/color corresponds to a permutation matrix
        # Create permutation matrix and remove edge from biparite graph
        permutation_matrix = np.zeros(traffic_matrix.shape, dtype="int")
        for output_port, input_port in matching.items():
            permutation_matrix[input_port][output_port] = 1
            bpGraph[input_port].remove(output_port)
        permutation_matrices.append(permutation_matrix)

    # Now the final step will produce N arbitrary permutations:
    for counter in range(0, N):
        permutation_matrix = np.zeros(traffic_matrix.shape, dtype="int")
        free_destinations = list(range(0, N))
        for input_port in range(0 , N):
            output_port = np.random.choice(free_destinations)
            free_destinations.remove(output_port)
            permutation_matrix[input_port][output_port] = 1
        permutation_matrices.append(permutation_matrix)

    probabilities = [1/len(permutation_matrices) for i in permutation_matrices]
    return permutation_matrices, probabilities


# Copyright: http://code.activestate.com/recipes/123641-hopcroft-karp-bipartite-matching/
# Hopcroft-Karp bipartite max-cardinality matching and max independent set
# David Eppstein, UC Irvine, 27 Apr 2002
def bipartiteMatch(graph):
	'''Find maximum cardinality matching of a bipartite graph (U,V,E).
	The input format is a dictionary mapping members of U to a list
	of their neighbors in V.  The output is a triple (M,A,B) where M is a
	dictionary mapping members of V to their matches in U, A is the part
	of the maximum independent set in U, and B is the part of the MIS in V.
	The same object may occur in both U and V, and is treated as two
	distinct vertices if this happens.'''

	# initialize greedy matching (redundant, but faster than full search)
	matching = {}
	for u in graph:
		for v in graph[u]:
			if v not in matching:
				matching[v] = u
				break

	while 1:
		# structure residual graph into layers
		# pred[u] gives the neighbor in the previous layer for u in U
		# preds[v] gives a list of neighbors in the previous layer for v in V
		# unmatched gives a list of unmatched vertices in final layer of V,
		# and is also used as a flag value for pred[u] when u is in the first layer
		preds = {}
		unmatched = []
		pred = dict([(u,unmatched) for u in graph])
		for v in matching:
			del pred[matching[v]]
		layer = list(pred)

		# repeatedly extend layering structure by another pair of layers
		while layer and not unmatched:
			newLayer = {}
			for u in layer:
				for v in graph[u]:
					if v not in preds:
						newLayer.setdefault(v,[]).append(u)
			layer = []
			for v in newLayer:
				preds[v] = newLayer[v]
				if v in matching:
					layer.append(matching[v])
					pred[matching[v]] = v
				else:
					unmatched.append(v)

		# did we finish layering without finding any alternating paths?
		if not unmatched:
			unlayered = {}
			for u in graph:
				for v in graph[u]:
					if v not in preds:
						unlayered[v] = None
			return (matching,list(pred),list(unlayered))

		# recursively search backward through layers to find alternating paths
		# recursion returns true if found path, false otherwise
		def recurse(v):
			if v in preds:
				L = preds[v]
				del preds[v]
				for u in L:
					if u in pred:
						pu = pred[u]
						del pred[u]
						if pu is unmatched or recurse(pu):
							matching[v] = u
							return 1
			return 0

		for v in unmatched: recurse(v)


def qbvn_cover(traffic_matrix):
    #TODO: Make this configurable?
    blow_up_factor = 10

    #Blow up matix and round to integers
    matrix = traffic_matrix * blow_up_factor
    matrix = np.round(matrix)

    size = len(traffic_matrix)
    permutation_matrices = []
    in_start = 0
    while np.max(matrix) != 0:
        permutation_matrix = np.zeros(matrix.shape, dtype="int")
        for in_counter in range(size):
            in_port = (in_start + in_counter) % size
            for out_port in range(size):
                #Is there still traffic for this out port and is out port not yet served?
                if matrix[in_port][out_port] > 0 and np.max(permutation_matrix[:,out_port]) == 0:
                    permutation_matrix[in_port][out_port] = 1
                    matrix[in_port][out_port] -=1
                    break
        permutation_matrices.append(permutation_matrix)
        in_start = (in_start + 1) % size
    permutation_matrices = np.array(permutation_matrices)
    unique, counts = np.unique(permutation_matrices,axis=0, return_counts=True)
    probabilities = counts / np.sum(counts)
    return unique, probabilities
