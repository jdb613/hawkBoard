$(document).on('click','#add_budget' ,function(){
  console.log('Add Budget Data Requested');
  $.getJSON('/budget_edit', {'action': 'edit'}, function(response) {
    console.log('Add Budget Response: ', response);
    var budgets = response.A;
    document.getElementById("existing_budgets").innerHTML = '&nbsp;';
    var budgeHTML = '';
      for(var A=0;A<budgets.length;A++) {

      budgeHTML += '<li class="list-group-item" id="'
      + budgets[A]['id'] + '"><span class="badge">$'
      + budgets[A]['amount'] + '</span>'
      + budgets[A]['name'] +   '</li>';
    }

    document.getElementById("existing_budgets").innerHTML = budgeHTML;
    });


});

$(document).on('click','#save_new_budget' ,function(){
  console.log('Saving New Budget Data');
  var amount = document.getElementById('new_budget_amount').value;
  var name = document.getElementById('new_budget_name').value;
  console.log('Name', name);
  console.log('Amount', amount);

  $.getJSON('/budget_edit', {'action': 'save', 'name': name, 'amount': amount}, function(response) {
    console.log('New Budget Response: ', response);
    toastr.info(response.A);
    }).done(function() {
      reloadHome();
    });

  });


