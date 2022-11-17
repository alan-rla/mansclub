$(document).ready(function () {
    $('#chall_posts').empty()
    show_challenge();
});

function post_challenge() {
    let url = $("#linkdata").val();
    const mytoken = $.cookie("mytoken");
    let score = 10;
    $.ajax({
      type: "POST",
      url: "/templates/challenge",
      data: { token_give: mytoken, url_give: url, score_give: score },
      success: function (response) {
        alert(response["msg"]);
        window.location.reload();
      },
    });
}

function show_challenge() {
    $.ajax({
        type: "GET",
        url: "/templates/challenge",
        data: {},
        success: function (response) {
            let rows = response["challenges"];
            for (i = 0; i < rows.length; i++) {
                let post_num = rows[i]["num"];
                let user = rows[i]["writer"];
                let post = rows[i]["url"];
                let count = rows[i]["confirmer"].length;
                
                let temp_html = `
              <tr>
              <td>${user}</td>
              <td>${post}</td>
              <td><button onclick="chall_confirm('${post_num}')">인증  ${count}/3</button></td>
              </tr>`

                // let temp_html = ` 
                //     < id="chall_posts"><span>${user} ${post}</span><button onclick="chall_confirm('${post_num}')">인증하기 ${count}/3</button></li>
                     

                
                $('#chall_posts').append(temp_html)
            }
        }
    });
}

function chall_confirm(post_num) {    
    const mytoken = $.cookie("mytoken");
    
    if (!mytoken) {
        alert('로그인이 필요합니다!')
    } else {
        $.ajax({
            type: "POST",
            url: "/api/challenge",
            data: { token_give: mytoken, num_give: post_num },
            success: function (response) {
                if (response['writer']) {
                    alert('게시글 작성자는 인증하지 못합니다!')
                } else if (response['confirmed']) {
                    alert('이미 인증했거나 점수가 부족합니다!')
                } else if (response['count_full']) {
                    alert('인증이 이미 완료됐습니다! (3/3)')
                } else if (response['complete']) {                                        
                    alert('인증 완료!')
                    window.location.reload()
                }
            }
        })
    }
}