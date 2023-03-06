$(document).ready(function()
{	
	//alert auto close and delay    
    $(".alert").delay(3500).slideUp(1000, function() {
    $(this).alert('close');
	});
  		
});
   