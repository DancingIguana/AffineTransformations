import tools
import numpy as np

def affine_transformation(img:np.array, T:np.array):
    
    # Number of rows and columns
    M , N = img.shape[:2]

    # Center of the matrix/image
    Pc = np.array([
        (N-1)/2,(M-1)/2,1
    ])

    # Get the cartesian coordinates matrix from 0 to x and 0 to y
    A = tools.get_cartesian_coordinate_matrix(N=N,M=M)

    # Move the coordinates to the center of the axis
    Q = tools.center_cartesian_coordinates(cartesian_coord_matrix=A, Pc=Pc)

    # Apply the affine transformation matrix to the centered coordinates
    Qp = tools.transform_cartesian_coordinates(Q=Q, T=T)
    
    # Get the minimum box corners to use for the transformed image
    left_upper_corner, right_lower_corner = tools.get_minimum_box(Qp=Qp)

    # For all of the coordinates in the box calculate color value
    # by using the inverse transformation followed by bilinear interpolation
    
    #Inverse tranformation
    invT = np.linalg.inv(T)

    # Horizontal coordinates of the minimum box
    horizontal = np.arange(left_upper_corner[0], right_lower_corner[0]+1,1)

    # Vertical coordinates of the minimum box
    vertical = np.arange(left_upper_corner[1],right_lower_corner[1]-1,-1)

    # Minimum box canvas
    transformed_img = np.zeros((len(vertical), len(horizontal)))

    for ivp in vertical:
        for ihp in horizontal:
            # Find the corresponding row and column of the matrix doing the inverse transformation
            fih,fiv,_ = np.matmul(invT,np.array([ihp,ivp,1]))
            fih_np, fiv_np, _ = np.array([0,M-1,0]) + ((np.array([fih,fiv,1]) + np.array([Pc[0],Pc[1],0])))*(np.array([1,-1,1]))
            new_row = int(ivp - left_upper_corner[1])*-1
            new_col = int(ihp - left_upper_corner[0])

            # Perform bilinear interpolation given the row and column of the original image matrix (float value)
            transformed_img[new_row][new_col] = tools.bilinear_interpolation(x=fih_np, y=fiv_np, N=N, M=M, img=img)

    
    return transformed_img

def colored_affine_transformation(img, T):
    #B
    AT_img = np.array(affine_transformation(np.array(img[:,:,0]),T))
    y,x = AT_img.shape
    channels = np.zeros((y,x,3))
    channels[:,:,0] = AT_img
    for channel in [1,2]: #G,R
        channels[:,:,channel] = np.array(affine_transformation(np.array(img[:,:,channel]),T))

    return channels