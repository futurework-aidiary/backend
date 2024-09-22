class GetDiaryRequest:
    def __init__(self, user_id, date):
        self.user_id = user_id
        self.date = date

    def to_dict(self):
        return {
            "userId": self.user_id,
            "date": self.date
        }

class GetDiaryResponse:
    def __init__(self, diary_id, user_id, date, context):
        self.diary_id = diary_id
        self.user_id = user_id
        self.date = date
        self.context = context


    def to_dict(self):
        return {
            "diaryId": self.diary_id,
            "userId": self.user_id,
            "date": self.date,
            "context": self.context
        }


class AiDiaryRequest:
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

class AiDiaryResponse:
    def __init__(self, diary_id, context):
        self.diary_id = diary_id
        self.context = context


    def to_dict(self):
        return {
            "diaryId": self.diary_id,
            "context": self.context
        }
