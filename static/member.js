function join_member() {
    let userId = $('#contents__main__userid').val();
    let userPw= $('#contents__main__pw').val();
    let userPwConfirm = $('#contents__main__pwp').val();
    let nickname = $('#contents__main__nickname').val();
    if(userId === ''){
        alert('사용하실 아이디를 입력해주세요')
    }else if(userPw ===''){
        alert('사용하실 비밀번호를 입력해주세요')
    }else if(userPw !== userPwConfirm){
        alert('비밀번호가 서로 일치하지 않습니다. 다시 확인해주십시오')
    }else if(nickname===''){
        alert('사용하실 닉네임을 입력해주세요')
    }else{
        $.ajax({
        type: 'POST',
        url: '/api/join',
        data: { userid_give:userId,
                userpw_give:userPw,
                nickname_give:nickname},
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.')
                window.location.href = '/login'
            } else {
                alert('이미 사용중인 ID입니다. 다른 ID를 사용해주세요')
            }
    }
    });
    }}

    