$(document).ready(function(){
  reloadHome();
  // $.getJSON('/homepage_data', {'type': 'loadup'}, function(response) {
  //   console.log('Homepage Data Response: ', response);
  //   document.getElementById("budget_count_container").innerHTML = '&nbsp;';
  //   document.getElementById("budget_count_container").innerHTML = '<div class="huge"><b>'+ response.A + '</b></div>';
  //   document.getElementById("transaction_tag_container").innerHTML = '&nbsp;';
  //   document.getElementById("transaction_tag_container").innerHTML = '<div class="huge"><b>'+ response.B + '</b></div>';
  //   document.getElementById("no_budget_container").innerHTML = '&nbsp;';
  //   document.getElementById("no_budget_container").innerHTML = '<div class="huge"><b>'+ response.D + '</b></div>';
  //   document.getElementById("special_container").innerHTML = '&nbsp;';
  //   document.getElementById("special_container").innerHTML = '<div class="huge"><b>'+ response.E + '</b></div>';
  //   var table_data = response.C;
  //   var table_HTML = '<thead><tr>'
  //                   + '<th>ID</th>'
  //                   +  '<th>Date</th>'
  //                   + '<th>Amount</th>'
  //                   +  '<th>Name</th>'
  //                   + ' <th>Account</th>'
  //                   +  '<th>Category</th>'
  //                   +  '<th>Sub-Category</th>'
  //                   +  '<th>Tag</th>'
  //                   +  '<th>Budget</th>'
  //                   + '</tr></thead><tbody>';
  //   for(var A=0;A<table_data.length;A++) {
  //               table_HTML += '<tr data-toggle="modal" data-id="' + table_data[A]['id'] + '" data-target="#tagModal"><td>'
  //                   + table_data[A]['id'] +                  '</td><td>'
  //                   + table_data[A]['date'] +                '</td><td>'
  //                   + table_data[A]['amount'] +              '</td><td>'
  //                   + table_data[A]['name'] +                '</td><td>'
  //                   + table_data[A]['account_id'] +          '</td><td>'
  //                   + table_data[A]['category'] +            '</td><td>'
  //                   + table_data[A]['sub_category'] +        '</td><td>'
  //                   + table_data[A]['tag'] +                 '</td><td>'
  //                   + table_data[A]['budget_id'] +           '</td></tr>';
  //                 }
  //                 table_HTML += '</tbody>';
  //   document.getElementById("masterTable").innerHTML = '&nbsp;';
  //   document.getElementById("masterTable").innerHTML = table_HTML;

  // });

});

$('body').on('click', '#add_budget', function() {
  // var id = $(this).data('id');
  console.log('Clicked!');
  // $.getJSON('/dailyTag', {'action': 'click', 'id': id}, function(response) {
  //       console.log('Tagging Response: ', response);
  //       document.getElementById('id').value = response.A['id'];
  //       document.getElementById('amt').value = response.A['amount'];
  //       document.getElementById('vendor').value = response.A['vendor'];
  //       document.getElementById('category').value = response.A['category'];
  //       document.getElementById('city').value = response.A['city'];
  //       document.getElementById('state').value = response.A['state'];
  //       document.getElementById('account').value = response.A['account_id'];
  //       document.getElementById('date').value = response.A['date'];
  //       if (response.A['tag']){
  //         document.getElementById('tag').value = response.A['tag'];
  //       } else{
  //         document.getElementById('tag').value = '';
  //       }
  //       if (response.A['flag']){
  //         console.log('Checked!');
  //         $('#flagBox').prop('checked', true);
  //       } else {
  //         $('#flagBox').prop('checked', false);
  //       }
  //       $('#allBox').prop('checked', true);


  //       document.getElementById("categoryCount").innerHTML = '&nbsp;';
  //       var count = response.B
  //       var tableHTML = '';
  //       tableHTML += '<div class="list-group">';
  //       for(var A=0;A<count.length;A++) {
  //         tableHTML += '<a href="#" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">'
  //           + count[A]['tag'] + '<span class="badge badge-primary badge-pill">'
  //           + count[A]['count'] + '</span></a>';
  //            }
  //            tableHTML += '</div>';
  //           $('#categoryCount').html(tableHTML);
  //    });

});
