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


