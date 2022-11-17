$(document).ready(function () {
  $('#today_news').empty()
  show_news();
});
function show_news() {
  $.ajax({
    type: 'GET',
    url: '/news',
    data: {},
    success: function (response) {
      let rows = response['news']
      for (let i = 0; i < rows.length; i++) {
        let rank = i+1;
        let title = rows[i]['title'];
        let link = rows[i]['link'];
        let temp_html = `
                                    <strong>${rank} </strong><a href="${link}" >${title}</a><br>
                                    `
        $('#today_news').append(temp_html)
      }
    }
  });
}
