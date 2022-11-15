function show_info_share() {
    alert("작동")
    $('#borde_wrapper').empty()
    $('#borde_wrapper').append()
}

function write_info_share() {
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