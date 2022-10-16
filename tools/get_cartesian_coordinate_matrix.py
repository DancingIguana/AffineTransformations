import numpy as np
def get_cartesian_coordinate_matrix(N,M):
    cartesian_coordinates =  np.array([[(xi,(M-1)-yi,1) for xi in range(N)] for yi in range(M)])
    return cartesian_coordinates