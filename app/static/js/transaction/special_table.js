$(document).on('click','#special_table' ,function(){
  console.log('Special Transactions Requested');
  $.getJSON('/homepage_data', {'type': 'special'}, function(response) {
    console.log('Special Response: ', response);
    var table_data = response.A;
    var table_HTML = '<thead><tr>'
                    + '<th>ID</th>'
                    +  '<th>Date</th>'
                    + '<th>Amount</th>'
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
                    + table_data[A]['amount'] +              '</td><td>'
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
