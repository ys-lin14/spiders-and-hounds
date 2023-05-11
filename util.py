import albumentations
import numpy as np
import win32gui

def get_window_region(window_name="Don't Starve Together", offset=7):
    """Get the screen coordinates of a window.
    
    Args:
        window_name: Name of the window.
        offset: Number of pixels to adjust for Window's borders.
        
    Returns:
        window_region: A tuple (left, top, right, bottom) corresponding 
          to the coordinates of the window. 
    """
    window_handle = win32gui.FindWindow(None, window_name)
    window_rectangle = win32gui.GetWindowRect(window_handle)
    left = window_rectangle[0] + offset      
    top = window_rectangle[1] + offset + 25  # exclude title bar
    right = window_rectangle[2] - offset     
    bottom = window_rectangle[3] - offset
    window_region = (left, top, right, bottom)
    return window_region

# adapted from https://sheldonsebastian94.medium.com/resizing-image-and-bounding-boxes-for-object-detection-7b9d9463125a
def resize_image(img_arr, bboxes, h, w):
    """
    Args:
        img_arr: original image as a numpy array
        bboxes: bboxes as numpy array where each row is 
          'x_min', 'y_min', 'x_max', 'y_max', 'class_id'
        h: resized height dimension of image
        w: resized weight dimension of image
    
    Returns: 
        transformed: dictionary containing 
          {image:transformed, bboxes:['x_min', 'y_min', 'x_max', 'y_max', 'class_id']}
    """
    # create resize transform pipeline
    transform = albumentations.Compose(
        [albumentations.Resize(height=h, width=w, always_apply=True)],
        bbox_params=albumentations.BboxParams(format='coco'))

    # pad bboxes with a column of ones (class labels) to visualize selective search results 
    if (bboxes.shape[1] == 4):
        padded_bboxes = np.c_[ bboxes, np.ones(bboxes.shape[0]) ]
        transformed = transform(image=img_arr, bboxes=padded_bboxes)
    elif (bboxes.shape[1] == 5):
        transformed = transform(image=img_arr, bboxes=bboxes)

    return transformed

def resize_bboxes(img_arr, bboxes, h, w):
    resized_bboxes = resize_image(img_arr, bboxes, h, w)['bboxes']
    return resized_bboxes
    