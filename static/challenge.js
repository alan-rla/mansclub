//챌린지 게시판 클릭 -> 게시판 내용 + 글쓰기 버튼 불러오기
// function show_challenge() {
//     alert("작동")
//     let temphtml = ''
//     $('#borde_wrapper').empty()
//     $.ajax({
//         type: "GET",
//         url: "/templates/challenge",
//         data: {},
//         success: function (response) {
//             alert('GET연결 성공')
//             console.log('comments')
//         }
//     })
//     $('#borde_wrapper').append(temphtml)
// }

function show_challenge() {
    $.ajax({
        type: "GET",
        url: "/templates/challenge",
        data: {},
        success: function (response) {
            let rows = response["challenges"];
            for (i = 0; i < rows.length; i++) {
                let post_num = rows[i]["post_num"]
                let user = rows[i]["user"];
                let post = rows[i]["post"];
                let count = rows[i]["count"];
                let temp_html = `<table class="table">
                                    <thead>
                                    <tr>
                                        <th scope="row">${user}</th>
                                        <th>${post}</th>
                                        <button type="button" class="btn btn-primary" onclick="chall_confirm(${post_num})">인증하기 ${count}/3</button>
                                    </tr>
                                    </thead>
                                </table>`
                $('#chall_posts').append(temp_html)
            }
        }
    })
}
function chall_confirm(post_num) {
    const mytoken = $.cookie('mytoken')
    $.ajax({
        type: "POST",
        url: "/api/challenge",
        data: { 'token_give': mytoken, 'num_give': post_num },
        success: function (response) {
            let point = response['point']
            if (point < 100) {
                alert('인증하기 위한 등급이 부족합니다!')
            } else {
                alert('인증 완료')
            }
        }
    })
}