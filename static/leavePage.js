
function leave(){
    $.ajax({
    type: "POST",
    url: "/leave",
    data: {id_give:id},
    success: function (response) {
  
          }
      });
  }


