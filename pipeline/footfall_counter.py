import cv2
import time

class FootfallCounter:
    def __init__(self) -> None:
        pass

    def get_centroids(self, detections_dict):
        """
        Extracts centroids from the detections.

        Parameters:
        -----------
        detections_dict : dict
            Dictionary containing detections with object IDs as keys and (class_name, bbox) as values.

        Returns:
        --------
        dict
            Dictionary containing object IDs as keys and centroids as values.
        """
        centroids = {}
        for obj_id, (class_name, bbox) in detections_dict.items():
            x1, y1, x2, y2 = map(int, bbox)
            centroid_x, centroid_y = (x1 + x2) // 2, (y1 + y2) // 2
            centroids[obj_id] = [centroid_x, centroid_y]
        return centroids

    def draw_bounding_box_and_putext_id(self, frame, detections_dict, centroids):
        """
        Draws bounding boxes, text ID, and centroids on the frame.

        Parameters:
        -----------
        frame : numpy.ndarray
            Frame on which to draw.
        detections_dict : dict
            Dictionary containing detections with object IDs as keys and (class_name, bbox) as values.
        centroids : dict
            Dictionary containing object IDs as keys and centroids as values.

        Returns:
        --------
        numpy.ndarray
            Frame with bounding boxes, text ID, and centroids drawn.
        """
        for obj_id, (label, bbox) in detections_dict.items():
            # Drawing bounding boxes
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 6)
            # Drawing text ID
            cv2.putText(frame, f"ID-{obj_id}", (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 4)
            # Drawing centroids
            if obj_id in centroids:
                centroid = centroids[obj_id]
                cv2.rectangle(frame, (centroid[0] - 5, centroid[1] - 5), (centroid[0] + 5, centroid[1] + 5), (0, 255, 0), -1)
        return frame

    def draw_border(self, frame, blue_line_position, line_size):
        """
        Draws a vertical line on the frame.

        Parameters:
        -----------
        frame : numpy.ndarray
            Frame on which to draw.
        blue_line_position : float
            Position of the blue line as a fraction of the frame width.
        line_size : int
            Thickness of the line.

        Returns:
        --------
        tuple
            Frame with the line drawn and its coordinates.
        """
        height, width, _ = frame.shape
        x_blue = int(width * blue_line_position)
        cv2.line(frame, (x_blue, 0), (x_blue, height), (255, 255, 255), line_size)
        return frame, {'start': (x_blue, 0), 'end': (x_blue, height)}

    def find_centroids_side(self, centroids, line_coordinates):
        """
        Determines the side of the line each centroid is on.

        Parameters:
        -----------
        centroids : dict
            Dictionary containing object IDs as keys and centroids as values.
        line_coordinates : dict
            Dictionary containing the coordinates of the line.

        Returns:
        --------
        dict
            Dictionary containing object IDs as keys and their side ('left', 'right', or 'on the line') as values.
        """
        x_blue = line_coordinates['start'][0]
        centroid_sides_dict = {}
        for obj_id, (cx, cy) in centroids.items():
            if cx < x_blue:
                centroid_sides_dict[obj_id] = "left"
            elif cx > x_blue:
                centroid_sides_dict[obj_id] = "right"
            else:
                centroid_sides_dict[obj_id] = "on the line"
        return centroid_sides_dict

    def update_counts(self, centroid_sides_dict, previous_counts, in_count, out_count):
        """
        Updates in and out counts based on centroid movements.

        Parameters:
        -----------
        centroid_sides_dict : dict
            Dictionary containing object IDs as keys and their side ('left', 'right', or 'on the line') as values.
        previous_counts : dict
            Dictionary containing previous centroid sides for each object ID.
        in_count : int
            Current count of individuals entering.
        out_count : int
            Current count of individuals exiting.

        Returns:
        --------
        tuple
            Updated dictionaries for centroid sides and counts.
        """
        updated_counts = {}
        for obj_id, side in centroid_sides_dict.items():
            if obj_id not in previous_counts:
                previous_counts[obj_id] = []
            sides_list = previous_counts[obj_id]
            if not sides_list or sides_list[-1] != side:
                sides_list.append(side)
            if len(sides_list) == 2:
                if sides_list == ['left', 'right']:
                    out_count += 1
                    sides_list.clear()
                elif sides_list == ['right', 'left']:
                    in_count += 1
                    sides_list.clear()
            updated_counts[obj_id] = sides_list
        return updated_counts, in_count, out_count

    def out_frame_show(self, frame, in_count, out_count):
        """
        Adds text to the frame showing the current in and out counts.

        Parameters:
        -----------
        frame : numpy.ndarray
            Frame on which to add text.
        in_count : int
            Current count of individuals entering.
        out_count : int
            Current count of individuals exiting.

        Returns:
        --------
        numpy.ndarray
            Frame with text added.
        """
        cv2.putText(frame, f"IN: {in_count}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 0, 255), 3, cv2.LINE_AA)
        cv2.putText(frame, f"OUT: {out_count}", (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 0, 255), 3, cv2.LINE_AA)
        return frame
