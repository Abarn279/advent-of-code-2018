import os.path

class FileImporter:
    @staticmethod
    def get_input(file_name):
        inp_str = ""
        file_name = os.path.dirname(__file__) + file_name
        with open(file_name, "r") as fopen:
            for line in fopen:
                inp_str += line
        return inp_str
                