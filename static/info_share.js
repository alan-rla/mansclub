//정보 공유 게시판 클릭->게시판 내용+글쓰기 버튼 불러오기
function show_info_share() {
    let temphtml = `<div id="writeWrapper">
                            <div class="writeTable">
                                <div>제목</div>
                                <div>내용</div>
                            </div>
                            <div class="top" id="test01">
                                <label for=""></label><input type="text" id="userTitle">
                                <label for=""></label><input type="text" id="userContents">
                                <button class="writeBtnPlus" onclick="write_info_share()">등록</button>
                            </div>
                        </div>
                        <button class="writeBtn" onclick="writing()" type="button">글쓰기</button>`
    $('#borde_wrapper').empty()
    alert("정보 공유 게시판을 불러옵니다")
    $.ajax({
        type: "GET",
        url: "/templates/info_share",
        data: {},
        success: function (response) {
            alert('GET연결 성공')
            console.log(response['comments'])
            let rows = response['comments']
            for (let i = 0; i < rows.length; i++) {
                let number = rows[i]
                let title = rows[i]
                let contents = rows[i]
                let writer = row[i]
                let date = rows[i]
                let tempImfoShare = `<div class="borde_list">
                                <div class="top">
                                    <textarea id="numId" class="num">${number}</textarea>
                                    <textarea id="titleId" class="title">${title}</textarea>
                                    <textarea id="contentsId" class="contents">${contents}</textarea>
                                    <textarea id="writerId" class="writer">${writer}</textarea>
                                    <textarea id="dateId" class="date">${date}</textarea>
                                </div>`
                $('#borde_wrapper').append(tempImfoShare)
            }
        }
    })
    $('#borde_wrapper').append(temphtml)
}
//공유게시판 글쓴 내용 DB에 전송
function write_info_share() {
    let upTitle = $('#userTitle').val()
    let upContents = $('#userContents').val()
    let upTime = new Date()
    alert("공유 게시글을 등록합니다")

    $.ajax({
        type: "POST",
        url: "/templates/free_board",
        data: { title_give: upTitle, post_give: contents, time_give: upTime },
        success: function (response) {
            alert(response['msg'])
        }
    });
}