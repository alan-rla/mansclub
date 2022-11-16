# 사나이클럽
### 소개
운동 덕후들의 커뮤니티
<img src="https://pbs.twimg.com/media/Ddyfl16VwAAQCZj?format=jpg&name=medium" width="100%" height="100%"></img>
운동을 좋아하거나 관심있는 사람들이 모여 같이 운동하고
정보를 공유하며 여러 운동 관련 챌린지들을 통해 운동에 재미를 알아갈 수 있게 해주는 플랫폼입니다.

### 와이어프레임
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FbfGe2w%2FbtrRddAmtOE%2FgbMZKTqmttNXLPYwHLCpAk%2Fimg.jpg" width="100%" height="100%"></img>

### 개발해야 하는 기능들
|기능|Method|URL|request|response|
|---|---|---|---|---|
|로그인|POST|/api/login|{'id' : id, 'pw' : pw}|-|
|회원가입|POST|/api/membership|{'id' : id, 'pw' : pw,<br/> 'nickname': nickname}|가입 완료 메시지|
|회원 점수|GET|/api/membership|"{'id' : id, 'point' : point,<br/>'tier':tier}"|point|
|회원 정보 수정|POST|/api/membership|{'point' : point }|수정 완료 메시지|
|게시글 작성|POST|/api/posts|{'post_num':post_num,'title': title, <br/>'content':content,'tag':tag}|작성 완료 메시지|
|게시글 수정|POST|/api/posts|{'post_num':post_num,'title': title, <br/>'content':content, 'tag':tag}|수정 완료 메시지|
|스포츠 뉴스|GET|/api/news|-|news|
|탈퇴하기|POST|/api/membership|{'id' : id, 'pw' : pw}|탈퇴 완료 메시지|
|챌린지|POST/GET|/api/membership|"{'id' : id, 'point' : point }"|점수 업 완료메시지/<br/>내 점수 및 티어|

### 데이터 베이스

|user 테이블|article 테이블|
|---|---|
|ID|id|
|PW|title|
|nickname|content|
|point|date|
|tier|tag|
|-|point|

..