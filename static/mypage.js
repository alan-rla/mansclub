function show_pw_change(){
    $('#contents__main').empty();
    const passwordHtml = `<input id="pw_original" type="password" placeholder="기존 패스워드">
    <input id="pw_change" type="password" placeholder="변경할 패스워드">
    <input id="pw_change_confirm" type="password" placeholder="패스워드 확인">
    <input id="confirmbtn" type="button" value="확인" onclick="passwordChange()">
    <input id="canclebtn" type="button" value="취소" onclick="show_return()">`
    $('#contents__main').append(passwordHtml);
}
function show_nick_change(){
    mytoken=$.cookie('mytoken');
    $('#contents__main').empty();
    $.ajax({
      type: "POST",
      url: "/api/nickcheck",
      data: {token_give:mytoken},
      success: function (response) {
              const mynickname=response['nick']

              const nicknamedHtml = `<h1>현재 닉네임:${mynickname}</h1>
    <input id="nickname_change" type="text" placeholder="변경할 닉네임">
    <input id="confirmbtn" type="button" value="확인" onclick="nicknameChange()">
    <input id="canclebtn" type="button" value="취소" onclick="show_return()">`
    $('#contents__main').append(nicknamedHtml);
          }
      });
}
function go_leave(){
    window.location.href="/leave"
}
function go_home(){
  window.location.href="/"
}
function show_return(){
    $('#contents__main').empty();
    const mypageHtml=`   <input
    id="contents__main__paC"
    type="button"
    value="비밀번호 변경"
    onclick="show_pw_change()"
  />
  <input
    id="contents__main__profC"
    type="button"
    value="닉네임 변경"
    onclick="show_nick_change()"
  />
  <input
    id="contents__main__withdraw"
    type="button"
    value="탈퇴하기"
    onclick="go_leave()"
  />
  <input
    id="contents__main__home"
    type="button"
    value="홈으로"
    onclick="go_home()"
  />`
  $('#contents__main').append(mypageHtml);
}

function passwordChange(){
    mytoken=$.cookie('mytoken');
    const pwOriginal = $('#pw_original').val();
    const pwChange = $('#pw_change').val();
    const pwChangeConfirm = $('#pw_change_confirm').val();

    if(pwChange!==pwChangeConfirm){
      alert('새로운 비밀번호가 일치하지 않습니다.')
    }else{
    $.ajax({
      type: "POST",
      url: "/api/pwchange",
      data: {token_give:mytoken,pw_give:pwOriginal,new_pw_give:pwChange},
      success: function (response) {
              if(response['result']==='fail'){
                  alert('비밀번호가 틀립니다. 다시 확인해주세요')
              }else{$.removeCookie('mytoken');
              alert('비밀번호 변경이 완료되었습니다. 다시 로그인 해주세요')
              window.location.href="/login";
            }
          }
      });
}
}


function nicknameChange(){
  mytoken=$.cookie('mytoken');
  const nicknameChange = $('#nickname_change').val();

  $.ajax({
    type: "POST",
    url: "/api/nicknamechange",
    data: {token_give:mytoken,nickname_give:nicknameChange},
    success: function (response) {
            if(response['result']==='fail'){
                alert('이미 사용중인 닉네임입니다.')
            }else{$.removeCookie('mytoken');
            alert('닉네임이 변경되었습니다. 다시 로그인해주세요')
            window.location.href="/login";
          }
        }
    });
}