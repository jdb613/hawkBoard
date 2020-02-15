$(document).on('click','tr' ,function(){
  var id = $(this).data('id');
  console.log('id selected: ', id);
  $.getJSON('/transaction_edit', {'action': 'table_click', 'id': id}, function(response) {
        console.log('Data for Edit Transaction Modal: ', response);
        document.getElementById('tag_id').value = response.A['id'];
        document.getElementById('tag_date').value = response.A['date'];
        document.getElementById('tag_name').value = response.A['name'];
        document.getElementById('tag_account').value = response.A['account_id'];
        document.getElementById('tag_category').value = response.A['category'];
        document.getElementById('tag_sub_category').value = response.A['sub_category'];
        document.getElementById('tag_tag').value = response.A['tag'];
        document.getElementById('tag_budget').value = response.A['budget_id'];

        document.getElementById("tags_available").innerHTML = '&nbsp;';
        var tag_count = response.B;
        var budget_count = response.C;
        var tagdropHTML = '';
        var budgetlistHTML = '';
        if (tag_count.length > 0){
          console.log('Tags Detected', tag_count);
          for(var A=0;A<tag_count.length;A++) {
            tagdropHTML += '<li class="list-group-item"><span class="badge">'
              + tag_count[A]['count'] + '</span>'
              + tag_count[A]['tag'] + '</li>';
               }
              $('#tags_available').html(tagdropHTML);
        } else {
          console.log('No Tags to Populate List');
        }

        if (budget_count.length > 0){
          console.log('Budgets Detected', budget_count);

          for(var A=0;A<budget_count.length;A++) {
            budgetlistHTML += '<li class="list-group-item"><span class="badge">'
              + budget_count[A]['count'] + '</span>'
              + budget_count[A]['Budget'] + '</li>';
               }
              $('#budgets_available').html(budgetlistHTML);
        } else {
          console.log('No Budgets to Populate List');
        }

        // if ()
        //   $("#budgets_available").val(existingTag).find("option[value=" + existingTag +"]").attr('selected', true);
        // } else {
        //   console.log('No Preexisting Tag to Preselect');
        // }
        // if (response.A['flag']){
        //   console.log('Checked!');
        //   $('#flagBox').prop('checked', true);
        // } else {
        //   $('#flagBox').prop('checked', false);
        // }
        // $('#allBox').prop('checked', false);
        // if (response.A['comments']){
        //   console.log('Comments!', comments);
        //   document.getElementById('comments').value = response.A['comments'];
        // } else {
        //   document.getElementById('comments').value ='';
        // }
        // if (response.A['spendEx'] == "No"){
        //   console.log("SpendEx is Checked")
        //   $('#exBox').prop('checked', false);
        // } else{
        //   $('#exBox').prop('checked', true);
        // }
        // $('#exAllBox').prop('checked', false);


     });

});
