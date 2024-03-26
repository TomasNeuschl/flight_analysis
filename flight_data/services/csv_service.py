import csv
from io import TextIOWrapper


class CSVService:
    @staticmethod
    def parse_data(csv_file):
        file = TextIOWrapper(csv_file.file, encoding='utf-8')
        reader = csv.reader(file)
        header = next(reader)
        parsed_data = []
        for row in reader:
            data = {header[i]: val for i, val in enumerate(row)}
            parsed_data.append(data)
        return parsed_data

