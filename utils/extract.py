from extract_utils import *


def process_files_in_directory(directory_path):
    """
    This function processes every file in the given directory.
    :param directory_path: Path to the directory containing the files.
    """
    print("---------------DIR: " + str(directory_path))
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            try:
                extract_info(file_path, '../data/processed_docs')
                print("success: " + str(filename))
            except:
                print("ERROR ----- ERROR:" + str(filename))




def perform_action_on_folders(directory):
    for foldername in os.listdir(directory):
        path = os.path.join(directory, foldername)
        if os.path.isdir(path):
            process_files_in_directory(path)

# Specify the root directory to start from
directory_path = '../data/documents'
perform_action_on_folders(directory_path)

