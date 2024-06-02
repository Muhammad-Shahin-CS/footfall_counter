import cv2
from vidgear.gears import VideoGear

def generate_video_frames_webcam(path, start_frame=1, end_frame=None):
    """
    Generate video frames from a webcam or video file.

    Parameters:
    -----------
    path : str
        Path to the webcam device or video file.
    start_frame : int, optional
        The starting frame number (default is 1).
    end_frame : int, optional
        The ending frame number (default is None).

    Yields:
    -------
    tuple
        A tuple containing the frame number and the frame itself.
    """
    # Open the video source
    cap = VideoGear(source=path).start() 
    frame_no = 0
    while True:
        # Read a frame
        frame = cap.read() 
        # Break the loop if no frame is retrieved
        if frame is None:
            break  
        frame_no += 1 
        # Yield the frame if it falls within the specified range
        if start_frame <= frame_no <= end_frame:
            yield frame_no, frame 
        # Break the loop if the end frame is reached
        if end_frame and frame_no >= end_frame:
            break 
    # Stop capturing from the video source
    cap.stop()


#  skip frames
# def generate_video_frames_webcam(path, start_frame=1, end_frame=None):
#     cap = VideoGear(source=path).start()
#     frame_no = 0
#     while True:
#         frame = cap.read()
#         if frame is None:
#             break
#         frame_no += 1
#         if frame_no >= start_frame and (frame_no % 1 == 1):
#             yield frame_no, frame
#         if end_frame and frame_no >= end_frame:
#             break
#     cap.stop()


# Generate video frames from an IP camera using RTSP protocol. 
# def generate_video_frames_ipcam(ip_path, start_frame=1, end_frame=None):
#     pass


