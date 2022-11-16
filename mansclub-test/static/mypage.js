function show_pw_change(){
    $('#contents__main').empty();
    const passwordHtml = `<input id="pw_original" type="password" placeholder="기존 패스워드">
    <input id="pw_change" type="password" placeholder="변경할 패스워드">
    <input id="pw_change_confirm" type="password" placeholder="패스워드 확인">
    <input type="button" value="확인" onclick="passwordChange()">
    <input type="button" value="취소" onclick="show_return()">`
    $('#contents__main').append(passwordHtml);
}
function show_nick_change(){
    $('#contents__main').empty();
    const nicknamedHtml = `<h1>현재 닉네임: {{nickname}}</h1>
    <input type="password" placeholder="변경할 닉네임">
    <input type="button" value="확인" onclick="nicknameChange()">
    <input type="button" value="취소" onclick="show_return()">`
    $('#contents__main').append(nicknamedHtml);
}
function go_leave(){
    window.location.href="/leave"
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
  />`
  $('#contents__main').append(mypageHtml);
}

function passwordChange(){
    mytoken=$.cookie('mytoken');
    const pwOriginal = $('#pw_original').val();
    const pwChange = $('#pw_change').val();
    const pwChangeConfirm = $('#pw_change_confirm').val();
        $.ajax({
        type: "POST",
        url: "/api/pwchange",
        data: {token_give:mytoken,pwconfirm_give:pwconfirm},
        success: function (response) {
            console.log(response)
            //     if(response['result']==='fail'){
            //         alert('비밀번호가 틀립니다. 다시 확인해주세요')
            //     }else{
            //         $.removeCookie('mytoken');
            //         alert('탈퇴가 완료되었습니다. 감사합니다.')
            //         window.location.href="/login";
            //     }
            //   }
        }})}
          


function nicknameChange(){

}