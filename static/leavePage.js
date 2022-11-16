$.ajax({
    type: "POST",
    url: "/guhaejo/view-count",
    data: {post_num:post_num,view_count:parseInt(view_count)+1},
    success: function (response) {
  
          }
      });
  }