import cv2
import dxcam
import numpy as np
import util

from ultralytics import YOLO


def main():
    model = YOLO('./weights/best.pt')
    
    camera = dxcam.create()
    window_region = util.get_window_region()
    camera.start(target_fps=30, region=window_region) 
        
    while (True):
        frame = camera.get_latest_frame()
        results = model(frame)
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Inference", cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
            
    camera.release()

    
if __name__ == '__main__':
    main()
    
    