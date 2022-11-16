//자유게시판 클릭 -> 게시판 내용 + 글쓰기 버튼 불러오기
function show_free_board() {
    let temphtml = `<div id="writeWrapper">
                            <div class="writeTable">
                                <div>제목</div>
                                <div>내용</div>
                            </div>
                            <div class="top" id="test01">
                                <label for=""></label><input type="text" id="userTitle">
                                <label for=""></label><input type="text" id="userContents">
                                <button class="writeBtnPlus" onclick="write_free_board()">등록</button>
                            </div>
                        </div>
                        <button class="writeBtn" onclick="writing()" type="button">글쓰기</button>`
    $('#borde_wrapper').empty()
    alert("자유게시판을 불러옵니다")
    $.ajax({
        type: "GET",
        url: "/templates/free_board",
        data: {},
        success: function (response) {
            alert('GET연결 성공')
            console.log(response['comments'])
            let rows = response['comments']
            for (let i = 0; i < rows.length; i++) {
                let number = rows[i]
                let title = rows[i]
                let contents = rows[i]
                let date = rows[i]
                let tempFreeShare = `<div class="borde_list">
                                <div class="top">
                                    <textarea id="titleId" class="title">${number}</textarea>
                                    <textarea id="numId" class="num">${title}</textarea>
                                    <textarea id="contentsId" class="contents">${contents}</textarea>
                                    <textarea id="writerId" class="writer">${date}</textarea>
                                    <textarea id="dateId" class="date">${date}</textarea>
                                </div>`
                $('#borde_wrapper').append(tempFreeShare)

            }
        }
    })
    $('#borde_wrapper').append(temphtml)
}
//자유게시판 글쓴 내용 DB에 저장
function write_free_board() {
    let upTitle = $('#userTitle').val()
    let upContents = $('#userContents').val()
    let upTime = new Date()
    alert("자유 게시글을 등록합니다")

    $.ajax({
        type: "POST",
        url: "/templates/free_board",
        data: { title_give: upTitle, post_give: contents, time_give: upTime },
        success: function (response) {
            alert(response['msg'])
        }
    });
}