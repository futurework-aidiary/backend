import requests

from .models import *

# 외부 AI 모델 API URL
AI_API_URL = "http://localhost:5001/ai"

def get_message(text):
    try:
        # AI 모델 인스턴스에 메시지를 전송
        payload = {"context": '', "text": text}

        msg_url = AI_API_URL + "/message"
        ai_response = requests.post(msg_url, json=payload)

        return ai_response.json()
        # 외부 API에서 응답 받음

    except Exception as e:
        return None, str(e)