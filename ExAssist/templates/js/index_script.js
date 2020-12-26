$(document).ready(function(){
  $('#dropdown-status li').click(function(){
      var status = $(this).text();
      $('#status-show').text(status);
      if(status == 'All'){
        $('#result-table tr').filter(function() {
            $(this).toggle(true);
          });
      } 
      else
      {
        $('#result-table tbody tr').filter(function() {
            $(this).toggle($('.status', this).text().indexOf(status) > -1);
          });
      }
  });

//  $('#create-button').click(function(){
//      var name = $('#list-name').val();
//      if (typeof(Storage) !== "undefined") {
//          localStorage.setItem(name, []);
//     } else {
//         // Sorry! No Web Storage support..
//         alert('Sorry! You browser does not support localStorage!');
//     }
//     $('#list-modal').modal('toggle');
//  });

    $("#comment-search").on("keyup", function(){
        var value = $(this).val();
        $("#result-table tbody tr").filter(function(){
            $(this).toggle($('.comments', this).text().indexOf(value) > -1);
        });
    });

});


