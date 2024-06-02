from ultralytics import YOLO
import cv2

class Detector:
    """
    A class used to represent a YOLO-based object detector.

    Attributes:
    -----------
    model : YOLO
        The YOLO model used for detection.
    detected_ids_list : list
        List to store detected object IDs.
    repeated_ids_check_list : list
        List to keep track of object IDs over consecutive frames for validation.
    total_people_detected : int
        Counter for the total number of unique people detected.

    Methods:
    --------
    __init__(model_path: str) -> None
        Initializes the detector with the given model path.
    do_predictions(frame)
        Performs detection on the given frame and returns the detected people and the total count of unique individuals detected.
    check_consecutive_values(sublist, num_of_consecutive_frames=3)
        Checks for IDs that appear in consecutive frames to ensure accurate counting.
    """

    def __init__(self, model_path: str) -> None: 
        self.model = YOLO(model_path)
        self.detected_ids_list = []
        self.repeated_ids_check_list = []
        self.base_id = 1
        self.reassigned_ids = {}
        self.total_people_detected = 0

    def do_predictions(self, frame):
        """
        Perform predictions on a given frame to detect objects, focusing on people.

        Parameters:
        -----------
        frame : numpy.ndarray
            The image frame on which predictions are to be made.

        Returns:
        --------
        person_detections_dict : dict
            A dictionary containing detections where keys are track IDs and values are lists containing class and bounding box.
        total_people_detected : int
            The total number of unique people detected.
        """
        results = self.model.track(frame, tracker="bytetrack.yaml", conf=0.5, classes=0, persist=True, verbose=False)
        for result in results:
            boxes_lst = result.boxes.xyxy.cpu().tolist() if result.boxes.xyxy is not None else []
            track_ids_lst = [int(id) for id in result.boxes.id.cpu().tolist()] if result.boxes.id is not None else []
            reassigned_track_ids_lst = self.re_assign_ids(track_ids_lst)
            labels_lst = [self.model.names[int(label)] for label in result.boxes.cls.cpu().tolist()] if result.boxes.cls is not None else []

            detected_ids_list = self.check_consecutive_values(reassigned_track_ids_lst, num_of_consecutive_frames=7)
            unique_detected_ids_list = [x for i, x in enumerate(detected_ids_list) if x not in detected_ids_list[:i]]
            self.total_people_detected = len(unique_detected_ids_list)

            detections_dict = {track_id: [cls, box] for track_id, cls, box in zip(reassigned_track_ids_lst, labels_lst, boxes_lst)}
            # person_detections_dict = {key: value for key, value in detections_dict.items() if 'person' in value[0]}
        return detections_dict, self.total_people_detected


    def re_assign_ids(self, ids_lst):
        """
        Reassigns IDs based on a given list of IDs.

        This method takes a list of lists of IDs and reassigns them unique IDs
        starting from a base ID.

        Parameters:
        - ids_lst (list of lists of int): A list containing lists of IDs to be reassigned.

        Returns:
        - reassigned_ids_result_lst (list of int): A list containing reassigned IDs.
        """ 
        reassigned_ids_result_lst = [] 
        for id in ids_lst:
            print(id)
            if id not in self.reassigned_ids:
                self.reassigned_ids[id] = self.base_id
                self.base_id += 1
            reassigned_ids_result_lst.append(self.reassigned_ids[id])
        print('self.reassigned_ids: ', self.reassigned_ids)
        return reassigned_ids_result_lst
        

    def check_consecutive_values(self, sublist, num_of_consecutive_frames=7):
        """
        Check for IDs that appear consistently over a specified number of consecutive frames.

        Parameters:
        -----------
        sublist : list
            List of IDs detected in the current frame.
        num_of_consecutive_frames : int, optional
            Number of consecutive frames to check for (default is 7).

        Returns:
        --------
        detected_ids_list : list
            List of IDs that have been detected consistently over the specified consecutive frames.
        """
        self.repeated_ids_check_list.append(sublist)

        if len(self.repeated_ids_check_list) == num_of_consecutive_frames + 1:
            self.repeated_ids_check_list.pop(0)

        if len(self.repeated_ids_check_list) == num_of_consecutive_frames:
            common_elements_code = "list(set(self.repeated_ids_check_list[0])"
            for i in range(1, num_of_consecutive_frames):
                common_elements_code += " & set(self.repeated_ids_check_list[{}])".format(i)
            common_elements_code += ")"
            common_elements = eval(common_elements_code)

            if common_elements:
                self.detected_ids_list.extend(common_elements)
        return self.detected_ids_list
