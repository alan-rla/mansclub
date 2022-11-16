import hashlib
import datetime
import jwt
import certifi
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)


ca = certifi.where()

client = MongoClient(
    "mongodb+srv://test:sparta@cluster0.cctcpnr.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.mansclub

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;


#################################
##  HTML을 주는 부분             ##
#################################
# @app.route('/')
# def home():


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/member')
def member():
    return render_template('member.html')


@app.route("/member/join", methods=["POST"])
def join_member():
    userid_receive = request.form['userid_give']
    userpw_receive = request.form['userpw_give']
    usernickname_receive = request.form['nickname_give']
    # userinfo = list(db.user.find({'id':userid_receive},{'_id':False}))

    doc = {
        'user_id': userid_receive,
        'pw': userpw_receive,
        'nickname': usernickname_receive,
        'point': 0,
        'tier': 1
    }
    db.user.insert_one(doc)
    return jsonify('msg', "등록 완료")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
