function reloadHome() {
  console.log('Reloading Homepage');
  $.getJSON('/homepage_data', {'type': 'loadup'}, function(response) {
    console.log('Homepage Data Response: ', response);
    document.getElementById("budget_count_container").innerHTML = '&nbsp;';
    document.getElementById("budget_count_container").innerHTML = '<div class="huge"><b>'+ response.A + '</b></div>';
    document.getElementById("transaction_tag_container").innerHTML = '&nbsp;';
    document.getElementById("transaction_tag_container").innerHTML = '<div class="huge"><b>'+ response.B + '</b></div>';
    document.getElementById("no_budget_container").innerHTML = '&nbsp;';
    document.getElementById("no_budget_container").innerHTML = '<div class="huge"><b>'+ response.D + '</b></div>';
    document.getElementById("special_container").innerHTML = '&nbsp;';
    document.getElementById("special_container").innerHTML = '<div class="huge"><b>'+ response.E + '</b></div>';
    var table_data = response.C;
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
      $('#masterTable tr').remove();
      $('#masterTable').html(table_HTML);


  });
}

function toasta(data) {
  for(var A=0;A<data.length;A++) {
    console.log("Notify Test: ", data[A]);
    toastr.info(data[A]);
}
}
