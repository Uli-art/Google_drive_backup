from tokenManager import *


class LoginSession:

    def __init__(self, token_manager: TokenManager):
        self.user_token_manager = token_manager

    def login(self):
        creds = self.user_token_manager.get_creds()
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.user_token_manager.refresh_access_token(creds)
            else:
                creds = self.user_token_manager.get_creds_from_app_flow()

            self.user_token_manager.form_token_json(creds)
        return creds

    # def logout(self):
