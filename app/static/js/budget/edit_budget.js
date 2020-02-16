$(document).on('click','#edit_budget' ,function(){
  console.log('Edit Budget Data Requested');
  $.getJSON('/budget_edit', {'action': 'edit'}, function(response) {
    console.log('Edit Budget Response: ', response);
    var budgets = response.A;
    document.getElementById("edit_budgets_available").innerHTML = '&nbsp;';
    var budgeHTML = '';
      for(var A=0;A<budgets.length;A++) {

      budgeHTML += '<li class="list-group-item" id="'
      + budgets[A]['id'] + '"><span class="badge">$'
      + budgets[A]['amount'] + '</span>'
      + budgets[A]['name'] +   '</li>';
    }

    document.getElementById("edit_budgets_available").innerHTML = budgeHTML;
    });


});

$(document).on('click', '#edit_budgets_available .list-group-item', function(e) {
  //GET THE TEXT INSIDE THAT SPECIFIC LI
  var id= $(this).attr("id");
  var name = $(this).text().replace(/[^a-zA-Z]+/g, '');
  var amount = $(this).text().replace(/\D+/g, '');

  console.log('Budget Selected: ', id);
  console.log('Budget Name: ', name);
  console.log('Budget Amount: ', amount);
  //PLACE THE TEXT INSIDE THE INPUT FIELD, YOU CAN CHANGE YOUR SELECTOR TO TARGET THE RIGHT INPUT
  $('#edit_budget_id').val(id);
  $('#edit_budget_name').val(name);
  $('#edit_budget_amount').val(amount);
  //HERE YOU CAN DO SOMETHING ELSE LIKE SIBMITING THE FORM, OR CLICK A BUTTON.. OR SOMETHING ELSE
    });

$(document).on('click','#save_old_budget' ,function(){
      console.log('Saving Updated Budget');
      var id= $('#edit_budget_id').val();
      var name = $('#edit_budget_name').val().replace(/[0-9]/g, '');
      var amount = $('#edit_budget_amount').val().replace(/\D+/g, '');
      console.log('Budget Selected: ', id);
      console.log('Budget Name: ', name);
      console.log('Budget Amount: ', amount);
      $.getJSON('/budget_edit', {'action': 'save', 'id': id, 'name': name, 'amount': amount}, function(response) {
        console.log('Save Old Budget Response: ', response);
      }).done(function() {
        reloadHome();
      });
    });

$(document).on('click','#delete_budget' ,function(){
      console.log('Deleting Budget');
      var id= $('#edit_budget_id').val();
      var name = $('#edit_budget_name').val().replace(/[0-9]/g, '');
      var amount = $('#edit_budget_amount').val().replace(/\D+/g, '');
      console.log('Budget Selected: ', id);
      console.log('Budget Name: ', name);
      console.log('Budget Amount: ', amount);
      $.getJSON('/budget_edit', {'action': 'delete', 'id': id, 'name': name, 'amount': amount}, function(response) {
        console.log('Delete Budget Response: ', response);
        toastr.info(response.A);
      }).done(function() {
        reloadHome();
      });

    });
