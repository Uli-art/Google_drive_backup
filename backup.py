import io

from googleapiclient.http import MediaIoBaseDownload

from googleDriveAPI import *
from tokenManager import *
from helpers import create_folder
from constants import MIME_TYPES
from backupSession import BackupSession


class Backup:

    def __init__(self, user_google_drive_api: UserGoogleDriveAPI, root_folder):
        self.user_google_drive_api = user_google_drive_api
        self.ROOT_FOLDER = root_folder
        self.backup_session = None

    def full_backup(self):
        self.backup_session = self.create_backup_session()
        cur_folder_name, current_timestamp = self.backup_session.create_folder()
        self.backup_session.add_backup_session(
            self.user_google_drive_api.get_start_page_token(), current_timestamp, "full")
        file_list = self.user_google_drive_api.get_file_list()

        all_files = self.save_files(file_list, cur_folder_name)

        data = {"type": "full", "files": all_files}
        with open(os.path.join(cur_folder_name, "files.json"), "w") as files:
            files.write(json.dumps(data))
            files.close()
        self.backup_session.close_session()

    def incremental_backup(self):
        self.backup_session = self.create_backup_session()
        cur_folder_name, current_timestamp = self.backup_session.create_folder()
        last_session = self.backup_session.get_last_backup_session()

        file_list, next_page_token = self.user_google_drive_api.get_changes_list(
            last_session.page_token)

        self.backup_session.add_backup_session(next_page_token, current_timestamp, "incremental")

        all_files = self.save_files(file_list, cur_folder_name, False)

        data = {"type": "incremental", "files": all_files}

        with open(os.path.join(cur_folder_name, "files.json"), "w") as files:
            files.write(json.dumps(data))
            files.close()
        self.backup_session.close_session()

    @staticmethod
    def download_file(requests, file_name):
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=requests)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        fh.seek(0)

        with open(file_name, 'wb') as f:
            f.write(fh.read())
            f.close()

    def add_file_to_db(self, file, file_path):
        self.backup_session.add_new_change(file, self.backup_session.session_id, file_path, file['parents'][0],
                                           file['name'], False, file['id'], 0)

    def create_backup_session(self):
        client_id = self.user_google_drive_api.current_session.user_token_manager.get_creds().client_id
        return BackupSession(self.ROOT_FOLDER, client_id)

    def save_files(self, file_list, backup_path, is_full=True, all_files=None):
        if all_files is None:
            all_files = []
        all_files += file_list
        create_folder(backup_path)
        for file in file_list:
            if not is_full:
                file = file['file']
            file_mime_type = file['mimeType']
            file_id = file['id']
            if "application/vnd.google-apps" not in file_mime_type:
                requests = self.user_google_drive_api.get_media(file_id)
                file_name = os.path.join(backup_path, file_id + '.' + file['fullFileExtension'])
                self.download_file(requests, file_name)
                self.add_file_to_db(file, file_name)
            else:
                if file_mime_type == "application/vnd.google-apps.folder":
                    new_backup_path = backup_path + '/' + file_id
                    self.add_file_to_db(file, new_backup_path)
                    if is_full:
                        file_list = self.user_google_drive_api.get_file_list(file_id)
                        self.save_files(file_list, new_backup_path, is_full, all_files)
                else:
                    if file_mime_type in MIME_TYPES.keys():
                        export_mime_type, extension = MIME_TYPES[file_mime_type]
                        requests = self.user_google_drive_api.get_export(file_id, export_mime_type)
                        file_name = os.path.join(backup_path, file_id + extension)
                        self.download_file(requests, file_name)
                        self.add_file_to_db(file, file_name)
                    else:
                        print(f"Unsupported Google Docs type: {file_mime_type}")
        return all_files
