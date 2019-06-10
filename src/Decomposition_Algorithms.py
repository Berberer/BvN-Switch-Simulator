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
    #Step 1: Initialization. Set i = 1 and A = C(T)
    #Step 2: Bipartite match. Construct a bipartite graph from A where each nonzero entry of A has a corresponding edge in the graph. Find a maximum-size matching M of this graph.
    #Step 3: Schedule. Construct a permutation P(i) which corresponds to the matching M. Set the weight based on the minimum entry value of A corresponding to the edges of M:phi(i) = min(e,f) element M, a(e,f)
    #Setp 4: Update and loop. Set A = A - phi(i)*P(i) and i = i+1. If any nonzero entries of A remain, go to Step 2. Otherwise end.
