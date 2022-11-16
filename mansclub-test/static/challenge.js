$(document).ready(function () {
    $('#chall_box').empty()
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
                let count = rows[i]["count"];
                
                let temp_html = `<div id="chall_posts">
                                <label for=""></label>
                                <input type="text" placeholder="${user}" />
                                <label for=""></label>
                                <input type="text" placeholder="${post}" />
                                <button onclick="chall_confirm('${post_num}')">인증하기 ${count}/3</button>
                                </div>`
                
                $('#chall_box').append(temp_html)
            }
        }
    });
}

function chall_confirm(post_num) {    
    const mytoken = $.cookie("mytoken");    
    $.ajax({
        type: "POST",
        url: "/api/challenge",
        data: { token_give: mytoken, num_give: post_num },
        success: function (response) {
            if (response['confirmed']) {
                alert('이미 인증했거나 점수가 부족합니다!')
            } else {
                let point = response['doc']['point']
                let count = Number(response['doc']['count'])            
                if (point < 100) {
                    alert('인증하기 위한 등급이 부족합니다!')
                } else if (point >= 100 && count === 3){
                    alert('인증이 이미 완료됐습니다!')
                } else {
                    alert('인증 완료!')
                    window.location.reload()
                }
            }
        }
    })
}