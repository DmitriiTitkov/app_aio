$(function(){
	var authForm = $('#authForm')
	var url = "http://192.168.63.10/auth"
	authForm.on("submit", function(e){
		e.preventDefault();
		$.ajax({
			url: url,
			type: 'POST',
			dataType: 'json',
			data: JSON.stringify(translateToJSON($('#authForm')))
		})
		.done(function(res){
			console.log(res)
		})
	})

	function translateToJSON($form){
 		var unindexedArray = $form.serializeArray();
 		var indexedArray = {};
 		$.map(unindexedArray, function(index, elem) {
 			indexedArray[index['name']] = index['value'];
	
 		});
 		return indexedArray;
 	}
})