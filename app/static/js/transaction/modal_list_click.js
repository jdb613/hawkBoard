$(document).on('click', '#tags_available .list-group-item', function(e) {
  // update active class
  var that_tag = $(this);
  console.log('Active Tag: ', that_tag);
  that_tag.parent().find('li').removeClass('active');
  that_tag.addClass('active');
  //GET THE TEXT INSIDE THAT SPECIFIC LI
  var content= $(this).text().replace(/[0-9]/g, '');
  console.log('List Group Click: ', content);
  //PLACE THE TEXT INSIDE THE INPUT FIELD, YOU CAN CHANGE YOUR SELECTOR TO TARGET THE RIGHT INPUT
  $('#tag_tag').val(content);
  //HERE YOU CAN DO SOMETHING ELSE LIKE SIBMITING THE FORM, OR CLICK A BUTTON.. OR SOMETHING ELSE
    });

$(document).on('click', '#budgets_available .list-group-item', function(e) {
  // update active class
  var that_budget = $(this);
  console.log('Active Budget: ', that_budget);
  that_budget.parent().find('li').removeClass('active');
  that_budget.addClass('active');
  //GET THE TEXT INSIDE THAT SPECIFIC LI
  var content= $(this).text().replace(/[0-9]/g, '');
  console.log('List Group Click: ', content);
  //PLACE THE TEXT INSIDE THE INPUT FIELD, YOU CAN CHANGE YOUR SELECTOR TO TARGET THE RIGHT INPUT
  $('#tag_budget').val(content);
  //HERE YOU CAN DO SOMETHING ELSE LIKE SIBMITING THE FORM, OR CLICK A BUTTON.. OR SOMETHING ELSE
    });
