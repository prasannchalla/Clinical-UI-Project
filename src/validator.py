import csv

class Validator:
    def __init__(self, filename):
        self.__credentials = {}
        self.__user_roles = {}
        self.__load_credentials_data(filename)

    def validate_credentials(self, username, passsword):
        return self.__credentials.get(username) == passsword

    def get_user_role(self, username):
        return self.__user_roles.get(username)

    def __load_credentials_data(self, filename):
        with open(filename, newline='', encoding='utf-8') as csvfile:
            data = csv.DictReader(csvfile)
            for row in data:
                self.__credentials[row['username']] = row['password']
                self.__user_roles[row['username']] = row['role']
