from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
import certifi
from bson.json_util import dumps

ca=certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.cctcpnr.mongodb.net/?retryWrites=true&w=majority')
db = client.mansclub

# 메인페이지
@app.route('/')
def home():
    return render_template('index.html')

# 자유게시판 포스트
@app.route('/templates/free_board', methods=['POST'])
def free_board_post():
    writer_receive = request.form['writer_give'] ##작성자 계정
    num_receive = request.form['num_give']  ##게시글 번호
    title_receive = request.form['title_give'] ##제목
    post_receive = request.form['post_give'] ## 게시글 내용
    time_receive = request.form['time_give'] ## 게시글 작성 시간

    doc = {
        'writer':writer_receive,
        'num':num_receive,
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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)