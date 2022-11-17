
function show_rank() {
    $.ajax({
      type: 'GET',
      url: '/rank',
      data: {},
      success: function (response) {
        let rows = response['rank']
        for (let i = 0; i < rows.length; i++) {
            let rank = i+1;
            let nick = rows[i]['nick'];
            let point = rows[i]['point'];
            let grade = ''
                if (point < 100) {
                    grade = '슈퍼겁쟁이'
                } else if (point < 300) {
                    grade = '겁쟁이'
                } else if (point < 500) {
                    grade = '사나이'
                } else if (point < 700) {
                    grade = '진짜사나이'
                } else if (point >= 700) {
                    grade = '슈퍼사나이'
                }
            let temp_html = `
                            <tr>
                            <td>${rank}</td>
                            <td>${nick}</td>
                            <td>${grade}</td>
                            <td>${point}</td>
                            </tr>`
                $('#rank_posts').append(temp_html)
        }
      }
    });
}
  