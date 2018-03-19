$(function(){
	$("#snmpForm").on('submit', function(e){
		e.preventDefault();
		var getSubtreeCheckBox = $('#snmpForm [name="GetSubtree"]')
		if(getSubtreeCheckBox.prop("checked") == true){
			var url = "/snmp/getBulk_by_oid"
		}
		else{
			var url = "/snmp/get_by_oid"
		}
		console.log(JSON.stringify(translateToJSON($('#snmpForm'))))
		$.ajax({
			url: url,
			type: 'POST',
			
			dataType: 'json',
			data: JSON.stringify(translateToJSON($('#snmpForm')))
		})
		.done(function(res) {
			if(res){
				console.log(typeof(res["SnmpReply"]))
				var resultStr = ''
				for(var k in res["SnmpReply"]) {
	   				resultStr += "<li>" + res["SnmpReply"][k] + "</li>";
				}
				showResult(resultStr);
			}
	
		})
		.fail(function(error) {
			showResult(error.statusText, true);
		}) 
	
		
	})

})

function showResult(formattedResult, error=false){
	if(error == true){
		$("#snmpResultHeader")
			.html("An error has occured:")
			.css({color: 'red',});

	}
	else{
		$("#snmpResultHeader")
			.html("Result:")
			.css({color: 'black',});

	}
	$("#snmpResult").html(formattedResult);
}

 function translateToJSON($form){
 	var unindexedArray = $form.serializeArray();
 	var indexedArray = {};
 	$.map(unindexedArray, function(index, elem) {
 		indexedArray[index['name']] = index['value'];

 	});
 	return indexedArray;
 }