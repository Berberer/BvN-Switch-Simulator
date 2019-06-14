import numpy as np
from hopcroftkarp import HopcroftKarp

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
    A = traffic_matrix
    bpGraph = {}
    permutation_matrices = []


    for i in range(0,5): #Replace by while check when maxMatching works correctly
        print("\n")
        # 2. Bipartite matching
        # 2.1 create bipartite graph from traffic matrix
        for lineNum, line in enumerate(traffic_matrix):
            currDestinations = set()
            print(currDestinations)
            for elementNum, element in enumerate(line):
                if element > 0:
                    currDestinations.add(elementNum)

            bpGraph[lineNum] = currDestinations
        print(bpGraph)
        
        # 2.2 find maximum matching in the bipartite graph
        maxMatching = HopcroftKarp(bpGraph).maximum_matching()
        print(maxMatching)

        # 3. Schedule
        # 3.1 Construct permutation matrix
        # 3.2 Set weight according to minimum value of A according to M
        permutation_matrix = np.zeros((len(traffic_matrix),len(traffic_matrix)), dtype="int")
        weight = 1
        for src, dst in maxMatching.items():
            permutation_matrix[src][dst] = 1
            if weight > traffic_matrix[src][dst]:
                weight = traffic_matrix[src][dst]

        # 4. Update and loop
        # 4.1 Set A to A - weight*P(i) and i = i+1
        traffic_matrix = np.subtract(traffic_matrix,np.multiply(weight,permutation_matrix))
        print(traffic_matrix)

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
