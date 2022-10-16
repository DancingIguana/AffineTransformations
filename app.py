import PySimpleGUI as sg
from affine_transformation import colored_affine_transformation
import cv2
import numpy as np
import os


sg.theme("DarkBlue1")
def load_image(values):
    filename = values["-FILE-"]
    if os.path.exists(filename):
        cv2_image = cv2.imread(values["-FILE-"])
        cv2_image = cv2.cvtColor(cv2_image,cv2.COLOR_RGB2BGR)

        RGB_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        imgbytes = cv2.imencode('.png', RGB_image)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

        return cv2_image


def apply_transformation(cv2_image,values):
    try:
        T = np.array([
            [float(values["-00-"]), float(values["-01-"]), float(values["-02-"])],
            [float(values["-10-"]), float(values["-11-"]), float(values["-12-"])],
            [float(values["-20-"]), float(values["-21-"]), float(values["-22-"])]
        ])
    except:
        return
    
    try:
        cv2_image.shape
    except:
        return
    
    #B
    transformed_image = colored_affine_transformation(cv2_image,T)

    cv2_image = transformed_image.astype("uint8")
    RGB_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    imgbytes = cv2.imencode('.png', RGB_image)[1].tobytes()
    window["-IMAGE2-"].update(data=imgbytes)
    
    return RGB_image


file_types = [
    ("JPEG",("*.jpg"),"*.jpg"),
    ("PNG",("*.png"),"*.png")
]
control_col = sg.Column([
    [sg.Text("Common transformations")],
    [
        sg.Button("Identity"),sg.Button("X-Axis Reflect"),sg.Button("Y-Axis Reflect")
    ],
    [
        sg.Button("Clockwise rotation (degrees)"),
        sg.Input(key = "-ROTDEG1-", size =(5,5)),
    ],
    [
        sg.Button("Scale (width,height)"),
        sg.Input(key = "-W-", size = (5,5)), sg.Input(key = "-H-", size = (5,5))
    ],
    [
        sg.Button("Shear in x (degrees)"),
        sg.Input(key = "-ROTDEG2-", size = (5,5))
    ],
    [
        sg.Button("Shear in y (degrees)"),
        sg.Input(key = "-ROTDEG3-", size = (5,5))
    ],
    [sg.Text("Transformation Matrix (numeric values only)")],
    [
        sg.Input(1,key = "-00-", size = (5,5)), 
        sg.Input(0,key = "-01-", size = (5,5)), 
        sg.Input(0,key = "-02-", size = (5,5))
    ],
    [
        sg.Input(0,key = "-10-", size = (5,5)), 
        sg.Input(1,key = "-11-", size = (5,5)), 
        sg.Input(0,key = "-12-", size = (5,5))
    ],
    [
        sg.Input(0,key = "-20-", size = (5,5)), 
        sg.Input(0,key = "-21-", size = (5,5)), 
        sg.Input(1,key = "-22-", size = (5,5))
    ],
    [sg.Button("Submit")]
    ])

image_col = sg.Column([
    [
        sg.Text("Image File"),
        sg.Input(size = (25,1), key = "-FILE-"),
        sg.FileBrowse(file_types = file_types),
        sg.Button("Load Image")
    ],
    [sg.Image(key="-IMAGE-"), sg.Image(key="-IMAGE2-")],
    [sg.Button("Save")]
    ])

layout = [[control_col,image_col]]

window = sg.Window("Affine Transformation", layout)
cv2_image = None
image = None
matrix = [ window["-00-"],
        window["-01-"],
        window["-02-"],
        window["-10-"],
        window["-11-"],
        window["-12-"],
        window["-20-"],
        window["-21-"],
        window["-22-"]]
numeric_input_buttons={
    "Clockwise rotation (degrees)" : ["-ROTDEG1-"],
    "Scale (width,height)": ["-W-","-H-"],
    "Shear in x (degrees)": ["-ROTDEG2-"],
    "Shear in y (degrees)": ["-ROTDEG3-"]}
while True:
    event, values = window.read(timeout = 50)
    if event == sg.WIN_CLOSED:
        break
    if event == "Load Image":
        cv2_image = load_image(values)

    if event == "Submit":

        image = apply_transformation(cv2_image,values)
        print(image)
            
    if event == "Identity":
        mat_vals = [1,0,0,0,1,0,0,0,1]
        for window_value,number in zip(matrix,mat_vals):
            window_value.update(number)
    
    if event == "X-Axis Reflect":
        mat_vals = [-1,0,0,0,1,0,0,0,1]
        for window_value,number in zip(matrix,mat_vals):
            window_value.update(number)
    
    
    if event == "Y-Axis Reflect":
        mat_vals = [1,0,0,0,-1,0,0,0,1]
        for window_value,number in zip(matrix,mat_vals):
            window_value.update(number)


    if event == "Clockwise rotation (degrees)":
        try:
            value = np.float(values["-ROTDEG1-"])
        except:
            continue
        
        theta = value*np.pi/180
        mat_vals = [np.cos(theta),np.sin(theta),0,-np.sin(theta),np.cos(theta),0,0,0,1]
        for window_value,number in zip(matrix,mat_vals):
            window_value.update(number)

    if event == "Scale (width,height)":
        try: 
            width = np.float(values["-W-"])
            height = np.float(values["-H-"])
        except:
            continue
    
        mat_vals = [width,0,0,0,height,0,0,0,1]
        for window_value,number in zip(matrix,mat_vals):
            window_value.update(number)

    if event == "Shear in x (degrees)":
        try:
            value = np.float(values["-ROTDEG2-"])
        except:
            continue
        
        theta = value*np.pi/180
        mat_vals = [1,np.tan(theta),0,0,1,0,0,0,1]
        for window_value,number in zip(matrix,mat_vals):
            window_value.update(number)
    
    if event == "Shear in y (degrees)":
        try:
            value = np.float(values["-ROTDEG3-"])
        except:
            continue
        theta = value*np.pi/180
        mat_vals = [1,0,0,np.tan(theta),1,0,0,0,1]
        for window_value,number in zip(matrix,mat_vals):
            window_value.update(number)

    if event == "Save":
        if image is not None:
            save_path = sg.popup_get_file("Save",save_as = True,no_window = True) + ".png"
            cv2.imwrite(save_path,image)
window.close()