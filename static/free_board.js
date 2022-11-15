//자유게시판 클릭 -> 게시판 내용 + 글쓰기 버튼 불러오기
function show_free_board() {
    alert("작동")
    $('#borde_wrapper').empty()
    $('#borde_wrapper').append()
    $.ajax({
        type: "GET",
        url: "/templates/free_board",
        data: {},
        success: function (response) {
            alert('GET연결 성공')
            console.log(response['comments'])
        }
    })
}
//자유게시판 글쓴 내용 DB에 저장
function write_free_board() {
    let upTitle = $('#userTitle').val()
    let upContents = $('#userContents').val()
    // let upId =$('#userId').val()
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