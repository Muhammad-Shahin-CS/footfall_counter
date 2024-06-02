# Import necessary modules
from flask import Flask, render_template, Response, jsonify
import os
import cv2
import pandas as pd

# Import custom modules
from pipeline.detector import Detector
from pipeline.footfall_counter import FootfallCounter
from pipeline.log_updater import LogUpdater
from utils import generate_video_frames_webcam
from config import MODEL_PATH, VIDEO_PATH, LOG_FILE_PATH

# Initialize Flask application
app = Flask(__name__)

# Initialize objects of custom classes
detector = Detector(MODEL_PATH)
footfall_counter = FootfallCounter()
log_updater = LogUpdater() 

# Define constants
blue_line_position = 0.37
line_size = 9
# Initialize variables for in and out counts
in_count = 0
out_count = 0

# Function to process video frames
def process_video():
    global in_count, out_count
    previous_counts = {}

    # Loop through each frame from the webcam video feed
    for frame_no, frame in generate_video_frames_webcam(VIDEO_PATH, start_frame=50, end_frame=4400):
        frame_no = frame_no-49
        frame = cv2.resize(frame, (853, 480)) # Resize the frame 
        detections_dict, total_individuals_detected = detector.do_predictions(frame)
        centroids = footfall_counter.get_centroids(detections_dict)
        frame = footfall_counter.draw_bounding_box_and_putext_id(frame, detections_dict, centroids)
        frame, line_coordinates = footfall_counter.draw_border(frame, blue_line_position, line_size)
        centroid_sides_dict = footfall_counter.find_centroids_side(centroids, line_coordinates)
        updated_counts, in_count, out_count = footfall_counter.update_counts(centroid_sides_dict, previous_counts, in_count, out_count)
        previous_counts = updated_counts
        annotated_frame = frame
        out_frame = footfall_counter.out_frame_show(annotated_frame, in_count, out_count)
        
        # Convert frame to JPEG
        ret, jpeg = cv2.imencode('.jpg', out_frame)
        frame_bytes = jpeg.tobytes()
        
        # Update and write log
        update_and_write_log(frame_no, in_count, out_count, total_individuals_detected)

        # Yield frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

# Function to update and write log
def update_and_write_log(frame_no, in_count, out_count, total_individuals_detected): 

    # Get formatted log 
    formatted_log = log_updater.get_formatted_log(frame_no, in_count, out_count, total_individuals_detected)
    
    # Write log to CSV 
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)  # Create directory if it doesn't exist
    log_updater.write_to_csv(formatted_log, LOG_FILE_PATH)


# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')


# Route for the video page
@app.route('/video')
def video():
    # Initial values for in_count and out_count
    in_count = 0
    out_count = 0
    return render_template('video.html', in_count=in_count, out_count=out_count)

# Route for the video feed
@app.route('/video_feed')
def video_feed():
    return Response(process_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route for fetching current counts
@app.route('/counts')
def counts():
    global in_count, out_count
    return jsonify({'in_count': in_count, 'out_count': out_count})


# Route for viewing logs
@app.route('/logs')
def logs():
    if not os.path.exists(LOG_FILE_PATH):
        return render_template('logs.html', tables="<p>Log file does not exist.</p>")

    # Read log file into DataFrame
    df = pd.read_csv(LOG_FILE_PATH)

    # Clean the DataFrame to remove unwanted characters
    df = df.applymap(lambda x: str(x).replace('\\n', '').replace('\\', '').replace("'", '').replace('{', '').replace('}', ''))

    # Convert DataFrame to HTML table without index
    tables = df.to_html(index=False, classes='table')

    return render_template('logs.html', tables=tables)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
