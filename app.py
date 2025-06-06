import datetime
from flask import Flask, send_from_directory

#flask 서버 임포
from flask import Flask, send_file, render_template, redirect, url_for, session, request, jsonify
from flask_cors import CORS  # CORS 추가

#ORM을 사용하게 되면 따로 SQL문을 작성할 필요없이 객체를 통해 간접적으로 데이터베이스를 조작
#from flask_sqlalchemy import SQLAlchemy

#시간관련 임포
from datetime import timedelta

#구글 연동 관련
import secrets
from authlib.integrations.flask_client import OAuth

#오픈ai 정보 임포트
import openai

#mysql연동
#import pymysql
from flask_bcrypt import Bcrypt
from flask_session import Session


#보안 관련
from werkzeug.utils import secure_filename
import uuid

import requests

#postreg .env에 있는 url 연동시 필요
from flask_sqlalchemy import SQLAlchemy

#api 키 불러오기
from dotenv import load_dotenv
#파일 업로드 다운로드 관련
import os



#import os
import asyncio
from sqlalchemy import text
#from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy.ext.asyncio import create_async_engine

# .env 파일 활성화
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("Neon_DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Contents 테이블 생성
class Members(db.Model):
    __tablename__ = 'Members'

    SERIAL_id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
#Contents 테이블 생성
class Contents(db.Model):
    __tablename__ = 'Contents'

    Content_SERIAL_id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    holseHead = db.Column(db.String(100), nullable=False)
    viewCount = db.Column(db.Integer, nullable=False)
    greatCount = db.Column(db.Integer, nullable=False)


    def to_dict(self):
        return {
            "Content_SERIAL_id": self.Content_SERIAL_id,
            "Title": self.Title,
            "content": self.content,
            "Email": self.Email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "holseHead": self.holseHead,
            "viewCount": self.viewCount,
            "greatCount": self.greatCount,
        }

#댓글 테이블 생성
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('Contents.Content_SERIAL_id', ondelete='CASCADE'), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # 게시글과의 관계 (선택적, 역참조용)
    post = db.relationship('Contents', backref=db.backref('comments', cascade='all, delete-orphan', lazy=True))

with app.app_context():
    db.create_all()

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

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    if not data:
        print("잘못된 요청")
        return jsonify({"response": "잘못된 요청"}), 400  # 반드시 return 필요!
    
    if request.method == "POST":
        
        user_Name = data.get('inputName')
        user_Pw = data.get('inputPw')
        user_Email = data.get('inputEmail')
        
        # #비밀번호를 DB에 저장할때 변환해서 저장
        hashed_password = bcrypt.generate_password_hash(user_Pw).decode("utf-8")
        
        try :

            new_user = Members(Email = user_Email, name = user_Name, Password = hashed_password)
            print(new_user)
            db.session.add(new_user)
            db.session.commit()
            print("***********************INSERT success**********************")
            #회원가입후 세션에 넣음
            session["user"] = user_Email
            return jsonify({"status": "success", "message": "register success", "redirect": "/"}), 200
        
        except Exception as e:
            print("commit 실패")
            return jsonify({"status": "fail","message": "register fail2, method not post"})
        
        
    else:
        print('get으로 받음')
        return jsonify({"status": "fail","message": "register fail2, method not post"})

# 📌 로그인
@app.route("/login", methods=["POST"])
def login():
    print('로그인')

    data = request.json

    if not data:
        print("잘못된 요청")
        return jsonify({"response": "잘못된 요청"}), 400  # 반드시 return 필요!
    
    if request.method == "POST":

        user_Email = data.get('inputEmail')
        
        user_Pw = data.get('inputPw')
        
        try:
            user = Members.query.filter_by(Email = user_Email).first()            
 
             #비밀번호 비교
            if user and bcrypt.check_password_hash(user.Password, user_Pw):
                session["user"] = user_Email
                print('로그인 성공')
                return jsonify({"status": "success", "message": "login success", "redirect": "/"}), 200
        
            else:
                print('회원가입 안함 실패1')
                return jsonify({"status": "fail", "message": "Invalid email or password"}),401
            
        except Exception as e:
            print(f"❌ 서버 오류 발생: {e}")
            return jsonify({"status": "error", "message": "Internal Server Error"}), 500
    
    else:
        print('로그인 실패2')
        return jsonify({"status": "fail", "message": "fail , server check please"}),402

# 로그아웃
@app.route("/logout", methods=["POST"])
def logout():
    if "user" not in session:
        print('로그인 안되어있음')
        return jsonify({"status": "fail", "message": "not login"}), 200        
    
    session.pop("user", None)
    print('로그아웃')
    return jsonify({"status": "success", "message": "success logout", "redirect": "/"}), 200

#로그인 상태 유무 확인
@app.route("/dashboard")
def dashboard():
    
    if "user" in session:
        print("dashboard : success")
        return jsonify({"status": "success"}), 200
    
    print("dashboard : not Login")
    return jsonify({"status": "fail", "message": "Unauthorized access"})

#게시글 선택시 호출
@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Contents.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()

    # 이전글, 다음글 찾기
    prev_post = Contents.query.filter(Contents.Content_SERIAL_id < post_id).order_by(Contents.Content_SERIAL_id.desc()).first()
    next_post = Contents.query.filter(Contents.Content_SERIAL_id > post_id).order_by(Contents.Content_SERIAL_id.asc()).first()

    return render_template('post_detail.html', post=post, comments=comments, prev_post=prev_post, next_post=next_post)


#DB에 등록된 게시글의 제목과 글쓴이 좋아요 등등 다수 데이터 불러오기
@app.route('/getNoticeBoardData', methods=['GET'])
def getNoticeBoardData():
    try:
        page = 1
        per_page = 20

        getContents = Contents.query.paginate(page=page, per_page=per_page, error_out=False).items
        
        contents_list = [content.to_dict() for content in getContents]

        return jsonify({"status": "success", "contents": contents_list})
    
    except Exception as e:
        print("게시글 가져오기 실패:", e)
        return jsonify({"status": "fail", "message": str(e)})
    

@app.route('/comment', methods=['POST'])
def add_comment():
    post_id = request.form['post_id']
    author = request.form['author']
    content = request.form['content']

    new_comment = Comment(post_id=post_id, author=author, content=content)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for('view_post', post_id=post_id))

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


@app.route('/')
def home():
    print("홈으로")
    return render_template('index.html')  # Flask가 HTML을 렌더링

@app.route('/serviceLogin')
def serviceLogin():
    print("serviceLogin 호출")
    return render_template('profile.html')  # Flask가 HTML을 렌더링


@app.route('/noticeBoard')
def noticeBoard():
    print("noticeBoard 호출")
    return render_template('noticeBoard.html')  # Flask가 HTML을 렌더링

#vide 태그에서 영상 불러올때 사용
@app.route('/videos/<string:videoName>')
def videos(videoName):
    response = send_from_directory('static/videos', videoName)
    response.headers['Cache-Control'] = 'public, max-age=86400'  # 1일 동안 캐시 유지
    return response


import requests
@app.route('/test-connection')
def test_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return f"✅ 외부 연결 성공! 응답 코드: {response.status_code}"
    except Exception as e:
        return f"❌ 외부 연결 실패: {str(e)}"
    

# if __name__ == '__main__':
#     app.run('0.0.0.0',debug=False, port=5000)

if __name__ == '__main__':
    app.run(debug=True)