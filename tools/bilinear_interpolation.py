import numpy as np

def bilinear_interpolation(x,y,N,M,img):
    """
    Given the float values of the numpy matrix coordinates, 
    perform a bilinear interpolation by choosing the 4 corresponding
    pixels and performing the weighted average.

    Parameters
    ----------------------
    x: the x coordinate of the image pixel (may be float), 
        values from 0 to N-1
    y: the y coordinate of the image pixel (may be float), 
        values from M-1 to 0
    N: the number of rows in the matrix
    M: the number of columns in the matrix
    img: the original image matrix

    Returns
    ----------------------
    The color value of the bilinear interpolation
    """

    # Make the centers 0.5 instead of 0
    x += 0.5
    y += 0.5
    ih = int(x)
    iv = int(y)

    if not (0 <= y and y < M and 0 <= x and x < N):
        return 0

    # Choose pixels
    pixel_sets = {
        "A":[
            [[ih-1,iv-1],[ih,iv-1]],
            [[ih-1,iv],[ih,iv]]
            ],

        "B":[
            [[ih,iv-1],[ih+1,iv-1]],
            [[ih,iv],[ih+1,iv]]
            ],

        "C":[
            [[ih,iv],[ih+1,iv]],
            [[ih,iv+1],[ih+1,iv+1]]
            ],

        "D":[
            [[ih-1,iv],[ih,iv]],
            [[ih-1,iv+1],[ih,iv+1]]
            ]
    }

    # If we're in the edges of the image, don't choose inexistent pixels
    if ih == 0:
        pixel_sets["A"][0][0][0] = ih
        pixel_sets["A"][1][0][0] = ih

        pixel_sets["D"][0][0][0] = ih
        pixel_sets["D"][1][0][0] = ih

    elif ih == N-1:
        pixel_sets["B"][0][1][0] = ih
        pixel_sets["B"][1][1][0] = ih

        pixel_sets["C"][0][1][0] = ih
        pixel_sets["C"][1][1][0] = ih
    
    if iv == 0:
        pixel_sets["A"][0][0][1] = iv
        pixel_sets["A"][0][1][1] = iv

        pixel_sets["B"][0][0][1] = iv
        pixel_sets["B"][0][1][1] = iv

    elif iv == M-1:
        pixel_sets["C"][1][0][1] = iv
        pixel_sets["C"][1][1][1] = iv

        pixel_sets["D"][1][0][1] = iv
        pixel_sets["D"][1][1][1] = iv

    
    # Get the decimal part of the pixel
    x_decimal_part = x % 1
    y_decimal_part = y % 1
    if x_decimal_part == 0.5 and y_decimal_part == 0.5:
        return img[iv][ih]
   

    if x_decimal_part < 0.5:
        if y_decimal_part < 0.5:
            pixels = pixel_sets["A"]
        else:
            pixels = pixel_sets["D"]
    else:
        if y_decimal_part < 0.5:
            pixels = pixel_sets["B"]
        else:
            pixels = pixel_sets["C"]

    deltah = abs(x_decimal_part - 0.5)
    deltav = abs(y_decimal_part - 0.5)

    p1 = img[pixels[0][0][1]][pixels[0][0][0]]
    p2 = img[pixels[0][1][1]][pixels[0][1][0]]
    p3 = img[pixels[1][0][1]][pixels[1][0][0]]
    p4 = img[pixels[1][1][1]][pixels[1][1][0]]

    pixel_values = np.array([
        [p1, p2],
        [p3, p4]
    ]
    )
    a = np.array([[1-deltav,deltav]])
    b = np.array([
        [1-deltah],
        [deltah]
    ])
    return np.matmul(np.matmul(a,pixel_values),b)[0][0]
