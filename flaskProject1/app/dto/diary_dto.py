class GetDiaryRequestDTO:
    def __init__(self, conversation_id, user_id, emo, weather):
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.emo = emo
        self.weather = weather

    def to_dict(self):
        return {
            "userId": self.user_id,
            "conversationId": self.conversation_id,
            "emo": self.emo,
            "weather": self.weather
        }

class GetDiaryResponseDTO:
    def __init__(self, diary_id, user_id, emo, weather, date, context):
        self.diary_id = diary_id
        self.user_id = user_id
        self.emo = emo
        self.weather = weather
        self.date = date
        self.context = context


    def to_dict(self):
        return {
            "diaryId": self.diary_id,
            "userId": self.user_id,
            "emo": self.emo,
            "weather": self.weather,
            "date": self.date,
            "context": self.context
        }


class AiDiaryRequestDTO:
    def __init__(self, diary_id, date, weather, emo, texts):
        self.diary_id = diary_id
        self.date = date
        self.weather = weather
        self.emo = emo
        self.texts = texts #list of texts


    def to_dict(self):
        return {
            "diary":{
            "diaryId": self.diary_id,
            "date": self.date,
            "weather": self.weather,
            "emo": self.emo
            },

            "texts": [{"text": text} for text in self.texts],
        }

class AiDiaryResponseDTO:
    def __init__(self, diary_id, context):
        self.diary_id = diary_id
        self.context = context


    def to_dict(self):
        return {
            "diaryId": self.diary_id,
            "context": self.context
        }
