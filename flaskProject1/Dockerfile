# 베이스 이미지
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
# . . 뜻: Dockerfile이 있는 디렉토리의 모든 파일과 폴더를 컨테이너의 현재 작업 디렉토리에 복사. 이로 인해 애플리케이션의 코드, 설정 파일 등 필요한 모든 파일이 컨테이너에 포함
COPY . .

EXPOSE 5000

# wsgi로 실행. 이후 app 실행 (cmd 명령을 써놓은거)
CMD ["waitress-serve", "--port=5000", "run:app"]
