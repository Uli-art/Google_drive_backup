import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from helpers import create_folder


class TokenManager:

    def __init__(self, scopes, root_folder):
        self.SCOPES = scopes
        self.ROOT_FOLDER = root_folder
        self.CREDS_FILE = os.path.join(self.ROOT_FOLDER, "credentials.json")
        self.TOKEN_FILE = os.path.join(self.ROOT_FOLDER, "token.json")

        create_folder(self.ROOT_FOLDER)

    @staticmethod
    def refresh_access_token(creds):
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

    def get_creds(self):
        creds = None
        if os.path.exists(self.TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES)
        return creds

    def get_creds_from_app_flow(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.CREDS_FILE, self.SCOPES)
        creds = flow.run_local_server(port=0)
        return creds

    def form_token_json(self, creds):
        with open(self.TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    def get_client_id(self):
        with open(self.TOKEN_FILE, "r") as json_file:
            data = json.load(json_file)
            return data['client_id'] if 'client_id' in data.keys() else None
