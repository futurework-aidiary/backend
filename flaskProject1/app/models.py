from typing import List, Optional

from sqlalchemy import Column, Date, DateTime, ForeignKeyConstraint, Index, Integer, String, Table, text, nulls_last, \
    ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, MappedClassProtocol
from datetime import datetime

from . import db



class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = (
        Index('User_pk', 'username', unique=True),
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(10))
    username: Mapped[str] = mapped_column(String(10))
    password: Mapped[str] = mapped_column(String(255))
    phone_num: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(String(40))
    birth: Mapped[datetime.date] = mapped_column(Date)

    condition: Mapped[List['Condition']] = relationship('Condition', back_populates='user')
    diary: Mapped[List['Diary']] = relationship('Diary', back_populates='user')
    messages: Mapped[List['Messages']] = relationship('Messages', back_populates='user')


class Abusing(db.Model):
    __tablename__ = 'abusing'
    __table_args__ = {}

    abuse_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(10))

    condition: Mapped[List['Condition']] = relationship('Condition', back_populates='abusing')


class Background(db.Model):
    __tablename__ = 'background'
    __table_args__ = {}

    backstyle: Mapped[str] = mapped_column(String(10), primary_key=True)


class Bubble(db.Model):
    __tablename__ = 'bubble'
    __table_args__ = {}

    bubstyle: Mapped[str] = mapped_column(String(10), primary_key=True)


class Character(db.Model):
    __tablename__ = 'character'
    __table_args__ = {}

    charstyle: Mapped[str] = mapped_column(String(10), primary_key=True)


class Emo(db.Model):
    __tablename__ = 'emo'
    __table_args__ = {}

    emo: Mapped[str] = mapped_column(String(10), primary_key=True)

    diary: Mapped[List['Diary']] = relationship('Diary', back_populates='emo_')


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    __table_args__ = {}

    rst_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rst_name: Mapped[str] = mapped_column(String(10))
    rst_address: Mapped[str] = mapped_column(String(40))
    rst_call: Mapped[int] = mapped_column(Integer)


class Survey(db.Model):
    __tablename__ = 'survey'
    __table_args__ = {}

    survey_name: Mapped[str] = mapped_column(String(10), primary_key=True)

    survey_question: Mapped[List['SurveyQuestion']] = relationship('SurveyQuestion', back_populates='survey')


class Weather(db.Model):
    __tablename__ = 'weather'
    __table_args__ = {}

    weather: Mapped[str] = mapped_column(String(10), primary_key=True)

    diary: Mapped[List['Diary']] = relationship('Diary', back_populates='weather_')


class Condition(db.Model):
    __tablename__ = 'condition'
    __table_args__ = (
        ForeignKeyConstraint(['abused'], ['abusing.abuse_id'], name='condition_abusing_abuse_id_fk'),
        ForeignKeyConstraint(['user_id'], ['User.user_id'], name='condition_User_user_id_fk'),
        Index('condition_User_user_id_fk', 'user_id'),
        Index('condition_abusing_abuse_id_fk', 'abused'),
    )

    con_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    con_date: Mapped[datetime.date] = mapped_column(Date)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    abused: Mapped[Optional[int]] = mapped_column(Integer)
    mental: Mapped[Optional[int]] = mapped_column(Integer)
    nutrition: Mapped[Optional[int]] = mapped_column(Integer)

    abusing: Mapped['Abusing'] = relationship('Abusing', back_populates='condition')
    user: Mapped['User'] = relationship('User', back_populates='condition')

class Custom(db.Model):
    __tablename__ = 'custom'
    __table_args__ = (
        ForeignKeyConstraint(['backstyle'], ['background.backstyle'], name='custom_background_backstyle_fk'),
        ForeignKeyConstraint(['bubstyle'], ['bubble.bubstyle'], name='custom_bubble_bubstyle_fk'),
        ForeignKeyConstraint(['charstyle'], ['character.charstyle'], name='custom_character_charstyle_fk'),
        ForeignKeyConstraint(['user_id'], ['User.user_id'], name='custom_User_user_id_fk'),
        Index('custom_User_user_id_fk', 'user_id'),
        Index('custom_background_backstyle_fk', 'backstyle'),
        Index('custom_bubble_bubstyle_fk', 'bubstyle'),
        Index('custom_character_charstyle_fk', 'charstyle')
    )

    conversation_id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True) # 추가: Integer 타입으로 정의
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    backstyle: Mapped[str] = mapped_column(String(10), nullable=False)  # 수정: backstyle로 변경
    charstyle: Mapped[str] = mapped_column(String(10), nullable=False)
    bubstyle: Mapped[str] = mapped_column(String(10), nullable=False)



class Conversations(db.Model):
    __tablename__ = 'conversations'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['User.user_id'], name='conversations_User_user_id_fk'),
        Index('conversations_User_user_id_fk', 'user_id'),
        Index('conversations_id', 'conversation_id', unique=True)
    )
    conversation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[Date] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))  # 수정된 부분
    end_time: Mapped[datetime] = mapped_column(DateTime)
    context: Mapped[str] = mapped_column(String(100))
    diary: Mapped['Diary'] = relationship('Diary', back_populates='conversations')


class Diary(db.Model):
    __tablename__ = 'diary'
    __table_args__ = (
        ForeignKeyConstraint(['emo'], ['emo.emo'], name='diary_emo_emo_fk'),
        ForeignKeyConstraint(['user_id'], ['User.user_id'], name='diary_User_user_id_fk'),
        ForeignKeyConstraint(['weather'], ['weather.weather'], name='diary_weather_weather_fk'),
        Index('diary_User_user_id_fk', 'user_id'),
        Index('diary_emo_emo_fk', 'emo'),
        Index('diary_weather_weather_fk', 'weather')
    )

    diary_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date)
    weather: Mapped[str] = mapped_column(String(10))
    emo: Mapped[str] = mapped_column(String(10))
    bookmark: Mapped[int] = mapped_column(TINYINT(1))
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    context: Mapped[Optional[str]] = mapped_column(String(300))
    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey('conversations.conversation_id'))

    conversations: Mapped['Conversations'] = relationship('Conversations', back_populates='diary')
    emo_: Mapped['Emo'] = relationship('Emo', back_populates='diary')
    user: Mapped['User'] = relationship('User', back_populates='diary')
    weather_: Mapped['Weather'] = relationship('Weather', back_populates='diary')


class SurveyQuestion(db.Model):
    __tablename__ = 'survey_question'
    __table_args__ = (
        ForeignKeyConstraint(['survey_name'], ['survey.survey_name'], name='survey_question_survey_survey_name_fk'),
        Index('survey_question_survey_survey_name_fk', 'survey_name'),
    )

    question_num: Mapped[int] = mapped_column(Integer, primary_key=True)
    survey_name: Mapped[str] = mapped_column(String(10))
    question: Mapped[str] = mapped_column(String(30))

    survey: Mapped['Survey'] = relationship('Survey', back_populates='survey_question')


class Messages(db.Model):
    __tablename__ = 'messages'
    __table_args__ = (
        ForeignKeyConstraint(['conversation_id'], ['conversations.conversation_id'], name='messages_conversations_conversation_id_fk'),
        ForeignKeyConstraint(['user_id'], ['User.user_id'], name='user_id'),
        Index('messages_conversations_conversation_id_fk', 'conversation_id'),
        Index('user_id', 'user_id'),
        Index('messages_id', 'message_id', unique=True)

    )

    message_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timelog: Mapped[datetime] = mapped_column(DateTime)
    conversation_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    text: Mapped[Optional[str]] = mapped_column('text', String(100))
    image: Mapped[Optional[str]] = mapped_column(String(255))
    botresponse: Mapped[Optional[str]] = mapped_column(String(255))
    user: Mapped['User'] = relationship('User', back_populates='messages')



class Response(db.Model):
    __tablename__ = 'response'
    __table_args__ = (
        ForeignKeyConstraint(['question_num'], ['survey_question.question_num'],
                             name='response_survey_question_question_num_fk'),
        ForeignKeyConstraint(['survey_name'], ['survey_question.survey_name'],
                             name='response_survey_question_survey_name_fk'),
        Index('response_survey_question_question_num_fk', 'question_num'),
        Index('response_survey_question_survey_name_fk', 'survey_name')
    )

    question_num: Mapped[int] = mapped_column(Integer, nullable=False)  # question_num 추가
    survey_name: Mapped[str] = mapped_column(String(10), nullable=False, primary_key=True)
    response: Mapped[int] = mapped_column(Integer, nullable=False)

