class MessageRequestDTO:
    def __init__(self, conversation_id, user_id, timelog, text, image):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.timelog = timelog
        self.text = text
        self.image = image

    def to_dict(self):
        return {
            "conversationId": self.conversation_id,
            "userId": self.user_id,
            "timelog": self.timelog,
            "text": self.text,
            "image": self.image
        }

class MessageResponseDTO:
    def __init__(self, user_id, timelog, botresponse = None):
        self.user_id = user_id
        self.botresponse = botresponse if botresponse is not None else ""
        self.timelog = timelog

    def to_dict(self):
        return {
            "userId": self.user_id,
            "botresponse": self.botresponse,
            "timelog": self.timelog
        }

class ConversationRequestDTO:
    def __init__(self, user_id, emo, weather):
        self.user_id = user_id
        self.emo = emo
        self.weather = weather

    def to_dict(self):
        return {
            "userId": self.user_id,
            "emo": self.emo,
            "weather": self.weather
        }

class ConversationResponseDTO:
    def __init__(self, conversation_id, start_time):
        self.conversation_id = conversation_id
        self.start_time = start_time

    def to_dict(self):
        return {
            "conversationId": self.conversation_id,
            "startTime": self.start_time
        }

class ConversationEndRequest:
    def __init__(self, conversation_id, end_time):
        self.conversation_id = conversation_id
        self.end_time = end_time

    def to_dict(self):
        return {
            "conversationId": self.conversation_id,
            "endTime": self.end_time
        }

class ConversationEndResponse:
    def __init__(self, diary):
        self.diary = diary

    def to_dict(self):
        return {
            "diary": self.diary
        }


