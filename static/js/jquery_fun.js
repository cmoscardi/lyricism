function butts(color){
  return function(){
	  $('div').css('color',color);
  }
}
$(document).ready(function(){
	setTimeout(butts('blue'),2200);
	setTimeout(butts('yellow'),1000);
});
