class MessageRequestDTO:
    def __init__(self, message_id, conversation_id, user_id, timelog, text, image):
        self.message_id = message_id
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
    def __init__(self, user_id, botresponse, timelog):
        self.user_id = user_id
        self.botresponse = botresponse
        self.timelog = timelog

    def to_dict(self):
        return {
            "userId": self.user_id,
            "botresponse": self.botresponse,
            "timelog": self.timelog
        }

class ConversationRequestDTO:
    def __init__(self, user_id):
        self.user_id = user_id
    def to_dict(self):
        return {
            "userId": self.user_id
        }

class ConversationResponseDTO:
    def __init__(self, conversation_id, user_id, start_time, emotions, weather_options):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.start_time = start_time
        self.emotions = emotions  # list of emotions
        self.weather_options = weather_options  # list of weather options

    def to_dict(self):
        return {
            "conversation": {
                "conversationId": self.conversation_id,
                "userId": self.user_id,
                "startTime": self.start_time
            },
            "emotions": [{"emo": emo} for emo in self.emotions],
            "weather": [{"weather": weather} for weather in self.weather_options]
        }

class ConversationEndRequest:
    def __init__(self, conversation_id, end_time, weather, emo):
        self.conversation_id = conversation_id
        self.end_time = end_time
        self.weather = weather
        self.emo = emo

    def to_dict(self):
        return {
            "conversation": {
                "conversationId": self.conversation_id,
                "endTime": self.end_time,
            },
            "diary": {
                "weather": self.weather,
                "emo": self.emo
            }

        }

class ConversationEndResponse:
    def __init__(self):
        pass

    def to_dict(msg : str):
        return {
            "msg": msg}


