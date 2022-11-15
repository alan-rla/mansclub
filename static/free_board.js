function show_free_board() {
    alert("작동")
    $('#borde_wrapper').empty()
    $('#borde_wrapper').append()
}

function write_free_board() {
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