$(document).on('click', '#tags_available .list-group-item', function(e) {
  //GET THE TEXT INSIDE THAT SPECIFIC LI
  var content= $(this).text().replace(/[0-9]/g, '');
  console.log('List Group Click: ', content);
  //PLACE THE TEXT INSIDE THE INPUT FIELD, YOU CAN CHANGE YOUR SELECTOR TO TARGET THE RIGHT INPUT
  $('#tag_tag').val(content);
  //HERE YOU CAN DO SOMETHING ELSE LIKE SIBMITING THE FORM, OR CLICK A BUTTON.. OR SOMETHING ELSE
    });

$(document).on('click', '#budgets_available .list-group-item', function(e) {
  //GET THE TEXT INSIDE THAT SPECIFIC LI
  var content= $(this).text().replace(/[0-9]/g, '');
  console.log('List Group Click: ', content);
  //PLACE THE TEXT INSIDE THE INPUT FIELD, YOU CAN CHANGE YOUR SELECTOR TO TARGET THE RIGHT INPUT
  $('#tag_budget').val(content);
  //HERE YOU CAN DO SOMETHING ELSE LIKE SIBMITING THE FORM, OR CLICK A BUTTON.. OR SOMETHING ELSE
    });
