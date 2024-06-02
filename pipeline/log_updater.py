import os
import csv
import datetime

class LogUpdater:
    """
    A class for updating logs with detected individuals' information.

    Methods:
    --------
    __init__()
        Initializes the LogUpdater object with the current datetime.
    get_log(frame_no, in_count, out_count, total_individuals_detected)
        Retrieves log information for a given frame and detection counts.
    get_formatted_log(frame_no, in_count, out_count, total_individuals_detected)
        Formats log information into a dictionary.
    write_to_csv(formatted_log, csv_file_path)
        Writes formatted log information to a CSV file.
    """
    def __init__(self) -> None: 
        self.current_datetime = datetime.datetime.now()  # Get the current datetime
 
    def get_log(self, frame_no, in_count, out_count, total_individuals_detected): 
        """
        Retrieves log information for a given frame and detection counts.

        Parameters:
        -----------
        frame_no : int
            The frame number.
        in_count : int
            Count of people entering.
        out_count : int
            Count of people leaving.
        total_individuals_detected : int
            Total number of individuals detected.

        Returns:
        --------
        tuple
            A tuple containing log information.
        """
        todays_date = self.current_datetime.strftime('%d-%m-%Y')  # Format the date as "day month year"
        current_time = self.current_datetime.strftime('%H:%M:%S')  # Format the time including seconds

        # Sample data for demonstration purposes(hard coded)
        person_trackid_in_out_time = {1: {'in_time': '09:20', 'out_time': '5:30'}}
        daily_hours_per_person = {1: '8.10 hours'}

        total_people_inside = max(0, in_count - out_count)

        return todays_date, current_time, frame_no, person_trackid_in_out_time, daily_hours_per_person, total_individuals_detected, total_people_inside
        
    def get_formatted_log(self, frame_no, in_count, out_count, total_individuals_detected):
        """
        Formats log information into a dictionary.

        Parameters:
        -----------
        frame_no : int
            The frame number.
        in_count : int
            Count of people entering.
        out_count : int
            Count of people leaving.
        total_individuals_detected : int
            Total number of individuals detected.

        Returns:
        --------
        dict
            A dictionary containing formatted log information.
        """
        todays_date, current_time, frame_no, person_trackid_in_out_time, daily_hours_per_person, total_individuals_detected, total_people_inside = self.get_log(frame_no, in_count, out_count, total_individuals_detected)
         
        formatted_log = {
            'todays_date': todays_date,
            'current_time': current_time,
            'frame_no': frame_no,
            'persons_trackid_in_out_time': person_trackid_in_out_time,
            'daily_hours_per_person': daily_hours_per_person,
            'total_individuals_detected': total_individuals_detected,
            'total_people_inside': total_people_inside,
        }
        return formatted_log

    def write_to_csv(self, formatted_log, csv_file_path):
        """
        Writes formatted log information to a CSV file.

        Parameters:
        -----------
        formatted_log : dict
            Dictionary containing formatted log information.
        csv_file_path : str
            Path to the CSV file where log information will be written.
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

        # Extract column names
        column_names = formatted_log.keys()

        file_exists = os.path.isfile(csv_file_path)

        try:
            with open(csv_file_path, 'a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=column_names)

                # Write column names only if the file doesn't exist or is empty
                if not file_exists or os.path.getsize(csv_file_path) == 0:
                    writer.writeheader()

                # Append formatted log to CSV file
                writer.writerow(formatted_log)

        except FileNotFoundError:
            print(f"Error: {csv_file_path} does not exist.")

