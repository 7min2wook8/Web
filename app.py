from flask import Flask, send_from_directory

#flask 서버 임포
from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from flask_cors import CORS  # CORS 추가
from flask_sqlalchemy import SQLAlchemy
#시간관련 임포
from datetime import timedelta

#구글 연동 관련
import secrets
from authlib.integrations.flask_client import OAuth

#오픈ai 정보 임포트
import openai

import psycopg2

#mysql연동
#import pymysql
from flask_bcrypt import Bcrypt
from flask_session import Session


#보안 관련
from werkzeug.utils import secure_filename
import uuid

import requests

#api 키 불러오기
from dotenv import load_dotenv
#파일 업로드 다운로드 관련
import os

# .env 파일 활성화
load_dotenv()

conn  = None

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://mydatabase_p7ae_user:fvCc4VdMYTjeXnO7jPBpI5WnnkxryDRs@dpg-cv7pgv5ds78s73cotta0-a/mydatabase_p7ae")

# SQLAlchemy 설정
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# 예제 테이블 모델
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)   # 기본키
    name = db.Column(db.String(50), nullable=False)  # 이름 (NOT NULL)

# 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()




@app.route('/add_user/<name>')
def add_user(name):
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    return f"User {name} added!"

@app.route('/users')
def get_users():
    users = User.query.all()
    return {"users": [user.name for user in users]}


@app.route("/user/<int:user_id>")
def get_user(user_id):
    user = User.query.get(user_id)  # 특정 ID 조회 (SELECT * FROM users WHERE id=user_id)
    if user:
        return {"id": user.id, "name": user.name}
    return "User not found", 404


@app.route("/update_user/<int:user_id>/<new_name>")
def update_user(user_id, new_name):
    user = User.query.get(user_id)  # 특정 ID 조회
    if user:
        user.name = new_name  # 데이터 변경
        db.session.commit()  # 변경 사항 저장 (UPDATE 실행)
        return f"User {user_id} updated to {new_name}!"
    return "User not found", 404


@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)  # 특정 ID 조회
    if user:
        db.session.delete(user)  # 삭제
        db.session.commit()  # 변경 사항 저장 (DELETE 실행)
        return f"User {user_id} deleted!"
    return "User not found", 404



@app.route("/drop_table")
def drop_table():
    db.drop_all()  # 모든 테이블 삭제 (DROP TABLE 실행)
    return "All tables dropped!"



@app.route("/search/<name>")
def search_user(name):
    users = User.query.filter_by(name=name).all()  # 특정 이름을 가진 사용자 조회
    return {"users": [user.id for user in users]}


@app.route("/search_advanced/<name>/<int:user_id>")
def search_advanced(name, user_id):
    users = User.query.filter((User.name == name) | (User.id == user_id)).all()
    return {"users": [user.id for user in users]}




app.secret_key = "qweasd456"  # 세션 암호화를 위한 SECRET_KEY 설정
bcrypt = Bcrypt(app)

# 모든 도메인에 대해 CORS 허용
# CORS 설정 (쿠키 사용 시 필요)
CORS(app, supports_credentials=True)  

# 업로드 폴더 경로 설정
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 폴더가 없으면 생성
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 원래 파일 이름과 변환된 파일 이름 저장
filename_mapping = {}


# 세션 설정
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)  # 1시간 유지


Session(app)


# try:
#     db = pymysql.connect(
#         host='localhost',
#         user='root',
#         passwd='qweasd456',
#         database='myDB',
#         charset='utf8'
#     )
#     print("연결완료")
# except Exception as e:
#     print(e)

# 연결이 성공했으면 커서 생성
#cursor = db.cursor()

# @app.route("/register", methods=["POST"])
# def register():
#     data = request.json

#     if not data:
#         print("잘못된 요청")
#         return jsonify({"response": "잘못된 요청"}), 400  # 반드시 return 필요!
    
#     if request.method == "POST":
        
#         user_Name = data.get('inputName')
#         user_Pw = data.get('inputPw')
#         user_Email = data.get('inputEmail')
        
#         # #비밀번호를 DB에 저장할때 변환해서 저장
#         hashed_password = bcrypt.generate_password_hash(user_Pw).decode("utf-8")
        
#         try:
            
#             cursor.execute("insert into mydb.memberinfo (id, pw, name) values (%s, %s, %s)", (user_Email, hashed_password, user_Name))
#             db.commit()
#             print('회원가입 실패1')
#             return jsonify({"status": "success", "message": "register succes", "redirect": "/"}), 200

        
#         except pymysql.err.IntegrityError:

#             print("이미 존재하는 아이디이거나 쿼리 오류입니다.")
#             return jsonify({"status": "fail","message": "register fail1"})
        
#     else:
#         print('회원가입 실패2')
#         return jsonify({"status": "fail","message": "register fail2, method not post"})


# # 📌 로그인
# @app.route("/login", methods=["POST"])
# def login():
#     print('로그인')

#     data = request.json

#     if not data:
#         print("잘못된 요청")
#         return jsonify({"response": "잘못된 요청"}), 400  # 반드시 return 필요!
    
#     print("받은 데이터:", data)  # JSON 데이터 확인

#     if request.method == "POST":

#         user_Email = data.get('inputEmail')
        
#         user_Pw = data.get('inputPw')

        
#         # #임시 입력
#         # if user_Email == '':
#         #     user_Email = "7min2wook8@naver.com"

#         # if user_Pw == '':
#         #     user_Pw = "qweasd456"
#         # session["user"] = user_Email
#         # return jsonify({"status": "success", "message": "login succes", "redirect": "/"}), 200
#         try:
#             cursor.execute("select ID,PW,name from mydb.memberinfo where ID = %s", (user_Email,))
#             user = cursor.fetchone()

#             if user and bcrypt.check_password_hash(user[1], user_Pw):
#                 session["user"] = user_Email
#                 print('로그인 성공')
#                 return jsonify({"status": "success", "message": "login succes", "redirect": "/"}), 200
        
#             else:
#                 print('로그인 실패1')
#                 return jsonify({"status": "fail", "message": "Invalid email or password"}),401
            
#         except Exception as e:
#             print(f"❌ 서버 오류 발생: {e}")
#             return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    
#     else:
#         print('로그인 실패2')
#         return jsonify({"status": "fail", "message": "fail , server check please"}),402




# # 로그아웃
# @app.route("/logout")
# def logout():
    
#     if "user" not in session:
#         print('로그인 안되어있음')
#         return redirect("/")  # 로그인 안 되어 있으면 로그인 페이지로 이동
    
#     session.pop("user", None)
#     return redirect("/")


# @app.route('/logout')
# def logout():
#     session.pop("user", None)  # 세션 삭제
#     return render_template('index.html')  # Flask가 HTML을 렌더링
#     return jsonify({"status": "success", "message": "Logged out"}), 200

#로그인 상태 유무 확인
@app.route("/dashboard")
def dashboard():
    print("/dashboard 실행")
    print(session)
    if "user" in session:
        return jsonify({"status": "success"}), 200
    
    return jsonify({"status": "fail", "message": "Unauthorized access"})
    return redirect("/")

# 추가 쿼리 insert into mydb.memberinfo (id,pw,name) values ("7min2wook8@naver.com","qweasd456" ,"parminwook")

##############################################################################################
openai_api_key= os.getenv("openai_api_key")
openai.api_key = openai_api_key


openWeathermap_api_key = os.getenv("openWeathermap_api_key")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_input1 = data.get('user_input', '').strip().lower()

    data2 = request.get_json()
    user_message = data2.get("user_input", "")
    
    if "날씨" in user_input1:
        # OpenWeatherMap API 사용 예제
        api_key = openWeathermap_api_key
        city = "Seoul"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=kr&units=metric"

        weather_data = requests.get(url).json()
        if weather_data.get('main'):
            temp = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            response = f"현재 {city}의 날씨는 {description}, 온도는 {temp}°C입니다."
        else:
            response = "날씨 정보를 가져오는 데 실패했습니다."
    
    elif "날씨" not in user_message :

       
        # OpenAI API 호출 (GPT-3 예시)
        try:
            print("response 호출")
            # OpenAI API 호출
            
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello!"}])
            
            reply = response.choices[0].message.content
            
            return jsonify({"reply": reply})

        except Exception as e:
            print("Error:", str(e))
            return jsonify({"error": str(e)}), 500
       
    
    else:
        response = "질문을 이해하지 못했습니다. 다시 시도해 주세요."


    return jsonify({'response': response})

##############################################################################################
#파일 업로드 받기
@app.route('/upload', methods=['POST'])
def upload_file():
    #print('업로드중....')
    if 'file' not in request.files:  # 'file' 키 확인
        return jsonify({'response': '파일이 첨부되지 않았습니다.'}), 400

    file = request.files['file']

    if file.filename == '':  # 파일 이름 확인
        return jsonify({'response': '파일 이름이 비어 있습니다.'}), 400


    original_filename = file.filename
    # 파일 이름 보안 처리 및 고유 이름 생성
    safe_filename  = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"


    # 파일 저장
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    file.save(save_path)

    filename_mapping[safe_filename] = original_filename
    print(f"Mapping: {filename_mapping}")
    # 파일 저장
    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
    
    return jsonify({'response': f"파일 '{file.filename}'이 성공적으로 업로드되었습니다."})

##############################################################################################
#파일 찾기
@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files})


##############################################################################################
#파일 다운로드
@app.route('/api/download', methods=['POST'])
def api_download_file():
    data = request.json
    filename = data.get('filename')

    # 파일 경로 확인
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.isfile(file_path):
        return jsonify({'error': '파일을 찾을 수 없습니다.'}), 404

    # 파일 데이터를 읽어와 응답
    #rb 자리는 파일의 바이너리 형식을 지정한다.
    with open(file_path, 'rb') as f:
        file_content = f.read()
    return jsonify({'filename': filename, 'content': file_content.decode('latin1')})  # 파일 내용을 전송


####################################################################################################################


# 환경 변수 사용
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# 보안을 위한 세션 키 설정
app.secret_key = os.urandom(24)

# OAuth 설정
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id= CLIENT_ID,
    client_secret = CLIENT_SECRET,
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    api_base_url="https://www.googleapis.com/oauth2/v2/",
    client_kwargs={"scope": "email profile"},
)

# 구글 로그인
@app.route("/login_Google")
def login_Google():

    session.permanent = True
    state = secrets.token_urlsafe(16)  # 임의의 state 값 생성
    session["oauth_state"] = state
    return google.authorize_redirect(url_for("auth_callback", _external=True), state=state)

# OAuth 인증 후 콜백 처리
@app.route("/auth/callback")
def auth_callback():

    if "oauth_state" not in session:
        return "세션에 state 값이 없습니다.", 400
    # 요청의 state와 세션의 state가 일치하는지 확인
    if request.args.get("state") != session["oauth_state"]:
        return "state 값이 일치하지 않습니다. CSRF 공격이 의심됩니다.", 400

    token = google.authorize_access_token()
    user_info = google.get("userinfo").json()
    session["user"] = user_info  # 세션에 사용자 정보 저장
    #return f"로그인 성공! 사용자: {user_info['email']}"
    return render_template("profile.html", user=user_info)  # HTML 페이지 반환
    # token = google.authorize_access_token()
    # user_info = google.get("userinfo").json()
    # session["user"] = user_info
    # #return jsonify(user_info)
    # return render_template("profile.html", user=user_info)  # HTML 페이지 반환

#####################################################################################################


@app.route('/welcom')
def welcom():    
    return render_template('welcom.html')  # Flask가 HTML을 렌더링


@app.route('/')
def home():
    print("홈으로")
    return render_template('index.html')  # Flask가 HTML을 렌더링

@app.route('/serviceLogin')
def serviceLogin():    
    return render_template('profile.html')  # Flask가 HTML을 렌더링

# if __name__ == '__main__':
#     app.run('0.0.0.0',debug=False, port=5000)

if __name__ == '__main__':
    app.run(debug=True)