
function leave(){
    mytoken=$.cookie('mytoken')
    pwconfirm = $('#contents__main__pwp').val();

    $.ajax({
    type: "POST",
    url: "/api/leave",
    data: {token_give:mytoken,pwconfirm_give:pwconfirm},
    success: function (response) {
        console.log(response)
            if(response['result']==='fail'){
                alert('비밀번호가 틀립니다. 다시 확인해주세요')
            }else{
                $.removeCookie('mytoken');
                alert('탈퇴가 완료되었습니다. 감사합니다.')
                window.location.href="/login";
            }
          }
      });
  }


