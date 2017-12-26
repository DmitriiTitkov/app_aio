$(function(){
	$("#snmpForm").on('submit', function(e){
		e.preventDefault();
		$.ajax({
			url: '/',
			type: 'POST',
			dataType: 'json',
			data: $('#snmpForm').serialize()
		})
		.done(function(res) {
			if(res){
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

