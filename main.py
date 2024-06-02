# Import the libraries
import cv2 
 
# Import custom modules
from pipeline.detector import Detector
from pipeline.footfall_counter import FootfallCounter
from pipeline.log_updater import LogUpdater
from utils import generate_video_frames_webcam
from config import MODEL_PATH, VIDEO_PATH, VIDEO_PATH_1, LOG_FILE_PATH


# Initialize objects of custom classes
detector = Detector(MODEL_PATH)
footfall_counter  = FootfallCounter()
log_updater  = LogUpdater()


# Define constants/thresholds for footfall counting
border_line_position = 0.37
line_size = 9
in_count = 0
out_count = 0
previous_counts = {} 

# Function to update and write logs
def update_and_write_log(frame_no, in_count, out_count): 
    formatted_log = log_updater.get_formatted_log(frame_no, in_count, out_count, total_individuals_detected)
    log_updater.write_to_csv(formatted_log, LOG_FILE_PATH) 
    return formatted_log

# Loop through each frame from the webcam video feed
for frame_no, frame in generate_video_frames_webcam(VIDEO_PATH, start_frame=65, end_frame=4400): 
    print(f'\n\n\nframe No :  {frame_no}')    
    frame = cv2.resize(frame, (853, 480))  # Resize the frame
    # cv2.imwrite('frame.jpg',frame) 

    # Predictions module
    detections_dict, total_individuals_detected = detector.do_predictions(frame)
    print('detections_dict-- ', detections_dict)  
    
    # Footfall module
    centroids = footfall_counter.get_centroids(detections_dict)    
    frame = footfall_counter.draw_bounding_box_and_putext_id(frame, detections_dict, centroids)  
    frame, line_coordinates = footfall_counter.draw_border(frame, border_line_position , line_size) 
    centroid_sides_dict = footfall_counter.find_centroids_side(centroids, line_coordinates)
    updated_counts, in_count, out_count = footfall_counter.update_counts(centroid_sides_dict, previous_counts, in_count, out_count)
    previous_counts = updated_counts 
    # print("updated_counts: ",updated_counts) 
    # print("in_count: ", in_count)
    # print("out_count: ", out_count)  

    # Update and write logs
    formatted_log = update_and_write_log(frame_no, in_count, out_count)
    # print("formatted_log: ", formatted_log)  

    # Show annotated frame with in and out counts
    annotated_frame = frame
    out_frame = footfall_counter.out_frame_show(annotated_frame, in_count, out_count)
    cv2.imshow("out frame",cv2.resize(out_frame,(440,320))) 
    cv2.waitKey(1) 

  
   