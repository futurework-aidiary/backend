import requests

from .models import *

# 외부 AI 모델 API URL
AI_API_URL = "http://localhost:5001/futurework/aidiary"

def get_message(text):
    try:
        # AI 모델 인스턴스에 메시지를 전송
        payload = {"context": '', "text": text}

        ai_response = requests.post(AI_API_URL, json=payload)

        return ai_response.json()
        # 외부 API에서 응답 받음

    except Exception as e:
        return None, str(e)