from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi

app = Flask(__name__)
ca = certifi.where()
client = MongoClient('mongodb+srv://test:123@cluster0.vpw4dwu.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)

# 메인 페이지 로드
@app.route('/')
def home():
    return render_template('index.html')

# 챌린지 게시판
@app.route('/challenge')
def challenge():
    return render_template('/challenge.html')

# 정보 공유 게시판
@app.route('/info_share')
def info_share():
    return render_template('/info_share.html')

# 자유게시판
@app.route('/free_board')
def free_board():
    return render_template('/free_board.html')

# 챌린지 게시판 포스트
@app.route('/templates/challenge', methods=['POST'])
def challenge_post():
    sample_receive = request.form['sample_give']
    return jsonify({'msg':'저장 완료!'})

# 챌린지 게시판 보여주기
@app.route('/templates/challenge',methods=["GET"])
def challenge_get():
    sample_list = list(db.article.find({}, {'_id': False}))
    return jsonify({'comments': '챌린지 게시판 보여주기'})

# 정보 공유 게시판 포스트
@app.route('/templates/info_share', methods=['POST'])
def info_share_post():
    sample_receive = request.form['sample_give']
    return jsonify({'msg':'저장 완료!'})

# 정보 공유 게시판 보여주기
@app.route('/templates/info_share',methods=["GET"])
def info_share_get():
    sample_list = list(db.article.find({}, {'_id': False}))
    return jsonify({'comments': '정보 공유 게시판 보여주기'})

# 자유 게시판 포스트
@app.route('/templates/info_share', methods=['POST'])
def free_board_post():
    sample_receive = request.form['sample_give']
    return jsonify({'msg':'저장 완료!'})

# 자유 게시판 보여주기
@app.route('/templates/info_share',methods=["GET"])
def free_board_get():
    sample_list = list(db.article.find({}, {'_id': False}))
    return jsonify({'comments': '정보 공유 게시판 보여주기'})
