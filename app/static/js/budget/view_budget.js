$(document).on('click','#budget_viewer' ,function(){
  console.log('Viewing Budget Status');
  $.getJSON('/budget_edit', {'action': 'view'}, function(response) {
    console.log('Viewing Budget Response', response);
    var budgets = response.A;
    document.getElementById("view_budget_detail").innerHTML = '&nbsp;';
    var budgeHTML = '';
      for(var A=0;A<budgets.length;A++) {

      budgeHTML += '<div class="progress-group">'
      + budgets[A]['name'] + '<span class="pull-right"><b>$'
      + budgets[A]['total'] + '</b>/$'
      + budgets[A]['amount'] +   '</span><div class="progress progress-sm"><div class="progress-bar bg-primary" style="width: '
      + Math.floor((budgets[A]['total']/budgets[A]['amount'])*100) + '%"></div></div></div>';
    }

    console.log(budgeHTML);
    document.getElementById("view_budget_detail").innerHTML = budgeHTML;
    });
  });


