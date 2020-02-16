$(document).on('click','#tagDone' ,function(){
  console.log('Saving Transaction Data');
  var id = document.getElementById('tag_id').value;
  console.log('ID', id);
  var budget = document.getElementById('tag_budget').value;
  var tag = document.getElementById('tag_tag').value;

  if ( $('#tag_all_box').is(':checked') ) {
      var tag_all = 'Yes';
            }
  else {
      var tag_all = 'No';
            }
  if ( $('#budget_all_box').is(':checked') ) {
      var budget_all = 'Yes';
            }
  else {
      var budget_all = 'No';
            }

  console.log('tag_all: ', tag_all);
  console.log('budget_all: ', budget_all);

  $.getJSON('/transaction_edit', {'action': 'update', 'id': id, 'tag': tag, 'budget': budget, 'tag_all': tag_all, 'budget_all': budget_all}, function(response) {
    console.log('Tagging Done Response: ', response);

      toastr.info(response.A);
      toastr.info(response.B);



    }).done(function() {
      reloadHome();

    });


  });


