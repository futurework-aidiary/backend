from flask import request

from .models import *

# 외부 AI 모델 API URL
AI_API_URL = "http://localhost:5000"

def get_message(conversation_id, message_id):
    try:

        # 데이터베이스에서 user_id로 메시지 데이터를 가져옴
        conv = Conversations.query.filter_by(conversation_id=conversation_id).first()

        msg = Messages.query.filter_by(message_id=message_id).first()

        if not conv:
            return None, "Conversation not found"
        if not msg:
            return None, "Message not found"



        # AI 모델 인스턴스에 메시지를 전송
        payload = {"context": conv.context, "text": msg.text}

        ai_response = {"context": "업데이트문맥", "botresponse": "응답"} #request.post(AI_API_URL, json=payload)


        return ai_response

        # 외부 API에서 응답 받음
        #if ai_response.status_code == 200:
         #   return ai_response.json()
        #else:
         #   return None, "Failed to get response from AI instance"

    except Exception as e:
        return None, str(e)



def make_diary(conv, diary_id):
    try:

        # 메시지 데이터를 가져옴
        messages = Messages.query.filter_by(conversation_id=conv.conversation_id).all()

        if not messages:
            return None, "Messages not found"

        # diary와 message 배열 구성
        diary_data = Diary.query.filter_by(diary_id=diary_id).first()


        # 메시지 데이터를 JSON 형식으로 구성
        message_list = [{"text": msg.text} for msg in messages]

        # 전체 페이로드 구성
        payload = {
            "diary": diary_data,
            "message": message_list
        }

        # AI 모듈에 요청을 전송
        ai_response = request.post(AI_API_URL, json=payload)

        # AI 모듈의 응답 처리
        if ai_response.status_code == 200:
            return ai_response.json(), None
        else:
            return None, "Failed to get response from AI instance"

    except Exception as e:
        return None, str(e)