import os.path


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
