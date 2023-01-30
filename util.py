import win32gui

def get_window_region(window_name="Don't Starve Together", offset=7):
    '''Get the screen coordinates of a window.
    
    Args:
        window_name: Name of the window.
        offset: Number of pixels to adjust for Window's borders.
        
    Returns:
        window_region: A tuple (left, top, right, bottom) corresponding 
          to the coordinates of the window. 
    '''
    window_handle = win32gui.FindWindow(None, window_name)
    window_rectangle = win32gui.GetWindowRect(window_handle)
    left = window_rectangle[0] + offset      
    top = window_rectangle[1] + offset + 25  # exclude title bar
    right = window_rectangle[2] - offset     
    bottom = window_rectangle[3] - offset
    window_region = (left, top, right, bottom)
    return window_region