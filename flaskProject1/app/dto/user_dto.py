#일단 getall은 안함


class AddUserRequestDTO:
    def __init__(self, name, username, password, phone_num, address, birth):
        self.name = name
        self.username = username
        self.password = password
        self.phone_num = phone_num
        self.address = address
        self.birth = birth

    def to_dict(self):
        return {
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "phoneNum": self.phone_num,
            "address": self.address,
            "birth": self.birth
        }

class AddUserResponseDTO:
    def __init__(self):
        pass
    def to_dict(msg : str):
        return {"msg": msg}


class GetUserRequestDTO:
    def __init__(self, user_id):
        self.user_id = user_id

    def to_dict(self):
        return {
            "userId": self.user_id
        }

class GetUserResponseDTO:
    def __init__(self, user_id, name, username, phone_num, address, birth):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.phone_num = phone_num
        self.address = address
        self.birth = birth

    def to_dict(self):
        return {
            "userId": self.user_id,
            "name": self.name,
            "username": self.username,
            "phoneNum": self.phone_num,
            "address": self.address,
            "birth": self.birth
        }

class DeleteUserRequestDTO:
    def __init__(self, user_id):
        self.user_id = user_id

    def to_dict(self):
        return {
            "userId": self.user_id
        }


class DeleteUserResponseDTO:
    def __init__(self):
        pass
    def to_dict(msg : str):
        return {"msg": msg}

class UpdateUserRequestDTO:
    def __init__(self, user_id, name, username, phone_num, address, birth):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.phone_num = phone_num
        self.address = address
        self.birth = birth

    def to_dict(self):
        return {
            "userId": self.user_id,
            "name": self.name,
            "username": self.username,
            "phoneNum": self.phone_num,
            "address": self.address,
            "birth": self.birth
        }


class UpdateUserResponseDTO:
    def __init__(self):
        pass
    def to_dict(msg : str):
        return {"str": msg}
