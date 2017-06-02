
// when selecting register wifi
$('#register_node').on('click', function(){
	var node_ssid = $('#network_name').val()
	console.log('Register Node: ' + node_ssid)

	$.ajax({
            url: '/register_node',
            data: {
                'ssid': node_ssid,
            },
            dataType: 'json',
            success: function (data) {
            	console.log(data)
            } // success fn
        });// ajax req
})