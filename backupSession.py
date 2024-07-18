
from datetime import datetime

from tokenManager import *
from dbManager import DbManager


class BackupSession:

    def __init__(self, root_folder, client_id, user="postgres", password="1958"):
        self.client_id = client_id

        self.dbManager = DbManager(user, password, client_id)
        self.session_id = None

        self.ROOT_FOLDER = root_folder
        self.BACKUP_FOLDER = os.path.join(self.ROOT_FOLDER, client_id + "/")

    def create_folder(self):
        cur_date_time = datetime.now()
        filename_timestamp = cur_date_time.strftime("%d-%m-%Y_%H-%M-%S")
        cur_folder_name = os.path.join(self.BACKUP_FOLDER, filename_timestamp)
        create_folder(cur_folder_name)
        return cur_folder_name, cur_date_time

    def get_last_backup_session(self):
        last_session = self.dbManager.select_last_session()
        return last_session

    def add_backup_session(self, new_page_token, new_backup_time, new_backup_type):
        self.dbManager.insert_session(new_backup_time, new_page_token, new_backup_type)
        self.session_id = self.get_last_backup_session().id

    def add_new_change(self, new_metadata, new_session_id, new_file_ref, new_parent_id, new_name,
                       is_removed, new_file_id, new_size):
        self.dbManager.insert_changes(new_metadata, new_session_id, new_file_ref, new_parent_id, new_name,
                                      is_removed, new_file_id, new_size)

    def close_session(self):
        self.dbManager.commit_all()
        self.client_id = None
        self.dbManager = None
        self.session_id = None
        self.ROOT_FOLDER = None
        self.BACKUP_FOLDER = None
