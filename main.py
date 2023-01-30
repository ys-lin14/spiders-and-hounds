import cv2
import dxcam
import numpy as np
import util

def main():
    camera = dxcam.create()
    window_region = util.get_window_region()
    camera.start(target_fps=30, region=window_region) 
    
    selective_search = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    
    while (True):
        frame = camera.get_latest_frame()
        
        # resize before performing selective search
        resized_frame = cv2.resize(frame, (128, 128))         
        selective_search.setBaseImage(resized_frame)
        selective_search.switchToSelectiveSearchFast()
        roi = selective_search.process()
            
        # convert bboxes back to original dimensions and visualize
        original_sized_bboxes = util.resize_bboxes(
            resized_frame, roi, frame.shape[0], frame.shape[1])
        
        #print(f'Selective Search returned {len(original_sized_bboxes)} boxes.')
        frame_copy = frame.copy()
        for i in range(0, min(len(original_sized_bboxes), 30)):
            x = int(original_sized_bboxes[i][0])
            y = int(original_sized_bboxes[i][1])
            w = int(original_sized_bboxes[i][2])
            h = int(original_sized_bboxes[i][3])
            cv2.rectangle(frame_copy, (x, y), (x+w, y+h), (0, 0, 255), 2)
        
        cv2.imshow("DST", frame_copy[:, :, ::-1])

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
    camera.release()

if __name__ == "__main__":
    main()
    
    