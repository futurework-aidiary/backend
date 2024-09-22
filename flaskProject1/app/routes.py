from flask import Flask, jsonify, request

from app.routesAI import get_message
from .dto import *
from .models import *
from app import db, app
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime

from flask import Blueprint

# 블루프린트 정의
main_routes = Blueprint('main', __name__)

# 회원가입
@app.route('/user/add', methods=['POST'])
def add_user():
    # 1. JSON 데이터 가져오기
    data = request.get_json()

    # 2. DTO 객체 생성
    try:
        user_dto = AddUserRequestDTO(
            name=data.get('name'),
            username=data.get('username'),
            password=data.get('password'),
            phone_num=data.get('phoneNum'),
            address=data.get('address'),
            birth=data.get('birth')
        )
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

    hashed_password = generate_password_hash(user_dto.password)

    # 3. User 모델 객체 생성
    try:
        new_user = User(
            name=user_dto.name,
            username=user_dto.username,
            password=hashed_password,  # 비밀번호는 해시 처리 필요
            phone_num=user_dto.phone_num,
            address=user_dto.address,
            birth=user_dto.birth
        )

        # 4. 데이터베이스에 저장
        db.session.add(new_user)
        db.session.commit()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # 5. 성공 응답
    return jsonify(AddUserResponseDTO.to_dict("User added successfully")), 201

# 로그인
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    try:
        user_dto = LoginRequestDTO(
            username=data.get('username'),
            password=data.get('password'),
        )
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

        # 2. 데이터베이스에서 username으로 사용자 조회
    user = User.query.filter_by(username=user_dto.username).first()

    if user is None:
        return jsonify({"error": "Invalid username or password"}), 401

    # 3. 비밀번호 비교
    if not check_password_hash(user.password, user_dto.password):
        return jsonify({"error": "Invalid username or password"}), 401


    return jsonify(AddUserResponseDTO.to_dict("Login successful")), 200


# 선택 유저 조회
@app.route('/user/<int:userId>/get', methods=['GET'])

def get_user(userId):

    try:
        user_dto = GetUserRequestDTO(
            user_id=userId,
        )

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400


    user=User.query.filter_by(user_id=user_dto.user_id).first()
    if user is None:
        return jsonify({"error": "Invalid username or password"}), 401


    userResponse = GetUserResponseDTO(
        user_id=user.user_id,
        name=user.name,
        username=user.username,
        phone_num=user.phone_num,
        address=user.address,
        birth=user.birth
    )

    return jsonify(userResponse.to_dict()), 200


# 유저 정보 수정
@app.route('/user/<int:userId>/update', methods=['PUT'])
def update_user(userId):

    data = request.get_json()

    # 2. DTO 객체 생성
    try:
        user_dto = UpdateUserRequestDTO(
            name=data.get('name'),
            username=data.get('username'),
            phone_num=data.get('phoneNum'),
            address=data.get('address'),
            birth=data.get('birth')
        )

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

    # 3. user에 데이터 가져와 수정
    try:
        updateuser = User.query.get(user_dto.username)

        updateuser.name = user_dto.name
        updateuser.phone_num = user_dto.phone_num
        updateuser.address = user_dto.address
        updateuser.birth = user_dto.birth

        # 4. 데이터베이스에 저장
        db.session.commit()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # 5. 성공 응답
    return jsonify(UpdateUserResponseDTO.to_dict("User updated successfully")), 204

# 유저 정보 삭제
@app.route('/user/<int:userId>/delete', methods=['DELETE'])
def delete_user(userId):

    user = User.query.get(userId)

    try:
        db.session.delete(user)
        db.session.commit()

    except Exception as e:
        return jsonify({"error": str(e)})

    return jsonify(DeleteUserResponseDTO.to_dict("User deleted successfully")), 200

#대화세션 생성
@app.route('/conversation/<int:userId>', methods=['GET'])
def conversation_start(userId):

    try:
        get_user = ConversationRequestDTO(
            user_id=userId
        )

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

    user = User.query.filter_by(user_id=get_user.user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    try:

        new_conv = Conversations(

            user_id=user.user_id,
            start_time=datetime.now(),  # 현재 시간 대입
            end_time=None,
            context= None
        )

        # 4. 데이터베이스에 저장
        db.session.add(new_conv)
        db.session.commit()


    except Exception as e:

        return jsonify({"error": str(e)}), 500

    try:
        # Fetch all possible emotion options
        emotions = Emo.query.all()
        emotion_list = [emotion.to_dict() for emotion in emotions]

        # Fetch all possible weather options
        weather_options = Weather.query.all()
        weather_list = [weather.to_dict() for weather in weather_options]

        # Create the response DTO
        convResponse = ConversationResponseDTO(
            conversation_id=new_conv.conversation_id,
            user_id=new_conv.user_id,
            start_time=new_conv.start_time,
            emotions=emotion_list,
            weather_options=weather_list
        )

        return jsonify(convResponse.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




# 메시지 생성
from .models import Messages  # SQLAlchemy 모델


@app.route('/message/<int:userId>', methods=['POST'])
def add_message():
    data = request.get_json()

    try:
        # DTO로 요청 데이터 검증
        message_dto = MessageRequestDTO(
            conversation_id=data['conversationId'],
            user_id=data['userId'],
            timelog=datetime.strptime(data['timelog'], '%Y-%m-%d %H:%M:%S'),
            text=data['text'],
            image=data['image']
        )

        # 1. SQLAlchemy Message 모델을 사용해 데이터베이스에 추가
        message = Messages(
            conversation_id=message_dto.conversation_id,
            user_id=message_dto.user_id,
            timelog=message_dto.timelog,
            text=message_dto.text,
            image=message_dto.image
        )
        db.session.add(message)
        db.session.commit()

        # 2. AI 모듈에 요청을 보내고 응답 받기
        aimsg = get_message(message.conversation_id, message.text)

        if not aimsg:
            raise Exception("Failed to get response from AI")

        # 3. t_conversations 릴레이션의 context 필드 업데이트
        conversation = Conversations.query.filter_by(conversation_id=message.conversation_id).first()

        if conversation:
            conversation.context = aimsg.context
            db.session.commit()
        else:
            raise Exception("Conversation not found")

        # 3. 응답에 AI 응답 포함
        response = MessageResponseDTO(
            user_id=message.user_id,
            timelog=message.timelog,
            botresponse=aimsg.text  # AI 응답
        )

        return jsonify(response.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 생성된 일기 조회
@app.route('/diary', methods=['POST'])
def get_diary():
    try:
        # 요청 데이터를 가져와 DTO로 감싸 검증
        data = request.get_json()
        diary_request = GetDiaryRequest(
            user_id=data['user_id'],
            date=data['date']
        )

        # 다이어리 조회
        diary = Diary.query.filter_by(user_id=diary_request.user_id, date=diary_request.date).first()

        if not diary:
            return jsonify({"error": "Diary not found"}), 404

        # 응답 DTO를 생성
        diary_response = GetDiaryResponse(
            user_id=diary.user_id,
            diary_id=diary.diary_id,
            date=diary.date,
            context=diary.context
        )

        return jsonify(diary_response.to_dict()), 200

    except KeyError as e:
        # 필수 필드가 없을 때 발생하는 KeyError 처리
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

    except Exception as e:
        # 그 외의 예외 처리
        return jsonify({"error": "An error occurred: " + str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
