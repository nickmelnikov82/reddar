
	var colors = [
	'linear-gradient(90deg, #f1f2b5 10%, #135058 90%)',
	'linear-gradient(90deg, #a770ef 10%, #cf8bf3 90%)',
	'linear-gradient(90deg, #20002c 10%, #cbb4d4 90%)',
	'linear-gradient(90deg, #000046 10%, #1cb5e0 90%)',
	'linear-gradient(90deg, #4ac29a 10%, #bdfff3 90%)',
	'linear-gradient(90deg, #FD6F46 10%, #FB9832 90%)', 
	'linear-gradient(90deg, #01a99c 10%, #0698b1 90%)',
	'linear-gradient(90deg, #99D22B 10%, #FBFF00 90%)',
	'inear-gradient(90deg, #50C9C3 10%, #96DEDA 90%)',
	'linear-gradient(90deg, #d64759 10%, #da7352 90%)',
	'linear-gradient(90deg,#224e4d 10%,#083023 90%)'
	];


$(".grid-item").hover(
	function() {
		$(this).css("background-color", colors[Math.floor(Math.random() * colors.length)]);
	}, function() {
		$(this).css("background-color","");
});

$(".grid-item:even" ).addClass("card-style1")
$(".grid-item:odd" ).addClass("card-style2")
$('.grid').masonry({
      // set itemSelector so .grid-sizer is not used in layout
      itemSelector: '.grid-item',
      // use element for option
      columnWidth: 200,
      percentPosition: true,
      transitionDuration: '0.2s',
      isInitLayout: false
  })


$(window).scroll(function(){
	if($(window).scrollTop() == $(document).height() - $(window).height()){

		$('div#loadmoreajaxloader').show();
		$.ajax({
			url: "search",
			data: {"query": $("#query").val(),"page":$("#page").val()},
			success: function(html){
				if(html){
					var $elements = $( html );
					if((parseInt($("#page").val()) + 1) % parseInt($("#total").val())){
						$("#page").val(2);
					}else{
						$("#page").val(parseInt($("#page").val()) + 1);

					}

					$("#page").val();
					$('.grid').append($elements)
					$('.grid').masonry( 'appended', $elements);
					$('div#loadmoreajaxloader').hide();
				}else{

					alert("failure");
					$('div#loadmoreajaxloader').html('<center>No more posts to show.</center>');
				}
			}
		});
	}
});

