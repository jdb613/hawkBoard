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
      });
      $.getJSON('/homepage_data', {'type': 'loadup'}, function(response) {
        console.log('budget_data response: ', response);
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
      });
      $.getJSON('/homepage_data', {'type': 'loadup'}, function(response) {
        console.log('budget_data response: ', response);
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
