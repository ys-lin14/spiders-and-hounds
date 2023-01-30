import cv2
import dxcam
import numpy as np
import util

def main():
    camera = dxcam.create()
    window_region = util.get_window_region()
    camera.start(target_fps=30, region=window_region) 
    
    while (True):
        frame = camera.get_latest_frame()
        cv2.imshow("DST", frame[:, :, ::-1])

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
    camera.release()

if __name__ == "__main__":
    main()
    
    