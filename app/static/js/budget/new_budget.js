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

    });
    $.getJSON('/homepage_data', {'type': 'loadup'}, function(response) {
      console.log('Load Up response: ', response);
      document.getElementById("budget_count_container").innerHTML = '&nbsp;';
      document.getElementById("budget_count_container").innerHTML = '<div class="huge"><b>'+ response.A + '</b></div>';
      document.getElementById("transaction_tag_container").innerHTML = '&nbsp;';
      document.getElementById("transaction_tag_container").innerHTML = '<div class="huge"><b>'+ response.B + '</b></div>';
      var table_data = response.C;
      var table_HTML = '<thead><tr>'
                      + '<th>ID</th>'
                      +  '<th>Date</th>'
                      +  '<th>Name</th>'
                      + ' <th>Account</th>'
                      +  '<th>Category</th>'
                      +  '<th>Sub-Category</th>'
                      +  '<th>Tag</th>'
                      +  '<th>Budget</th>'
                      + '</tr></thead><tbody>';
      for(var A=0;A<table_data.length;A++) {
                  table_HTML += '<tr data-toggle="modal" data-id="' + table_data[A]['id'] + '" data-target="#tagModal"><td>'
                      + table_data[A]['id'] +                  '</td><td>'
                      + table_data[A]['date'] +                '</td><td>'
                      + table_data[A]['name'] +                '</td><td>'
                      + table_data[A]['account_id'] +          '</td><td>'
                      + table_data[A]['category'] +            '</td><td>'
                      + table_data[A]['sub_category'] +        '</td><td>'
                      + table_data[A]['tag'] +                 '</td><td>'
                      + table_data[A]['budget_id'] +           '</td></tr>';
                    }
                    table_HTML += '</tbody>';
      document.getElementById("masterTable").innerHTML = '&nbsp;';
      document.getElementById("masterTable").innerHTML = table_HTML;

    });

  });


