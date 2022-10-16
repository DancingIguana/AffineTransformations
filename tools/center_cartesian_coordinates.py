import numpy as np
def center_cartesian_coordinates(cartesian_coord_matrix, Pc):
    # Center the coordinates
    return cartesian_coord_matrix - np.array([Pc[0],Pc[1],0])