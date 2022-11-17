import datetime
import hashlib

import certifi
import jwt
from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import uuid

app = Flask(__name__)
# application = Flask(__name__, static_folder='static', template_folder='templates')


ca = certifi.where()
client = MongoClient(
    "mongodb+srv://test:sparta@cluster0.cctcpnr.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.mansclub

# 크롤링
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://sports.daum.net/',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

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


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"])

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return render_template('index.html')


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/register')
def register():
    return render_template('member.html')

@app.route('/leave')
def leave():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('leavePage.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/mypage')
def mypage():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('mypage.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))        

#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/join', methods=['POST'])
def api_register():
    id_receive = request.form['userid_give']
    pw_receive = request.form['userpw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    id_check = db.user.find_one({'id': id_receive}, {'_id': 0})
    if id_check == None:
        db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive, 'point': 0, 'tier': 1})
        return jsonify({'result': 'success'})
    else :
        return jsonify({'result': 'fail'})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# [탈퇴 API]
@app.route('/api/leave', methods=['POST'])
def api_leave():
        token_receive = request.form['token_give']
        pw_receive = request.form['pwconfirm_give']
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        

        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        if pw_hash == userinfo['pw']:
            db.user.delete_one({'id':payload['id']})
            return jsonify({'result': 'success'})
        else :
            return jsonify({'result': 'fail'})

# [비번변경 API]
@app.route('/api/pwchange', methods=['POST'])
def api_pwchange():
        token_receive = request.form['token_give']
        pw_receive = request.form['pw_give']
        new_pw_receive = request.form['new_pw_give']
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        #받아온 원래 패스워드
        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest() 
        #새로운 패스워드
        new_pw_hash = hashlib.sha256(new_pw_receive.encode('utf-8')).hexdigest()
        
        #db에 저장된 원래 패스워드 
        pw_original = db.user.find_one({'id': payload['id']}, {'_id': 0})['pw']

        if pw_hash == pw_original:
            db.user.update_one({'id':payload['id']},{'$set':{'pw':new_pw_hash}})
            return jsonify({'result':'success' })
        else :
            return jsonify({'result': 'fail'})

# [닉네임변경 API]
@app.route('/api/nicknamechange', methods=['POST'])
def api_nickchange():
        token_receive = request.form['token_give']
        nick_receive = request.form['nickname_give']
       
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        nickname_check = db.user.find_one({'nick': nick_receive}, {'_id': 0})
  
        if nickname_check == None:
            db.user.update_one({'id':payload['id']},{'$set':{'nick':nick_receive}})
            return jsonify({'result':'success' })
        else :
            return jsonify({'result': 'fail'})  


#[닉네임 체크용]
@app.route('/api/nickcheck', methods=['POST'])
def api_nickcheck():
        token_receive = request.form['token_give']
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        nickname_check = db.user.find_one({'id': payload['id']}, {'_id': 0})['nick']
        return jsonify({'nick': nickname_check})  


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})



# 챌린지 포스트
@app.route('/templates/challenge', methods=['POST'])
def challenge_post():
    num_receive = uuid.uuid4().hex ##게시글 번호
    token_receive = request.form['token_give'] ##작성자 계정
    url_receive = request.form['url_give'] ## 게시글 내용
    score_receive = request.form['score_give'] ## 챌린지 점수
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    count = 0

    doc = {
        'num':num_receive,
        'writer':payload['id'],
        'url':url_receive,
        'score':score_receive,
        'confirmer':[]
    }
    db.challenge.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})

# 챌린지 보여주기
@app.route('/templates/challenge',methods=["GET"])
def challenge_get():
    challenge_list = list(db.challenge.find({}, {'_id': False}))
    # return dumps({'trading_posts': trading_list})
    return jsonify({'challenges': challenge_list})

# 챌린지 인증
@app.route('/api/challenge',methods=["POST"])
def chall_confirm ():
    token_receive = request.form['token_give'] ##인증자 계정
    num_receive = request.form['num_give'] ##게시글 번호
    ## 인증자 점수 찾기
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.user.find_one({"id": payload['id']})
    user_point = user_info['point']
    ## 게시글 정보 찾기
    post = db.challenge.find_one({"num": num_receive}) ## HEX값으로 찾은 게시글 object
    count = len(post['confirmer']) ## 게시글의 인증 횟수
    # 게시자인지 확인
    if user_info['id'] == post['writer']:
        return jsonify({'writer': True})
    # 이미 인증했는지, 점수가 부족한지 확인
    elif user_info['id'] in post['confirmer'] or user_point < 100:
        return jsonify({'confirmed': True})
    # 게시글 인증이 이미 3회 완료됐는지 확인
    elif count >= 3:
        return jsonify({'count_full': True})
    # 인증 횟수 추가하기
    else:
        db.challenge.update_one({'num':num_receive},{'$push': {'confirmer':payload['id']}})
        # 인증 3회 체웠을 때
        if len(db.challenge.find_one({"num": num_receive})['confirmer']) < 3:
            return jsonify({'complete': True})
        else:
            ## 챌린지 인증 완료되면 게시자 점수 찾고 덧셈하기
            writer = post['writer'] ## 게시자의 id
            point = int(db.user.find_one({"id": writer})['point']) ## 게시자의 현재 점수
            score = int(post['score']) ## 게시글의 점수
            db.user.update_one({'id':writer},{'$set':{'point':point+score}})
            return jsonify({'complete': True})

# 뉴스 크롤링
@app.route('/news', methods=['GET'])
def news_get():
    news = soup.select('#cSub > div.feature_top > div.top_rank > ol:nth-child(3) > li')
    news_list = []
    for new in news:
        rank = new.select_one('em').text
        title = new.select_one('strong > a').text
        link = new.select_one('strong > a').attrs['href']

        if len(title) > 25:
            title = title[0:20] + '...'

        doc = {
            'rank':rank, 
            'title':title, 
            'link':link
            }
        news_list.append(doc)
    return jsonify({'news':news_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
#