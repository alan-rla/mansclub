from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
import certifi
from bson.json_util import dumps
from bs4 import BeautifulSoup
import requests

ca=certifi.where()

# 크롤링
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
client = MongoClient('mongodb+srv://test:sparta@cluster0.cctcpnr.mongodb.net/?retryWrites=true&w=majority')

# CSS 렌더링
app = Flask(__name__, template_folder='templates', static_folder='static')

# DB 주소
db = client.mansclub

# 크롤링
data = requests.get('https://sports.daum.net/',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

# 메인페이지
@app.route('/')
def home():
    return render_template('index.html')

# 챌린지 포스트
@app.route('/templates/challenge', methods=['POST'])
def challenge_post():
    # writer_receive = request.form['writer_give'] ##작성자 계정
    title_receive = request.form['title_give'] ##제목
    post_receive = request.form['post_give'] ## 게시글 내용
    time_receive = request.form['time_give'] ## 게시글 작성 시간
    num = len(list(db.free_board.find({},{'_id':False}))) ## 게시글 번호
    score = request.form['score_give'] ## 챌린지 점수

    doc = {
        # 'writer':writer_receive,
        'num':num,
        'title':title_receive,
        'post':post_receive,
        'time':time_receive,
        'score':score
    }

    db.challenge.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})

# 챌린지 보여주기
@app.route('/templates/challenge',methods=["GET"])
def challenge_get():
    challenge_list = list(db.challenge.find({}, {'_id': False}))
    # return dumps({'trading_posts': trading_list})
    return jsonify({'comments': challenge_list})


# 정보 공유 포스트
@app.route('/templates/info_share', methods=['POST'])
def info_share_post():
    # writer_receive = request.form['writer_give'] ##작성자 계정
    title_receive = request.form['title_give'] ##제목
    post_receive = request.form['post_give'] ## 게시글 내용
    time_receive = request.form['time_give'] ## 게시글 작성 시간
    num = len(list(db.free_board.find({},{'_id':False}))) ## 게시글 번호

    doc = {
        # 'writer':writer_receive,
        'num':num,
        'title':title_receive,
        'post':post_receive,
        'time':time_receive
    }

    db.info_share.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})

# 정보 공유 보여주기
@app.route('/templates/info_share',methods=["GET"])
def info_share_get():
    info_share_list = list(db.info_share.find({}, {'_id': False}))
    # return dumps({'trading_posts': trading_list})
    return jsonify({'comments': info_share_list})

# 자유게시판 포스트
@app.route('/templates/free_board', methods=['POST'])
def free_board_post():
    # writer_receive = request.form['writer_give'] ##작성자 계정
    title_receive = request.form['title_give'] ##제목
    post_receive = request.form['post_give'] ## 게시글 내용
    time_receive = request.form['time_give'] ## 게시글 작성 시간
    num = len(list(db.free_board.find({},{'_id':False}))) ## 게시글 번호

    doc = {
        # 'writer':writer_receive,
        'num':num,
        'title':title_receive,
        'post':post_receive,
        'time':time_receive
    }

    db.free_board.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})

# 자유게시판 보여주기
@app.route('/templates/free_board',methods=["GET"])
def free_board_get():
    free_board_list = list(db.free_board.find({}, {'_id': False}))
    # return dumps({'trading_posts': trading_list})
    return jsonify({'comments': free_board_list})

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