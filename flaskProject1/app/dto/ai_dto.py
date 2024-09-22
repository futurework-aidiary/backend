class MessageAiRequest:
    def __init__(self, context, text):
        self.context = context
        self.text = text

    def to_dict(self):
        return {
            "context": self.context,
            "text": self.text
        }

class MessageAiResponse:
    def __init__(self, context, botresponse):
        self.context = context
        self.botresponse = botresponse

    def to_dict(self):
        return {
            "context": self.context,
            "botresponse": self.botresponse
        }