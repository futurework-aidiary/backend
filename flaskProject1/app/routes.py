from flask import jsonify, request

from app.routesAI import get_message
from .dto import *
from .models import *
from app import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime

from flask import Blueprint
# 메시지 생성
from .models import Messages  # SQLAlchemy 모델

import logging

# 로깅 설정
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 블루프린트 정의
main_routes = Blueprint('main', __name__)


@main_routes.route('/')
def hellor():
    return "Hello, routes!"

# 회원가입
@main_routes.route('/user/add', methods=['POST'])
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
@main_routes.route('/login', methods=['POST'])
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
@main_routes.route('/user/<int:userId>/get', methods=['GET'])

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
@main_routes.route('/user/<int:userId>/update', methods=['PUT'])
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
@main_routes.route('/user/<int:userId>/delete', methods=['DELETE'])
def delete_user(userId):

    user = User.query.get(userId)

    try:
        db.session.delete(user)
        db.session.commit()

    except Exception as e:
        return jsonify({"error": str(e)})

    return jsonify(DeleteUserResponseDTO.to_dict("User deleted successfully")), 200

#대화세션 생성
@main_routes.route('/conversations', methods=['POST'])
def conversation_start():
    data = request.get_json()

    try:
        get_con = ConversationRequestDTO(
            user_id=data.user_id,
            emo=data.emo,
            weather=data.weather
        )

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

    user = User.query.filter_by(user_id=get_con.user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404



    try:

        new_conv = Conversations(
            user_id=user.user_id,
            start_time=datetime.now(),  # 현재 시간 대입
            end_time=None,
            context=""
        )
        # 4. 데이터베이스에 저장
        db.session.add(new_conv)
        db.session.commit()

        new_diary = Diary(
            date = datetime.today(),
            weather = get_con.weather,
            emo = get_con.emo,
            bookmark = None,
            user_id = get_con.user_id,
            context = "",
            conversation_id = new_conv.conversation_id
        )
        db.session.add(new_diary)
        db.session.commit()

        # Create the response DTO
        convResponse = ConversationResponseDTO(
            conversation_id=new_conv.conversation_id,
            start_time=new_conv.start_time
        )

        return jsonify(convResponse.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@main_routes.route('/message', methods=['POST'])
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

        # 데이터베이스에 메시지 추가
        message = Messages(
            conversation_id=message_dto.conversation_id,
            user_id=message_dto.user_id,
            timelog=message_dto.timelog,
            text=message_dto.text,
            image=message_dto.image
        )
        db.session.add(message)
        db.session.commit()

        # AI 모듈에 요청
        botresponse = get_message(message.text)

        if not botresponse:
            logging.error("Failed to get response from AI")
            raise Exception("Failed to get response from AI")

        #메시지 db에 업데이트
        message.botresponse = botresponse['botresponse']
        db.session.commit()

        # 응답 반환
        response = MessageResponseDTO(
            user_id=message.user_id,
            timelog=datetime.now().strftime('%Y-%m-%d'),
            botresponse=botresponse['botresponse']
        )
        return jsonify(response.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#프론트서 종료 요청 시, exit문자 ai에 전달하고, 응답(일기)를 diary에 마저 저장

@main_routes.route('/conversations/end', methods=['POST'])
def end_conversation():
    try:
        data = request.get_json()
        get_end = ConversationEndRequest(
            conversation_id=data['conversationId'],
            end_time=data['endTime']
        )

        conv = Conversations.query.filter_by(conversation_id=get_end.conversation_id)
        conv.end_time = get_end
        db.session.commit()

        # AI 모듈에 요청
        endtext = "exit"
        diarytext= get_message(endtext)

        #db에 일기내용 추가

        writtendiary = Diary.query.filter_by(conversation_id=get_end.conversation_id).first()

        writtendiary.context = diarytext

        endresponse = ConversationEndResponse(
            diary = diarytext
        )

        return jsonify(endresponse.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# 생성된 일기 조회
@main_routes.route('/diary', methods=['POST'])
def get_diary():
    try:
        logging.info("Diary 조회 요청 시작")

        # 요청 데이터를 가져와 DTO로 감싸 검증
        data = request.get_json()
        logging.debug(f"받은 요청 데이터: {data}")

        diary_request = GetDiaryRequestDTO(
            user_id=data['userId'],
            conversation_id=data['conversationId']
        )
        logging.debug(f"Diary 요청 DTO: {diary_request}")

        writtendiary = Diary.query.filter_by(conversation_id=diary_request.conversation_id).first()
        logging.debug(f"기존 일기 조회 결과: {writtendiary}")

        # 적힌 일기를 찾았다면, 이를 반환.
        if writtendiary:
            logging.info("일기 반환")
            diary_response = GetDiaryResponseDTO(
                user_id=writtendiary.user_id,
                diary_id=writtendiary.diary_id,
                emo=writtendiary.emo,
                weather=writtendiary.weather,
                date=writtendiary.date,
                context=writtendiary.context
            )

        return jsonify(writtendiary.to_dict()), 200

    except KeyError as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    main_routes.run(debug=True)
