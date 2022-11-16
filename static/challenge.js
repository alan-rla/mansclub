//챌린지 게시판 클릭 -> 게시판 내용 + 글쓰기 버튼 불러오기
function show_challenge() {
    alert("작동")
    let temphtml = ''
    $('#borde_wrapper').empty()
    $.ajax({
        type: "GET",
        url: "/templates/challenge",
        data: {},
        success: function (response) {
            alert('GET연결 성공')
            console.log('comments')
        }
    })
    $('#borde_wrapper').append(temphtml)
}