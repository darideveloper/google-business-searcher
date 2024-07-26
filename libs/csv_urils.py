import csv


class CsvWriter():
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
    
    def write_row(self, mode: str, row: list):
        """ Write a row in the csv file
        
        Args:
            mode (str): Mode to write the row
            row (list): Row to write
        """
        
        with open(self.csv_path, mode, newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row)
            