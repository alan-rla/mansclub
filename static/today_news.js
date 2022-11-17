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
      for (const row of rows) {
        let rank = row['rank']
        let title = row['title']
        let link = row['link']

        let temp_html = `
                                    <strong>${rank} </strong><a href="${link}" >${title}</a><br>
                                    `
        $('#today_news').append(temp_html)
      }
    }
  });
}
