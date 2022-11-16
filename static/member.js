function join_member() {
    let userId = $('contents__main__userid').val()
    let userPw= $('#contents__main__pw').val()
    let userPwConfirm = $('#contents__main__pwp').val()
    let nickname = $('#contents__main__nickname').val()
    const confirmPasswordElement = document.getElementById("contents__main__pwp");
        $.ajax({
        type: 'POST',
        url: '/member/join',
        data: { userid_give:userId ,userpw_give:userPw,nickname_give:nickname},
        success: function (response) {
        alert(response['msg'])
    }
    });
    }
    