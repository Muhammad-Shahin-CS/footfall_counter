Footfall Counter with Object Detection
=======================================


Overview
--------
This project implements a footfall counter using object detection techniques. It detects individuals in a video stream, tracks their movements, and counts the number of people entering and exiting a specified area.


Features
--------
- Real-time object detection using YOLOv8 model.
- Footfall counting based on centroid tracking.
- Ability to process video streams from webcams or video files.
- Logging of footfall data to a CSV file.
- Adjustable parameters for line position, line size, frames, log_storage etc.


Requirements
------------
- Python 3.x
- OpenCV
- Ultralytics 
- VidGear
- flask

Installation
------------
1. Clone the repository: 
2. Install the required dependencies:

Usage
-----
1. Make sure the model weights are placed in the designated directory (`models/`). 
2. Run the `main.py` script: 
3. Adjust the parameters as needed (e.g., video source, thresholds, etc.) in the `main.py` file. 
4. (Optional) If you want to view the output via a Flask web interface, run the `server.py` script:
This will start a Flask server, and you can view the output in a web browser by navigating to `http://localhost:5000`.

Configuration
-------------
- `config.py`: Contains project configuration settings such as model paths, video paths, log file paths, etc.

Project Structure
-----------------
- `main.py`: Entry point of the application, contains the main logic.
- `detector.py`: Class for performing object detection using YOLOv5.
- `footfall_counter.py`: Class for counting footfalls and tracking centroids.
- `log_updater.py`: Class for updating and writing footfall data to a CSV file.
- `utils.py`: Utility functions for generating video frames and other helper functions.
- `config.py`: Configuration settings for the project.
- `models/`: Directory for storing model weights.
- `logs/`: Directory for storing log files.

License
-------
This project is licensed under the MIT License - see the LICENSE file for details.

   