import numpy as np
def transform_cartesian_coordinates(Q,T):
    """
    Apply a tranformation matrix to all the coordinates
    in Q.

    Parameters:
    -----------------
    Q: coordinates matrix
    T: transformation matrix
    """
    def affine_transformation_multiplication(coordinates,T):
        return np.matmul(T,coordinates)   
     
    return np.apply_along_axis(affine_transformation_multiplication,2,Q,T)