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
    A = traffic_matrix
    bpGraph = []

    # 2. Bipartite matching
    # 2.1 create bipartite graph from traffic matrix
    for lineNum, line in enumerate(traffic_matrix):
        bpGraphLine = []
        for elementNum, element in enumerate(line):
            if element > 0:
                bpGraphLine.append(1)
            else:
                bpGraphLine.append(0)
        bpGraph.append(bpGraphLine)
    # 2.2 find maximum matching in the bipartite graph
