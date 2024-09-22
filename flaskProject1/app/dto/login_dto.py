class LoginRequestDTO:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
        }

class LoginResponse:
    def __init__(self):
        pass
    def to_dict(msg : str):
        return {"msg": msg}
