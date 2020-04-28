import requests
from pgtoolbox import db_toolbox as pgtb
from flask import request
import json


class Authenticc:
    def __init__(self):
        self._reset_attributes()

    def _reset_attributes(self):
        self._schema = "fantasy_pi_schema"
        self._users_table = "users"
        self._api_token = ""
        self._validator_url = "https://usecredo.com/user"
        self._response = {}
        self._user_credentials = {}
        self._user_data = {}
        self._is_third_party_authenticated = False
        self._is_authenticated = False
        self._is_existing_user = False

    def _get_token(self):
        if False:
            self._api_token = request.headers.get("api_token")
            # this is here for testing purposes
        self._api_token = "P4uzp3idyhLKjz4VM3OgoUEc2cL5M2nx2vAtMxyy6MG5iQPDDjEfmeAFKmQaKn9Oua3gPbqIUFhBJE1wRKdq6GtOFJljLqfmDkV2Vg4KgKyRGyzPeh2xCVOBwolv9PaRhJXLu2VB0gDFmUMTP2fFljkh0qOw5GoR4MkzSdvxcY3reCh31fWxsRLo5mD0dBHqXGurQyKWSSGAYAtunUC3nnyP9FjvIQ2GTC3nqPEOD4hcDWVoKmt6LTHrziGfJfie"

    def login_user(self, called_function):
        def inner_function(*args, **kwargs):
            def validate_token():
                self._response = requests.get(
                    self._validator_url,
                    headers={"Authorization": f"Bearer {self._api_token}"},
                )
                if self._response.json().get("username"):
                    self._is_third_party_authenticated = True
                    self._user_credentials = {
                        "email": self._response.json()["username"]
                    }
                    self._user_credentials = {"email": "penis@pinaha.com"}
                else:
                    # Redirect to credo
                    self._is_third_party_authenticated = False

            def check_database():
                user_data = db_con.read_query(
                    f"""
                    select 
                        user_id, 
                        email 
                    from {self._schema}.{self._users_table} 
                    where email = '{self._user_credentials['email']}'
                    """
                )
                print("user data is ", user_data)
                if user_data:
                    # If there is user_data, it means it is already existing and also authenticated consequently
                    # Therefore we fill the _user_credentials dict with the info from the db.
                    self._is_authenticated = True
                    self._is_existing_user = True
                    self._user_credentials = {
                        "user_id": user_data[0][0],
                        "email": user_data[0][1],
                        "is_authenticated": self._is_authenticated,
                        "is_existing_user": self._is_existing_user,
                    }
                else:
                    # If there is no user_data, it means there is no user in the db and we need to
                    # create an entry, since it is already authenticated on the credo side.
                    self._is_authenticated = True
                    self._is_existing_user = False
                    # here we just insert the entry in the db
                    query = f"""
                    insert into fantasy_pi_schema.users(email) 
                        values ( 
                            '{self._user_credentials['email']}'
                        )
                     """
                    db_con.execute_query(query)
                    db_con.commit_changes()
                    query = f"""
                        select 
                            user_id, 
                            email 
                        from fantasy_pi_schema.users 
                        where email = '{self._user_credentials['email']}' 
                     """
                    user_data = db_con.read_query(query)
                    print(user_data)
                    self._user_credentials = {
                        "user_id": user_data[0][0],
                        "email": user_data[0][1],
                        "is_existing_user": self._is_existing_user,
                        "is_authenticated": self._is_authenticated,
                    }
                    print(self._user_credentials)

            self._reset_attributes()
            db_con = pgtb.connect_to_database()
            self._get_token()
            validate_token()

            if self._is_third_party_authenticated:
                check_database()
            else:
                pass
                # else: send to credo

            # This is where we call the funciton that has been decorated
            return_data = called_function(*args, **kwargs)
            # This is where we add the extra credentials
            return_data_json = return_data.get_json()
            return_data_json["user_credentials"] = self._user_credentials
            # Set as string the json
            return_data.set_data(
                json.dumps(return_data_json, indent=2, separators=(",", ": "))
            )
            return return_data

        return inner_function

    def get_user_credentials(self):
        return self._user_credentials
