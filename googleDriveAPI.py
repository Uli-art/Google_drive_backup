
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from loginSession import LoginSession


class UserGoogleDriveAPI:

    def __init__(self, session: LoginSession):
        self.current_session = session
        self.service = build("drive", "v3", credentials=self.current_session.user_token_manager.get_creds())

    def get_start_page_token(self):
        try:
            results = (
                self.service.changes()
                .getStartPageToken()
                .execute()
            )

            start_page_token = results.get("startPageToken")

            if not start_page_token:
                raise Exception("Can not get start page token")

            return start_page_token

        except HttpError as error:
            raise Exception(error)

    def get_file_list(self, folder_id=None):
        if folder_id:
            query = f"'{folder_id}' in parents and trashed = false"
        else:
            query = "'root' in parents and trashed = false"
        try:
            results = (
                self.service.files()
                .list(q=query, fields='*')
                .execute()
            )

            files_list = results.get("files", [])

            while results.get("nextPageToken"):
                next_page_token = results.get("nextPageToken")
                results = (
                    self.service.files()
                    .list(pageToken=next_page_token, q=query, fields='*')
                    .execute()
                )
                files_list += results.get("files", [])

            return files_list
        except HttpError as error:
            raise Exception(error)

    def get_changes_list(self, page_token):
        try:
            results = (
                self.service.changes()
                .list(pageToken=page_token, includeRemoved=False, fields='*')
                .execute()
            )

            files_list = results.get("changes", [])

            while results.get("nextPageToken"):
                next_page_token = results.get("nextPageToken")
                results = (
                    self.service.files()
                    .list(pageToken=next_page_token, includeRemoved=False, fields='*')
                    .execute()
                )
                files_list += results.get("changes", [])

            new_start_page_token = results.get("newStartPageToken")
            return files_list, new_start_page_token
        except HttpError as error:
            raise Exception(error)

    def get_media(self, file_id):
        try:
            results = (
                self.service.files()
                .get_media(fileId=file_id)
            )

            return results
        except HttpError as error:
            raise Exception(error)

    def get_export(self, file_id, file_mime_type):
        try:
            results = (
                self.service.files()
                .export(fileId=file_id, mimeType=file_mime_type)
            )

            return results
        except HttpError as error:
            raise Exception(error)
