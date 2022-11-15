//정보 공유 게시판 클릭->게시판 내용+글쓰기 버튼 불러오기
function show_info_share() {
    alert("작동")
    $('#borde_wrapper').empty()
    $('#borde_wrapper').append()
    $.ajax({
        type: "GET",
        url: "/templates/info_share",
        data: {},
        success: function (response) {
            alert('GET연결 성공')
            console.log('comments')
        }
    })
}
//공유게시판 글쓴 내용 DB에 전송
function write_info_share() {
    let upTitle = $('#userTitle').val()
    let upContents = $('#userContents').val()
    let upTime = new Date()

    $.ajax({
        type: "POST",
        url: "/templates/free_board",
        data: { title_give: upTitle, post_give: contents, time_give: upTime },
        success: function (response) {
            alert(response['msg'])
        }
    });
}